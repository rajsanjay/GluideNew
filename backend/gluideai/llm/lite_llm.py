from .base import LLMInterface
from typing import List
import os
from django.conf import settings


class LiteLLM(LLMInterface):
    """
    LiteLLM implementation for OpenAI API calls.
    Reference: REWRITE_SPECIFICATION.md lines 739-815

    Works in two modes:
    - TEST mode: Returns mock data
    - DATABASE mode: Calls real OpenAI API
    """

    def __init__(self):
        self.model = "gpt-4o"  # EXACT model string from documentation
        self.use_test_mode = getattr(settings, 'USE_TEST_MODE', False)

    def generate(
        self,
        messages: List[dict],
        response_format: dict = None,
        temperature: float = 0.0
    ) -> dict:
        """
        Generate completion from LLM.

        In TEST mode: Returns mock structured data
        In DATABASE mode: Calls OpenAI API
        """
        if self.use_test_mode:
            return self._generate_mock_response(response_format)

        return self._generate_real_response(messages, response_format, temperature)

    def _generate_mock_response(self, response_format):
        """Generate mock response for TEST mode."""
        if response_format:
            # Return mock data matching Transcript model
            return {
                "courses": [
                    {
                        "college": "Mock College",
                        "major": "Computer Science",
                        "semester": "Fall",
                        "year": "2023",
                        "course_code": "CS 101",
                        "course_title": "Intro to Programming",
                        "credit": "3.00",
                        "grade": "A"
                    }
                ]
            }
        return {}

    def _generate_real_response(self, messages, response_format, temperature):
        """Generate real response using OpenAI API."""
        try:
            import litellm

            # Configure API key
            os.environ['OPENAI_API_KEY'] = settings.OPENAI_API_KEY

            # Build completion args
            completion_args = {
                'model': self.model,
                'messages': messages,
                'temperature': temperature,
            }

            # Add structured output if provided
            if response_format:
                completion_args['response_format'] = {
                    'type': 'json_object',
                    'schema': response_format.model_json_schema()
                }

            # Call LiteLLM
            response = litellm.completion(**completion_args)

            # Parse response
            content = response.choices[0].message.content

            # If structured output requested, parse JSON
            if response_format:
                import json
                return json.loads(content)

            return {'content': content}

        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
