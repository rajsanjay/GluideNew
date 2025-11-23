import os
import meilisearch
from ..state import GluideMeState


def params_spelling_corrector(state: GluideMeState) -> GluideMeState:
    """
    Correct spelling of colleges and majors using Meilisearch fuzzy search.

    This node uses Meilisearch to find the closest matching official names
    for colleges and majors mentioned in the user's query. This handles:
    - Misspellings (e.g., "Stanfrd" -> "Stanford")
    - Abbreviations (e.g., "UCB" -> "UC Berkeley")
    - Informal names (e.g., "Cal" -> "UC Berkeley")

    Args:
        state: Current GluideMeState containing acquired_params

    Returns:
        Updated GluideMeState with corrected parameter values
    """
    # Get acquired parameters
    acquired_params = state.get("acquired_params", {})

    # If no parameters acquired, return early
    if not acquired_params:
        return state

    # Get Meilisearch configuration
    meilisearch_host = os.getenv("MEILISEARCH_HOST", "http://localhost:7700")
    meilisearch_api_key = os.getenv("MEILISEARCH_API_KEY", "")
    course_index_name = os.getenv("MEILISEARCH_COURSE_INDEX", "courses")
    major_index_name = os.getenv("MEILISEARCH_MAJOR_INDEX", "majors")

    try:
        # Initialize Meilisearch client
        client = meilisearch.Client(meilisearch_host, meilisearch_api_key)

        # Create a copy of acquired_params to update
        corrected_params = acquired_params.copy()

        # Correct college names (from_collage, to_collage)
        for param_name in ['from_collage', 'to_collage']:
            if param_name in acquired_params and acquired_params[param_name]:
                college_query = acquired_params[param_name]

                try:
                    # Search for closest college match
                    results = client.index(course_index_name).search(
                        college_query,
                        {
                            'limit': 1,
                            'attributesToSearchOn': ['school_name', 'school_code']
                        }
                    )

                    # If we found a match, use the corrected name
                    if results.get('hits') and len(results['hits']) > 0:
                        corrected_name = results['hits'][0].get('school_name')
                        if corrected_name:
                            corrected_params[param_name] = corrected_name
                except Exception as e:
                    # If search fails, keep original value
                    print(f"Warning: Could not correct college name '{college_query}': {e}")
                    continue

        # Correct major name
        if 'major' in acquired_params and acquired_params['major']:
            major_query = acquired_params['major']

            try:
                # Search for closest major match
                results = client.index(major_index_name).search(
                    major_query,
                    {
                        'limit': 1,
                        'attributesToSearchOn': ['major_name', 'major_code']
                    }
                )

                # If we found a match, use the corrected name
                if results.get('hits') and len(results['hits']) > 0:
                    corrected_name = results['hits'][0].get('major_name')
                    if corrected_name:
                        corrected_params['major'] = corrected_name
            except Exception as e:
                # If search fails, keep original value
                print(f"Warning: Could not correct major name '{major_query}': {e}")

        # Update state with corrected parameters
        state["acquired_params"] = corrected_params

    except Exception as e:
        # If Meilisearch client initialization fails, keep original params
        print(f"Warning: Meilisearch not available, using original parameters: {e}")

    return state
