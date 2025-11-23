"""
Gluide Me - Complete LangGraph Workflow

This module defines the complete LangGraph workflow for processing student queries
about courses, majors, and college transfers. The workflow consists of multiple
nodes that handle intent classification, parameter extraction, SQL generation,
and answer formatting.

Workflow Structure:
    START
    → classify_main_intent: Classify user query into main intent categories
    → classify_sub_intent: Determine specific sub-intent for SQL template selection
    → extract_params: Extract required parameters (colleges, majors, etc.)
    → [CONDITIONAL ROUTING]
        ├─ If missing params → prepare_prompt_for_missing_params → END
        ├─ If GENERAL intent → generate_answer → generate_follow_ups → END
        └─ Otherwise → spell_check_params → generate_sql → execute_sql
                    → generate_answer → generate_follow_ups → END

Usage:
    from gluide_me.workflow import app

    result = app.invoke({
        "input": "What majors are available at UC Berkeley?",
        "messages": []
    })

    print(result["answer"])
    print(result["follow_up_questions"])
"""

from langgraph.graph import StateGraph, START, END
from .app.graphs.gluide_query_engine.state import GluideMeState
from .app.graphs.gluide_query_engine.nodes.classify_intent import classify_main_intent
from .app.graphs.gluide_query_engine.nodes.classify_sub_intent import classify_sub_intent
from .app.graphs.gluide_query_engine.nodes.extract_params import extract_required_question_params
from .app.graphs.gluide_query_engine.nodes.spell_checker import params_spelling_corrector
from .app.graphs.gluide_query_engine.nodes.generate_sql import generate_sql_for_general_question
from .app.graphs.gluide_query_engine.nodes.execute_sql import query_postgres_database
from .app.graphs.gluide_query_engine.nodes.generate_answer import generate_http_final_answer_from_postgres_output
from .app.graphs.gluide_query_engine.nodes.follow_up import handle_generate_question_using_llm
from .app.graphs.gluide_query_engine.nodes.handle_missing_params import prepare_prompt_for_missing_params


def route_after_param_extraction(state: GluideMeState) -> str:
    """
    Router function to determine next node after parameter extraction.

    Decision logic:
    1. If missing_params is not empty → Ask user for missing information
    2. If main_intent is GENERAL → Skip SQL generation, generate direct answer
    3. Otherwise → Proceed with SQL generation workflow

    Args:
        state: Current GluideMeState

    Returns:
        str: Next node name
    """
    missing_params = state.get("missing_params", [])
    main_intent = state.get("main_intent", "GENERAL")

    # If we're missing required parameters, ask the user
    if missing_params:
        return "prepare_prompt_for_missing_params"

    # If it's a general question, generate answer directly without SQL
    if main_intent == "GENERAL":
        return "generate_answer_direct"

    # Otherwise, proceed with SQL generation workflow
    return "spell_check_params"


def route_after_missing_params(state: GluideMeState) -> str:
    """
    Router function after handling missing parameters.

    Since we're asking the user for more info, we end the workflow here.

    Args:
        state: Current GluideMeState

    Returns:
        str: Always returns END
    """
    return END


def route_after_answer_generation(state: GluideMeState) -> str:
    """
    Router function after answer generation.

    Determines if we should generate follow-up questions or end.

    Args:
        state: Current GluideMeState

    Returns:
        str: Next node name or END
    """
    # Always generate follow-up questions after successful answer
    return "generate_follow_ups"


def generate_answer_direct(state: GluideMeState) -> GluideMeState:
    """
    Generate answer for GENERAL intent queries without SQL execution.

    For general questions that don't require database queries, we can
    generate a response directly using the LLM.

    Args:
        state: Current GluideMeState

    Returns:
        Updated GluideMeState with answer
    """
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import SystemMessage, HumanMessage
    import os

    user_input = state.get("input", "")

    # Initialize LLM
    model_name = os.getenv("ANSWER_GENERATION_MODEL", "gpt-4o-2024-08-06")
    llm = ChatOpenAI(model=model_name, temperature=0.3)

    system_prompt = """You are an academic counseling assistant helping students with course planning and college transfer information.

Answer the student's question in a friendly, helpful manner. If the question is about specific courses, majors, or colleges, let them know they can ask more specific questions and you'll look up the exact information for them.

Use markdown formatting for clarity."""

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Student question: {user_input}")
        ]

        response = llm.invoke(messages)
        state["answer"] = response.content.strip()

    except Exception as e:
        print(f"Error generating direct answer: {e}")
        state["answer"] = "I'm here to help with your academic planning questions. Could you please provide more details about what you'd like to know?"

    return state


# Create the workflow graph
workflow = StateGraph(GluideMeState)

# Add all nodes to the graph
workflow.add_node("classify_main_intent", classify_main_intent)
workflow.add_node("classify_sub_intent", classify_sub_intent)
workflow.add_node("extract_params", extract_required_question_params)
workflow.add_node("spell_check_params", params_spelling_corrector)
workflow.add_node("generate_sql", generate_sql_for_general_question)
workflow.add_node("execute_sql", query_postgres_database)
workflow.add_node("generate_answer", generate_http_final_answer_from_postgres_output)
workflow.add_node("generate_answer_direct", generate_answer_direct)
workflow.add_node("generate_follow_ups", handle_generate_question_using_llm)
workflow.add_node("prepare_prompt_for_missing_params", prepare_prompt_for_missing_params)

# Define the workflow edges

# Start of workflow
workflow.add_edge(START, "classify_main_intent")

# Sequential classification steps
workflow.add_edge("classify_main_intent", "classify_sub_intent")
workflow.add_edge("classify_sub_intent", "extract_params")

# Conditional routing after parameter extraction
workflow.add_conditional_edges(
    "extract_params",
    route_after_param_extraction,
    {
        "prepare_prompt_for_missing_params": "prepare_prompt_for_missing_params",
        "generate_answer_direct": "generate_answer_direct",
        "spell_check_params": "spell_check_params"
    }
)

# If missing params, end workflow after prompting user
workflow.add_conditional_edges(
    "prepare_prompt_for_missing_params",
    route_after_missing_params
)

# SQL generation workflow path
workflow.add_edge("spell_check_params", "generate_sql")
workflow.add_edge("generate_sql", "execute_sql")
workflow.add_edge("execute_sql", "generate_answer")

# Both answer generation paths lead to follow-ups
workflow.add_edge("generate_answer", "generate_follow_ups")
workflow.add_edge("generate_answer_direct", "generate_follow_ups")

# Follow-ups lead to end
workflow.add_edge("generate_follow_ups", END)

# Compile the workflow
app = workflow.compile()


# Export the compiled workflow
__all__ = ["app", "GluideMeState"]
