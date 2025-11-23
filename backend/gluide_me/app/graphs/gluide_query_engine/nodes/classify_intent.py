import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..state import GluideMeState


def classify_main_intent(state: GluideMeState) -> GluideMeState:
    """
    Classify user's query into one of the predefined intent categories.
    
    Intent Categories:
    - GET_ALL_MAJORS: User wants to see all available majors
    - AVAILABLE_MAJORS: User wants to see majors available at specific colleges
    - COURSE_REQUIREMENTS: User asks about course requirements for a major/program
    - COURSE_TRANSFERABILITY: User asks about course transfer between colleges
    - GENERAL: General questions or unclear intent
    
    Args:
        state: Current GluideMeState containing user input
        
    Returns:
        Updated GluideMeState with main_intent set
    """
    # Get user input
    user_input = state.get("input", "")
    
    # Initialize LLM
    model_name = os.getenv("ROUTING_MODEL", "gpt-4o-2024-08-06")
    llm = ChatOpenAI(model=model_name, temperature=0)
    
    # Create classification prompt
    system_prompt = """You are an intent classifier for an academic counseling system.
Your job is to classify user queries into one of the following categories:

1. GET_ALL_MAJORS - User wants to see all available majors/programs (e.g., "What majors are available?", "Show me all majors")

2. AVAILABLE_MAJORS - User wants to see majors available at specific colleges or institutions (e.g., "What majors does UC Berkeley offer?", "Which programs are at De Anza College?")

3. COURSE_REQUIREMENTS - User asks about course requirements for a major or program (e.g., "What courses do I need for Computer Science?", "Requirements for Biology major")

4. COURSE_TRANSFERABILITY - User asks about course transfer between colleges (e.g., "Does this course transfer to UCLA?", "Which courses are transferable?")

5. GENERAL - General questions or queries that don't fit the above categories

Respond with ONLY the category name (e.g., "GET_ALL_MAJORS"). Do not include any explanation."""

    # Call LLM for classification
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Classify this query: {user_input}")
    ]
    
    response = llm.invoke(messages)
    main_intent = response.content.strip()
    
    # Validate intent is one of the allowed categories
    allowed_intents = [
        "GET_ALL_MAJORS",
        "AVAILABLE_MAJORS",
        "COURSE_REQUIREMENTS",
        "COURSE_TRANSFERABILITY",
        "GENERAL"
    ]
    
    if main_intent not in allowed_intents:
        main_intent = "GENERAL"
    
    # Update state
    state["main_intent"] = main_intent
    
    return state
