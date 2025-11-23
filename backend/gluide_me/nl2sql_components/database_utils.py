"""
Vanna.ai integration for natural language to SQL conversion.

This module provides NL2SQL capabilities using Vanna.ai for COMPLEX queries only.
Simple queries should use template-based SQL from intent.json instead.

Usage:
    - Template-based (Simple): "What majors are available at UC Berkeley?"
    - Vanna-based (Complex): "Show me all CS courses from De Anza that transfer
                              to UCLA or Stanford and have been taken by students
                              with GPA > 3.5"
"""

import os
import django
from django.conf import settings
from vanna.openai.openai_chat import OpenAI_Chat
from vanna.postgres import PG_VectorStore


class VannaPostgres(PG_VectorStore, OpenAI_Chat):
    """
    Custom Vanna implementation using PostgreSQL vector store and OpenAI Chat.

    This class combines Vanna's PostgreSQL vector store (for storing training data)
    with OpenAI's chat model for SQL generation.
    """

    def __init__(self, config=None):
        """
        Initialize VannaPostgres with configuration.

        Args:
            config: Dictionary containing 'api_key' and 'model' for OpenAI
        """
        PG_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)


# Global Vanna instance
_vanna_instance = None


def get_vanna_instance():
    """
    Get or create the global Vanna instance.

    Returns:
        VannaPostgres: Configured Vanna instance
    """
    global _vanna_instance

    if _vanna_instance is None:
        # Get OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        # Get course_db database configuration
        course_db_config = settings.DATABASES.get('course_db')
        if not course_db_config:
            raise ValueError("course_db database not configured in Django settings")

        # Initialize Vanna with PostgreSQL vector store and OpenAI
        _vanna_instance = VannaPostgres(config={
            "api_key": api_key,
            "model": "gpt-4o",
            "host": course_db_config.get('HOST', 'localhost'),
            "port": course_db_config.get('PORT', '5432'),
            "database": course_db_config.get('NAME'),
            "user": course_db_config.get('USER'),
            "password": course_db_config.get('PASSWORD'),
        })

    return _vanna_instance


def train_on_schema():
    """
    Train Vanna on the course_db schema.

    This function should be run once during setup to train Vanna on the
    database schema. It extracts table structures, column information,
    and relationships from the course_db database.

    Tables trained on:
    - schools: College/university information
    - majors: Academic major/program information
    - courses: Course catalog information
    - articulations: Course transfer agreements
    - requirements: Major/program requirements

    Returns:
        bool: True if training was successful
    """
    try:
        vn = get_vanna_instance()

        # Get course_db database configuration
        course_db_config = settings.DATABASES.get('course_db')

        # Connect to course_db and train on schema
        vn.connect_to_postgres(
            host=course_db_config.get('HOST', 'localhost'),
            port=course_db_config.get('PORT', '5432'),
            dbname=course_db_config.get('NAME'),
            user=course_db_config.get('USER'),
            password=course_db_config.get('PASSWORD'),
        )

        # Train on database information schema
        # Vanna will automatically extract table structures, columns, and relationships
        df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

        # Train on specific important tables
        plan = vn.get_training_plan_generic(df_information_schema)
        vn.train(plan=plan)

        # Optionally add custom documentation for specific tables
        vn.train(documentation="""
        The course_db database contains academic course and transfer information:

        - schools: Contains college/university information (school_name, school_code)
        - majors: Academic programs (major_name, major_code)
        - courses: Course catalog (course_code, course_title, units)
        - articulations: Transfer agreements between colleges (from_school, to_school, from_course, to_course)
        - requirements: Major requirements (major_id, required_courses)
        """)

        print("Successfully trained Vanna on course_db schema")
        return True

    except Exception as e:
        print(f"Error training Vanna: {e}")
        return False


def generate_sql(question: str, use_training: bool = True) -> str:
    """
    Convert natural language question to SQL using Vanna.ai.

    This function should ONLY be used for complex queries that cannot be
    handled by template-based SQL from intent.json.

    Examples of when to use Vanna:
    - Complex multi-table joins with conditions
    - Queries requiring aggregations and grouping
    - Questions with multiple filters and nested conditions

    Examples of when NOT to use Vanna (use templates instead):
    - "What majors are available at UC Berkeley?" (simple lookup)
    - "Show all courses" (basic SELECT)
    - "List colleges" (simple query)

    Args:
        question: Natural language question
        use_training: Whether to use trained schema information

    Returns:
        str: Generated SQL query

    Raises:
        ValueError: If Vanna instance cannot be created
        Exception: If SQL generation fails
    """
    try:
        vn = get_vanna_instance()

        # Get course_db database configuration
        course_db_config = settings.DATABASES.get('course_db')

        # Connect to course_db
        vn.connect_to_postgres(
            host=course_db_config.get('HOST', 'localhost'),
            port=course_db_config.get('PORT', '5432'),
            dbname=course_db_config.get('NAME'),
            user=course_db_config.get('USER'),
            password=course_db_config.get('PASSWORD'),
        )

        # Generate SQL from natural language
        sql = vn.generate_sql(question=question)

        return sql

    except Exception as e:
        print(f"Error generating SQL with Vanna: {e}")
        raise


def execute_sql(sql: str):
    """
    Execute SQL query on course_db database.

    Args:
        sql: SQL query to execute

    Returns:
        DataFrame: Query results as pandas DataFrame
    """
    try:
        vn = get_vanna_instance()

        # Execute SQL and return results
        df = vn.run_sql(sql)

        return df

    except Exception as e:
        print(f"Error executing SQL: {e}")
        raise


def ask_vanna(question: str):
    """
    Complete end-to-end NL2SQL workflow: generate SQL, execute, and format.

    This is a convenience function that combines SQL generation and execution.
    Use this for complex queries that require Vanna's capabilities.

    Args:
        question: Natural language question

    Returns:
        tuple: (sql, results_dataframe)
    """
    try:
        # Generate SQL
        sql = generate_sql(question)

        # Execute SQL
        results = execute_sql(sql)

        return sql, results

    except Exception as e:
        print(f"Error in ask_vanna: {e}")
        raise
