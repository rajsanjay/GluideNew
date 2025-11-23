import os
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..state import GluideMeState


# Get the prompts directory path
PROMPTS_DIR = Path(__file__).parent.parent.parent.parent / "prompts"


def get_jinja_environment():
    """
    Create and configure Jinja2 environment for template loading.

    Returns:
        Environment: Configured Jinja2 environment
    """
    return Environment(
        loader=FileSystemLoader(str(PROMPTS_DIR)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True
    )


def handle_generate_question_using_llm(state: GluideMeState) -> GluideMeState:
    """
    Generate contextual follow-up questions using LLM.

    This node analyzes the conversation context and generates 3-5 relevant
    follow-up questions that:
    1. Explore related topics
    2. Dive deeper into the current topic
    3. Address practical next steps for students

    The questions are personalized based on:
    - Original user question
    - Answer provided
    - Main intent category
    - Extracted parameters (colleges, majors, etc.)

    Args:
        state: Current GluideMeState containing input, answer, and main_intent

    Returns:
        Updated GluideMeState with follow_up_questions list
    """
    # Get required data from state
    user_input = state.get("input", "")
    answer = state.get("answer", "")
    main_intent = state.get("main_intent", "GENERAL")
    acquired_params = state.get("acquired_params", {})

    # If no answer was generated, skip follow-up questions
    if not answer:
        state["follow_up_questions"] = []
        return state

    # Determine topic from main intent and parameters
    topic = _get_topic_from_context(main_intent, acquired_params)

    # Load Jinja2 template
    try:
        jinja_env = get_jinja_environment()
        template = jinja_env.get_template("followup_question.j2")

        # Render template with context
        template_context = {
            "topic": topic,
            "previous_question": user_input,
            "answer": answer,
            "main_intent": main_intent,
            "acquired_params": acquired_params
        }

        prompt = template.render(**template_context)

    except TemplateNotFound:
        # If template not found, use default prompt
        print("Warning: followup_question.j2 template not found, using default prompt")
        prompt = f"""Based on the conversation about {topic}, generate 3-5 relevant follow-up questions.

Previous question: {user_input}
Answer provided: {answer}

Generate questions that:
1. Explore related topics
2. Dive deeper into the current topic
3. Address practical next steps"""

    except Exception as e:
        print(f"Error loading template: {e}")
        # Use basic prompt if template fails
        prompt = f"Generate 3-5 follow-up questions for: {user_input}"

    # Initialize LLM for follow-up generation
    model_name = os.getenv("FOLLOWUP_GENERATION_MODEL", "gpt-4o-2024-08-06")
    llm = ChatOpenAI(model=model_name, temperature=0.7)  # Higher temp for creative questions

    # Create system prompt
    system_prompt = """You are an academic counseling assistant helping students explore their educational options.

Your task is to generate 3-5 relevant, helpful follow-up questions based on the conversation.

Guidelines for follow-up questions:
1. **Relevant**: Directly related to the topic discussed
2. **Progressive**: Build on the information already provided
3. **Actionable**: Help students take next steps
4. **Diverse**: Cover different aspects (requirements, timeline, alternatives, etc.)
5. **Natural**: Phrased as students would actually ask
6. **Specific**: Include colleges/majors mentioned when relevant

Question types to include:
- Deeper exploration (e.g., "What are the prerequisites for...")
- Related topics (e.g., "Are there similar programs at...")
- Practical steps (e.g., "How do I apply to...")
- Alternatives (e.g., "What other majors offer similar career paths...")
- Timeline (e.g., "When should I start applying...")

Format:
Return ONLY a JSON array of strings, no other text.
Example: ["Question 1?", "Question 2?", "Question 3?"]

DO NOT include explanations, numbering, or any text besides the JSON array."""

    # Call LLM to generate follow-up questions
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt)
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

            follow_up_questions = json.loads(response_text)

            # Validate it's a list of strings
            if not isinstance(follow_up_questions, list):
                raise ValueError("Response is not a list")

            # Filter to only strings and limit to 5 questions
            follow_up_questions = [
                q for q in follow_up_questions
                if isinstance(q, str) and q.strip()
            ][:5]

            # Update state
            state["follow_up_questions"] = follow_up_questions

        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing follow-up questions JSON: {e}")
            print(f"Response: {response_text}")

            # Try to extract questions from plain text response
            follow_up_questions = _extract_questions_from_text(response_text)
            state["follow_up_questions"] = follow_up_questions

    except Exception as e:
        print(f"Error generating follow-up questions: {e}")
        # Return empty list if generation fails
        state["follow_up_questions"] = []

    return state


def _get_topic_from_context(main_intent: str, acquired_params: dict) -> str:
    """
    Determine the conversation topic from intent and parameters.

    Args:
        main_intent: Main intent category
        acquired_params: Extracted parameters

    Returns:
        str: Topic description for follow-up generation
    """
    # Extract key parameters
    major = acquired_params.get("major", "")
    to_college = acquired_params.get("to_collage", "")
    from_college = acquired_params.get("from_collage", "")

    # Build topic string based on intent and available params
    if main_intent == "GET_ALL_MAJORS":
        return "available academic majors and programs"
    elif main_intent == "AVAILABLE_MAJORS":
        if to_college:
            return f"majors available at {to_college}"
        return "majors available at specific colleges"
    elif main_intent == "COURSE_REQUIREMENTS":
        if major and to_college:
            return f"{major} requirements at {to_college}"
        elif major:
            return f"{major} requirements"
        return "course requirements"
    elif main_intent == "COURSE_TRANSFERABILITY":
        if from_college and to_college:
            return f"transferring from {from_college} to {to_college}"
        elif to_college:
            return f"transferring to {to_college}"
        return "course transfer between colleges"
    else:
        return "academic planning and transfer"


def _extract_questions_from_text(text: str) -> list:
    """
    Extract questions from plain text if JSON parsing fails.

    Args:
        text: Response text that may contain questions

    Returns:
        list: Extracted questions
    """
    questions = []

    # Split by newlines and look for question marks
    lines = text.split("\n")
    for line in lines:
        line = line.strip()

        # Skip empty lines or markdown formatting
        if not line or line.startswith("#") or line.startswith("**"):
            continue

        # Remove numbering (1., 2., etc.)
        if line and line[0].isdigit() and "." in line:
            line = line.split(".", 1)[1].strip()

        # Remove bullet points
        line = line.lstrip("-•*").strip()

        # If line ends with question mark, it's likely a question
        if line.endswith("?"):
            questions.append(line)

    # Limit to 5 questions
    return questions[:5]
