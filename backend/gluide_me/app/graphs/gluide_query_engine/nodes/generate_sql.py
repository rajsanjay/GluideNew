import os
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from ..state import GluideMeState


# Get the intent configuration directory
CONFIG_DIR = Path(__file__).parent.parent.parent.parent.parent / "config"


def load_intent_templates():
    """
    Load SQL templates from intent.json configuration file.

    Returns:
        dict: Intent configuration with SQL templates
    """
    intent_file = CONFIG_DIR / "intent.json"

    try:
        with open(intent_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: intent.json not found at {intent_file}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing intent.json: {e}")
        return {}


def generate_sql_for_general_question(state: GluideMeState) -> GluideMeState:
    """
    Generate SQL query based on intent, sub-intent, and extracted parameters.

    This node uses template-based SQL generation for standard queries.
    Templates are defined in config/intent.json and mapped to specific
    intent + sub-intent combinations.

    For complex queries that don't fit templates, this could delegate to
    Vanna.ai NL2SQL (see nl2sql_components/database_utils.py).

    Args:
        state: Current GluideMeState containing main_intent, sub_intent, and acquired_params

    Returns:
        Updated GluideMeState with sql_query set
    """
    # Get required data from state
    main_intent = state.get("main_intent", "GENERAL")
    sub_intent = state.get("sub_intent", "GENERAL")
    acquired_params = state.get("acquired_params", {})

    # Load intent configuration
    intent_config = load_intent_templates()

    # Find the matching SQL template
    sql_template = None
    template_key = f"{main_intent}_{sub_intent}"

    # Try to find template for specific intent/sub-intent combination
    if main_intent in intent_config:
        intent_data = intent_config[main_intent]

        # Look for sub-intent specific template
        if "templates" in intent_data and sub_intent in intent_data["templates"]:
            sql_template = intent_data["templates"][sub_intent]
        # Fall back to default template for this intent
        elif "default_template" in intent_data:
            sql_template = intent_data["default_template"]

    # If no template found, use Vanna.ai for complex NL2SQL
    if not sql_template:
        # For now, return error - in production, could call Vanna here
        state["sql_query"] = ""
        print(f"Warning: No SQL template found for {main_intent}/{sub_intent}")
        return state

    # Replace parameters in SQL template
    try:
        sql_query = sql_template

        # Replace common parameter placeholders
        replacements = {
            "{to_collage}": acquired_params.get("to_collage", ""),
            "{from_collage}": acquired_params.get("from_collage", ""),
            "{major}": acquired_params.get("major", ""),
            "{courses}": str(acquired_params.get("courses", [])),
            "{to_college}": acquired_params.get("to_collage", ""),  # Alternative spelling
            "{from_college}": acquired_params.get("from_collage", ""),  # Alternative spelling
        }

        for placeholder, value in replacements.items():
            sql_query = sql_query.replace(placeholder, value)

        # Update state with generated SQL
        state["sql_query"] = sql_query

    except Exception as e:
        print(f"Error generating SQL: {e}")
        state["sql_query"] = ""

    return state


def generate_sql_with_vanna(state: GluideMeState) -> GluideMeState:
    """
    Generate SQL using Vanna.ai for complex queries.

    This is an alternative to template-based generation for queries that
    are too complex or don't fit predefined templates.

    Args:
        state: Current GluideMeState

    Returns:
        Updated GluideMeState with sql_query set
    """
    from .....nl2sql_components.database_utils import generate_sql

    user_input = state.get("input", "")

    try:
        # Use Vanna to generate SQL from natural language
        sql_query = generate_sql(user_input)
        state["sql_query"] = sql_query

    except Exception as e:
        print(f"Error generating SQL with Vanna: {e}")
        state["sql_query"] = ""

    return state
