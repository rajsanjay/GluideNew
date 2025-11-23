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
        autoescape=False,  # Don't escape HTML/special characters
        trim_blocks=True,
        lstrip_blocks=True
    )


def generate_http_final_answer_from_postgres_output(state: GluideMeState) -> GluideMeState:
    """
    Generate natural language answer from SQL query results.

    This node takes the structured SQL output and converts it into a
    student-friendly, markdown-formatted response using:
    1. Jinja2 templates (intent-specific formatting)
    2. OpenAI LLM (natural language generation)

    The response format includes:
    - Clear, conversational language
    - Markdown formatting (headers, bullet points, tables)
    - Student-friendly explanations
    - Actionable information

    Args:
        state: Current GluideMeState containing main_intent and sql_output

    Returns:
        Updated GluideMeState with answer containing formatted response
    """
    # Get required data from state
    main_intent = state.get("main_intent", "GENERAL")
    sub_intent = state.get("sub_intent", "GENERAL")
    sql_output = state.get("sql_output", "{}")
    user_input = state.get("input", "")
    acquired_params = state.get("acquired_params", {})

    # Parse SQL output JSON
    try:
        sql_data = json.loads(sql_output)
        results = sql_data.get("results", [])
        success = sql_data.get("success", False)
        error = sql_data.get("error")
    except json.JSONDecodeError:
        results = []
        success = False
        error = "Failed to parse SQL output"

    # If query failed, return error message
    if not success or error:
        state["answer"] = f"""I encountered an error while processing your request:

**Error:** {error}

Please try rephrasing your question or contact support if the issue persists."""
        return state

    # If no results, return friendly message
    if not results:
        state["answer"] = """I couldn't find any results matching your query.

**Suggestions:**
- Check the spelling of college or major names
- Try using different search terms
- Broaden your search criteria

Feel free to ask another question!"""
        return state

    # Map main intents to template files
    intent_template_map = {
        "GET_ALL_MAJORS": "intent_templates/get_all_majors.j2",
        "AVAILABLE_MAJORS": "intent_templates/available_majors.j2",
        "COURSE_REQUIREMENTS": "intent_templates/course_requirements.j2",
        "COURSE_TRANSFERABILITY": "intent_templates/course_transferability.j2",
        "GENERAL": "intent_templates/general.j2"
    }

    # Get template path for this intent
    template_path = intent_template_map.get(main_intent, "intent_templates/general.j2")

    try:
        # Load Jinja2 environment
        jinja_env = get_jinja_environment()

        # Try to load the template
        try:
            template = jinja_env.get_template(template_path)
        except TemplateNotFound:
            # Fall back to a generic template if specific one not found
            template = None

        # Prepare template context
        template_context = {
            "results": results,
            "user_query": user_input,
            "main_intent": main_intent,
            "sub_intent": sub_intent,
            "acquired_params": acquired_params,
            "result_count": len(results)
        }

        # Render template if available
        if template:
            formatted_data = template.render(**template_context)
        else:
            # If no template, create basic formatted output
            formatted_data = f"""Query Results:

Found {len(results)} result(s).

{json.dumps(results, indent=2)}"""

    except Exception as e:
        # If template rendering fails, use basic formatting
        print(f"Warning: Template rendering failed: {e}")
        formatted_data = f"""Query Results:

Found {len(results)} result(s).

{json.dumps(results, indent=2)}"""

    # Initialize LLM for answer generation
    model_name = os.getenv("ANSWER_GENERATION_MODEL", "gpt-4o-2024-08-06")
    llm = ChatOpenAI(model=model_name, temperature=0.3)  # Slightly higher temp for natural responses

    # Create system prompt for answer generation
    system_prompt = """You are an academic counseling assistant helping students with course planning and college transfer information.

Your task is to convert structured data into a friendly, conversational response.

Guidelines:
1. Use clear, student-friendly language
2. Format using Markdown (headers, bullet points, tables where appropriate)
3. Organize information logically
4. Highlight key information (e.g., transfer requirements, important deadlines)
5. Be encouraging and supportive
6. If showing multiple items, group them logically
7. Include relevant context (e.g., units, prerequisites, transfer agreements)
8. Use tables for comparing multiple items
9. Use bullet points for lists
10. Keep responses concise but complete

Example formats:

For a list of majors:
## Available Majors at [College Name]

Here are the majors available:

| Major | Type | Department |
|-------|------|------------|
| Computer Science | B.S. | Engineering |
| Biology | B.A./B.S. | Life Sciences |

For course requirements:
## Requirements for [Major] at [College]

To complete this major, you'll need:

**Lower Division Requirements:**
- Course 1 (Units)
- Course 2 (Units)

**Upper Division Requirements:**
- Course 3 (Units)
- Course 4 (Units)

Always end with an encouraging note or offer to help with follow-up questions."""

    # Create human message with formatted data
    human_message = f"""User's question: {user_input}

Data to format:
{formatted_data}

Generate a friendly, well-formatted response that answers the student's question."""

    # Call LLM to generate final answer
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message)
        ]

        response = llm.invoke(messages)
        final_answer = response.content.strip()

        # Update state with generated answer
        state["answer"] = final_answer

    except Exception as e:
        # If LLM fails, return formatted data with error note
        print(f"Error generating answer with LLM: {e}")
        state["answer"] = f"""{formatted_data}

*Note: Unable to generate enhanced response. Showing raw data above.*"""

    return state
