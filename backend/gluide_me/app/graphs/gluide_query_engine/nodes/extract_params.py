import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..state import GluideMeState


def extract_required_question_params(state: GluideMeState) -> GluideMeState:
    """
    Extract required parameters from user input based on the main intent.
    
    This node determines which parameters are needed for the query (based on intent),
    extracts them from the user's input, and tracks which parameters are still missing.
    
    Parameters that can be extracted:
    - from_collage: Source community college name
    - to_collage: Target university name
    - major: Academic major/program name
    - courses: List of course codes
    
    Args:
        state: Current GluideMeState containing user input and main_intent
        
    Returns:
        Updated GluideMeState with acquired_params and missing_params set
    """
    # Get user input and main intent
    user_input = state.get("input", "")
    main_intent = state.get("main_intent", "")
    sub_intent = state.get("sub_intent", "")
    
    # Initialize LLM
    model_name = os.getenv("RETRIEVE_QUESTION_PARAMS_MODEL", "gpt-4o-2024-08-06")
    llm = ChatOpenAI(model=model_name, temperature=0)
    
    # Define required parameters for each intent
    # This mirrors the structure in intent.json
    intent_params = {
        "GET_ALL_MAJORS": ["to_collage"],
        "AVAILABLE_MAJORS": ["to_collage"],
        "COURSE_REQUIREMENTS": ["major", "to_collage"],
        "COURSE_TRANSFERABILITY": ["from_collage", "to_collage", "major"],
        "GENERAL": []
    }
    
    # Get required parameters for this intent
    required_params = intent_params.get(main_intent, [])
    
    # If no parameters required, return early
    if not required_params:
        state["acquired_params"] = {}
        state["missing_params"] = []
        return state
    
    # Create parameter extraction prompt
    param_descriptions = {
        "from_collage": "The source community college or current institution (e.g., 'De Anza College', 'Foothill College')",
        "to_collage": "The target university or destination institution (e.g., 'UC Berkeley', 'Stanford', 'UCLA')",
        "major": "The academic major, program, or field of study (e.g., 'Computer Science', 'Biology', 'Engineering')",
        "courses": "List of specific course codes (e.g., ['CS 101', 'MATH 201'])"
    }
    
    # Build extraction instructions
    param_instructions = "\n".join([
        f"- {param}: {param_descriptions[param]}"
        for param in required_params
    ])
    
    system_prompt = f"""You are a parameter extraction assistant for an academic counseling system.

Extract the following parameters from the user's query:

{param_instructions}

Important instructions:
1. Extract ONLY the parameters that are explicitly mentioned or clearly implied in the query
2. Use full, official names for colleges and universities
3. Expand abbreviations when possible (e.g., "UCB" -> "UC Berkeley")
4. For courses, extract the exact course codes mentioned
5. If a parameter is not present in the query, do NOT include it in your response

Respond with a JSON object containing only the parameters you found. Example:
{{
    "to_collage": "UC Berkeley",
    "major": "Computer Science"
}}

If no parameters are found, respond with an empty JSON object: {{}}"""

    # Call LLM for parameter extraction
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Extract parameters from this query: {user_input}")
    ]
    
    response = llm.invoke(messages)
    response_text = response.content.strip()
    
    # Parse JSON response
    try:
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        acquired_params = json.loads(response_text)
    except json.JSONDecodeError:
        # If JSON parsing fails, return empty params
        acquired_params = {}
    
    # Determine missing parameters
    missing_params = [
        param for param in required_params
        if param not in acquired_params or not acquired_params[param]
    ]
    
    # Update state
    state["acquired_params"] = acquired_params
    state["missing_params"] = missing_params
    
    return state
