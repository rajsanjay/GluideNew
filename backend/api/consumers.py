"""
WebSocket consumers for real-time features.

This module contains WebSocket consumers for:
- Real-time chat between counselor and student (ChatConsumer)
- AI guidance with streaming responses (GluideAiWithStreaming)

Message formats are standardized and must match frontend expectations.
DO NOT modify message formats without updating the frontend client.
"""

import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for real-time chat between counselor and student.

    URL Pattern: ws/chat/{room_name}/
    Example: ws://localhost:8000/ws/chat/123/?session_id=abc

    Message Format:
        Client → Server:
        {
            "message": "string"
        }

        Server → Client:
        {
            "message": "string",
            "sender": "integer (user_id)",
            "created_at": "datetime",
            "room": "integer"
        }

    Security:
        - User must be authenticated (via AllauthSessionMiddleware)
        - User must be either the student or counselor of the room
        - Room access is validated on connection
    """

    async def connect(self):
        """
        Handle WebSocket connection.

        Validates user authentication and room access before accepting connection.
        Adds the WebSocket to the room's group for message broadcasting.
        """
        # Extract room_name from URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Validate user has access to room
        if not await self.user_can_access_room():
            await self.close()
            return

        # Add this channel to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.

        Removes the WebSocket from the room's group.

        Args:
            close_code: WebSocket close code
        """
        # Remove this channel from the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        """
        Handle incoming JSON message from client.

        Saves message to database and broadcasts to all room participants.

        Args:
            content: Parsed JSON content from client
                Expected format: {"message": "text"}
        """
        message = content.get('message', '')
        user = self.scope['user']

        # Save message to database
        saved_message = await self.save_message(message)

        # Broadcast to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.id,
                'created_at': timezone.now().isoformat(),
                'room': int(self.room_name)
            }
        )

    async def chat_message(self, event):
        """
        Handle chat_message event from room group.

        Sends the message to the WebSocket client.

        Args:
            event: Event data from group_send
                Contains: message, sender, created_at, room
        """
        await self.send_json(event)

    @database_sync_to_async
    def save_message(self, message):
        """
        Save chat message to database.

        Args:
            message: Message text to save

        Returns:
            ChatMessage: Created message object
        """
        from .models import ChatMessage, Room

        room = Room.objects.get(id=self.room_name)
        return ChatMessage.objects.create(
            room=room,
            sender=self.scope['user'],
            message=message
        )

    @database_sync_to_async
    def user_can_access_room(self):
        """
        Validate that the user has access to this room.

        User must be authenticated and be either:
        - The student in the room
        - The counselor in the room

        Returns:
            bool: True if user can access room, False otherwise
        """
        from .models import Room

        user = self.scope['user']

        # Check if user is authenticated
        if not user or not user.is_authenticated:
            return False

        try:
            room = Room.objects.get(id=self.room_name)
            # User must be either student or counselor
            return room.student == user or room.counselor == user
        except Room.DoesNotExist:
            return False


class GluideAiWithStreaming(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for AI guidance with streaming responses.

    URL Pattern: ws/ask-gluide/{room_name}/
    Example: ws://localhost:8000/ws/ask-gluide/session_abc123/?session_id=xyz

    Message Format:
        Client → Server:
        {
            "input": "string (user question)",
            "metadata": {
                "intent": "string",
                "acquired_params": {},
                "missing_params": []
            }
        }

        Server → Client (streaming):
        {
            "type": "message_chunk",
            "content": "string"
        }

        Server → Client (final):
        {
            "type": "complete",
            "message_id": "uuid",
            "sql_query": "string",
            "main_intent": "string",
            "sub_intent": "string"
        }

    Uses LangGraph workflow to process questions with streaming responses.
    Each chunk represents an incremental part of the answer.
    """

    async def connect(self):
        """
        Handle WebSocket connection.

        Validates session exists and belongs to authenticated user.
        """
        # Extract session_id from URL
        self.session_id = self.scope['url_route']['kwargs']['room_name']

        # Validate session exists and belongs to user
        if not await self.validate_session():
            await self.close()
            return

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.

        Args:
            close_code: WebSocket close code
        """
        # No cleanup needed for this consumer
        pass

    async def receive_json(self, content):
        """
        Handle incoming JSON message from client.

        Processes user question through LangGraph workflow with streaming.

        Args:
            content: Parsed JSON content from client
                Expected format: {
                    "input": "question",
                    "metadata": {
                        "intent": "...",
                        "acquired_params": {...},
                        "missing_params": [...]
                    }
                }
        """
        user_input = content.get('input', '')
        metadata = content.get('metadata', {})

        # Import workflow
        from gluide_me.workflow import app

        # Create initial state
        initial_state = {
            "messages": [],
            "input": user_input,
            "main_intent": metadata.get('intent', ''),
            "sub_intent": '',
            "acquired_params": metadata.get('acquired_params', {}),
            "missing_params": metadata.get('missing_params', []),
            "sql_query": '',
            "sql_output": '',
            "answer": '',
            "follow_up_questions": []
        }

        # Stream workflow execution
        try:
            # Stream chunks as workflow executes
            async for chunk in app.astream(initial_state):
                # Send chunk to client if answer is present
                if 'answer' in chunk and chunk.get('answer'):
                    await self.send_json({
                        "type": "message_chunk",
                        "content": chunk['answer']
                    })

            # Get final state after workflow completes
            final_state = await app.ainvoke(initial_state)

            # Save message to database
            message = await self.save_message(user_input, final_state)

            # Send completion message
            await self.send_json({
                "type": "complete",
                "message_id": str(message.message_id),
                "sql_query": final_state.get('sql_query', ''),
                "main_intent": final_state.get('main_intent', ''),
                "sub_intent": final_state.get('sub_intent', '')
            })

        except Exception as e:
            # Send error message to client
            await self.send_json({
                "type": "error",
                "message": str(e)
            })

    @database_sync_to_async
    def validate_session(self):
        """
        Validate that the session exists and belongs to the authenticated user.

        Returns:
            bool: True if session is valid, False otherwise
        """
        from .models import Session

        user = self.scope.get('user')

        # Check if user is authenticated
        if not user or not user.is_authenticated:
            return False

        # Check if session exists and belongs to user
        return Session.objects.filter(
            session_id=self.session_id,
            user=user
        ).exists()

    @database_sync_to_async
    def save_message(self, question, final_state):
        """
        Save AI guidance message to database.

        Args:
            question: User's question
            final_state: Final state from LangGraph workflow

        Returns:
            Message: Created message object
        """
        from .models import Message, Session

        session = Session.objects.get(session_id=self.session_id)
        return Message.objects.create(
            session=session,
            question=question,
            answer=final_state.get('answer', ''),
            sql_query=final_state.get('sql_query'),
            main_intent=final_state.get('main_intent'),
            sub_intent=final_state.get('sub_intent'),
            request_time=timezone.now(),
            response_time=timezone.now()
        )
