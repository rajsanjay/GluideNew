import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..state import GluideMeState


def classify_sub_intent(state: GluideMeState) -> GluideMeState:
    """
    Classify sub-intent based on the main intent to determine the specific SQL template.
    
    The sub-intent helps narrow down the exact type of query within the main intent category,
    which is then mapped to specific SQL templates in intent.json.
    
    Args:
        state: Current GluideMeState containing user input and main_intent
        
    Returns:
        Updated GluideMeState with sub_intent set
    """
    # Get user input and main intent
    user_input = state.get("input", "")
    main_intent = state.get("main_intent", "")
    
    # Initialize LLM
    model_name = os.getenv("ROUTING_MODEL", "gpt-4o-2024-08-06")
    llm = ChatOpenAI(model=model_name, temperature=0)
    
    # Define sub-intent options based on main intent
    sub_intent_map = {
        "GET_ALL_MAJORS": {
            "description": "Getting all available majors",
            "options": [
                "LIST_ALL_MAJORS - List all majors without filters",
                "LIST_BY_CATEGORY - List majors by category (STEM, Arts, etc.)",
                "GENERAL - Other variations"
            ]
        },
        "AVAILABLE_MAJORS": {
            "description": "Finding majors at specific colleges",
            "options": [
                "BY_COLLEGE_NAME - User specifies a college name",
                "BY_COLLEGE_TYPE - User asks about community colleges or universities",
                "BY_LOCATION - User asks about colleges in a specific area",
                "GENERAL - Other variations"
            ]
        },
        "COURSE_REQUIREMENTS": {
            "description": "Finding course requirements",
            "options": [
                "BY_MAJOR - Requirements for a specific major",
                "BY_PROGRAM - Requirements for a specific program",
                "BY_TRANSFER_PATH - Requirements for transfer between colleges",
                "BY_COURSE - Prerequisites or corequisites for a course",
                "GENERAL - Other variations"
            ]
        },
        "COURSE_TRANSFERABILITY": {
            "description": "Course transfer information",
            "options": [
                "SPECIFIC_COURSE - Transfer info for a specific course",
                "FROM_TO_COLLEGES - Transfer between specific colleges",
                "BY_MAJOR - Transferable courses for a major",
                "GENERAL_TRANSFER - General transferability questions",
                "GENERAL - Other variations"
            ]
        },
        "GENERAL": {
            "description": "General questions",
            "options": [
                "GENERAL - General inquiry"
            ]
        }
    }
    
    # Get sub-intent options for this main intent
    intent_info = sub_intent_map.get(main_intent, sub_intent_map["GENERAL"])
    
    # Create classification prompt
    system_prompt = f"""You are classifying the specific type of query for: {intent_info['description']}

Based on the user's question, classify it into one of these sub-categories:

{chr(10).join(intent_info['options'])}

Respond with ONLY the sub-category name (e.g., "BY_COLLEGE_NAME"). Do not include any explanation."""

    # Call LLM for classification
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Classify this query: {user_input}")
    ]
    
    response = llm.invoke(messages)
    sub_intent = response.content.strip()
    
    # Extract just the category name (remove description if present)
    if " - " in sub_intent:
        sub_intent = sub_intent.split(" - ")[0].strip()
    
    # Validate sub_intent is one of the allowed options
    allowed_sub_intents = [opt.split(" - ")[0].strip() for opt in intent_info['options']]
    
    if sub_intent not in allowed_sub_intents:
        sub_intent = "GENERAL"
    
    # Update state
    state["sub_intent"] = sub_intent
    
    return state
