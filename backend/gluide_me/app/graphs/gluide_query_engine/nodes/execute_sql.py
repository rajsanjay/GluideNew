import json
from django.db import connections
from ..state import GluideMeState


def query_postgres_database(state: GluideMeState) -> GluideMeState:
    """
    Execute SQL query against the course_db PostgreSQL database.

    This node executes the SQL query stored in state['sql_query'] against
    the course_db database (which contains academic course and transfer data).
    Results are converted to JSON and stored in state['sql_output'].

    The course_db database contains:
    - schools: College/university information
    - majors: Academic programs
    - courses: Course catalog
    - articulations: Course transfer agreements
    - requirements: Major requirements

    Args:
        state: Current GluideMeState containing sql_query

    Returns:
        Updated GluideMeState with sql_output containing query results or error
    """
    # Get SQL query from state
    sql_query = state.get("sql_query", "")

    # If no SQL query provided, return early
    if not sql_query:
        state["sql_output"] = json.dumps({
            "error": "No SQL query provided",
            "results": []
        })
        return state

    try:
        # Execute query against course_db database
        # CRITICAL: Use 'course_db' connection, NOT default database
        with connections['course_db'].cursor() as cursor:
            # Execute the SQL query
            cursor.execute(sql_query)

            # Get column names from cursor description
            columns = [col[0] for col in cursor.description]

            # Fetch all results and convert to list of dictionaries
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

            # Convert results to JSON string
            state["sql_output"] = json.dumps({
                "success": True,
                "row_count": len(results),
                "results": results
            }, default=str)  # default=str handles datetime and other non-JSON types

    except Exception as e:
        # Log error and return error message in sql_output
        error_message = f"Database error: {str(e)}"
        print(f"Error executing SQL query: {error_message}")
        print(f"SQL Query: {sql_query}")

        state["sql_output"] = json.dumps({
            "success": False,
            "error": error_message,
            "results": []
        })

    return state
