import re
from typing import Dict, Optional

from ConfigLoader import config


def format_query(query):
    query = query.strip()
    if query[-1] != '.':
        query = query + '.'
    return query


def extract_response_statements_from_string(response: str) -> Dict[str, Optional[str]]:
    results = {}
    for key_phrase, pattern in config.key_phrases_patterns.__dict__.items():
        match = re.search(pattern, response)
        results[key_phrase] = match.group(1).strip() if match else None

    return results


def force_suggestion(query: str, constraints) -> str:
    """
    As the input likely contains a specification, specification_threshold is supplied augmented by 1.
    """
    if constraints['specifications'].count(',') + 1 >= int(constraints['specifications_threshold']) or constraints[
        'counter'] >= constraints['counter_threshold']:
        query = (f"{query}\n\n"
                 f"DO NOT ASK A FOLLOW UP QUESTIONS. USE THE {config.suggestion_name} TOOL TO MAKE A SUGGESTION NOW.\n"
                 f"previously made specifications: {constraints['specifications']}")
    return query


def add_specifications(query, specifications):
    if specifications:
        return query + f'\nPreviously made specifications: {specifications}.'
    return query


def add_comparison_description(query, comparison_desription):
    if comparison_desription:
        return query + f'\nChoose one similar to the following description: {comparison_desription}'
    return query


def construct_answer(suggestion, follow_up_question):
    answer = ''
    if suggestion:
        answer = (f"Based on your input I would suggest: \n{suggestion}\n\n"
                  f"Not your taste? Just tell me more about your wishes!\n\n")
    if follow_up_question:
        answer = (answer
                  + follow_up_question)
    return answer


def extract_category_and_object_of_comparison(response: str) -> dict:
    try:
        # Initialize variables to hold the extracted category and object_for_comparison
        category = None
        object_for_comparison = None

        # Split the response by lines and loop through each line
        for line in response.split('\n'):
            # Check if the line starts with "category:" and extract the category
            if line.strip().lower().startswith("category:"):
                category = line.split(":", 1)[1].strip()
            # Check if the line starts with "object for comparison:" and extract the object_for_comparison
            elif line.strip().lower().startswith("object for comparison:"):
                object_for_comparison = line.split(":", 1)[1].strip()

        # Check if category is extracted, if not raise a ValueError
        if category is None:
            raise ValueError("Category not found in the provided response.")

        # Return the extracted information as a dictionary
        return {
            config.selected_pipeline_phrase: clean_string(category),
            config.object_for_comparison_phrase: clean_string(object_for_comparison)
        }
    except Exception as e:
        # Handle any unexpected error and raise it with a custom message
        raise ValueError(f"An error occurred while extracting information: {str(e)}")


def clean_string(input_string: str) -> str:
    # Define a regex pattern to match allowed characters
    pattern = re.compile('[^a-zA-Z0-9\-\[\]()\s]')
    # Substitute disallowed characters with an empty string
    cleaned_string = pattern.sub('', input_string)
    return cleaned_string
