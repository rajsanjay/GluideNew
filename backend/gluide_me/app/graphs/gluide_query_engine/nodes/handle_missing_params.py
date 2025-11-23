from ..state import GluideMeState


def prepare_prompt_for_missing_params(state: GluideMeState) -> GluideMeState:
    """
    Generate a user-friendly prompt asking for missing parameters.

    This node is triggered when required parameters are missing from the user's query.
    It creates a conversational prompt asking the user to provide the missing information.

    Args:
        state: Current GluideMeState containing missing_params and acquired_params

    Returns:
        Updated GluideMeState with answer containing prompt for missing parameters
    """
    missing_params = state.get("missing_params", [])
    acquired_params = state.get("acquired_params", {})
    main_intent = state.get("main_intent", "GENERAL")

    # If no missing params, return early (this shouldn't happen, but safety check)
    if not missing_params:
        state["answer"] = "I have all the information I need to help you."
        state["follow_up_questions"] = []
        return state

    # Create friendly parameter names for display
    param_display_names = {
        "from_collage": "source college/community college",
        "to_collage": "target university/college",
        "major": "academic major or program",
        "courses": "course codes"
    }

    # Build the prompt
    missing_display = [
        param_display_names.get(param, param)
        for param in missing_params
    ]

    # Create context about what we already know
    context_parts = []
    if "to_collage" in acquired_params:
        context_parts.append(f"transferring to {acquired_params['to_collage']}")
    if "from_collage" in acquired_params:
        context_parts.append(f"from {acquired_params['from_collage']}")
    if "major" in acquired_params:
        context_parts.append(f"in {acquired_params['major']}")

    context_str = " ".join(context_parts) if context_parts else "help you"

    # Generate the prompt based on number of missing params
    if len(missing_display) == 1:
        prompt = f"""I'd be happy to help you {context_str}!

To provide accurate information, I need to know your **{missing_display[0]}**.

Could you please provide that information?"""

    else:
        params_list = "\n".join([f"- {param}" for param in missing_display])
        prompt = f"""I'd be happy to help you {context_str}!

To provide accurate information, I need a bit more detail:

{params_list}

Could you please provide these details?"""

    # Add helpful examples based on intent
    examples = _get_examples_for_intent(main_intent, missing_params)
    if examples:
        prompt += f"\n\n**Example:** {examples}"

    # Update state
    state["answer"] = prompt
    state["follow_up_questions"] = []  # No follow-ups when asking for info

    return state


def _get_examples_for_intent(main_intent: str, missing_params: list) -> str:
    """
    Generate helpful examples based on intent and missing parameters.

    Args:
        main_intent: Main intent category
        missing_params: List of missing parameter names

    Returns:
        str: Example query string
    """
    examples = {
        "AVAILABLE_MAJORS": {
            "to_collage": "What majors are available at UC Berkeley?",
            "default": "What majors does Stanford offer?"
        },
        "COURSE_REQUIREMENTS": {
            "major": "What courses do I need for Computer Science at UCLA?",
            "to_collage": "What are the Biology requirements at UC San Diego?",
            "default": "What are the requirements for Computer Science at UC Berkeley?"
        },
        "COURSE_TRANSFERABILITY": {
            "from_collage": "Which courses from De Anza transfer to UCLA for Computer Science?",
            "to_collage": "Do my Foothill courses transfer to Stanford?",
            "major": "What CS courses transfer from De Anza to UC Berkeley?",
            "default": "Which courses from De Anza College transfer to UC Berkeley for Computer Science?"
        },
        "GET_ALL_MAJORS": {
            "default": "What majors are available?"
        }
    }

    # Get examples for this intent
    intent_examples = examples.get(main_intent, {})

    # Try to find example for specific missing param
    if missing_params:
        first_missing = missing_params[0]
        if first_missing in intent_examples:
            return intent_examples[first_missing]

    # Return default example for this intent
    return intent_examples.get("default", "")
