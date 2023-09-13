import re
from typing import Dict, Optional

from default_config import suggestion_name, key_phrases_patterns


def format_query(query):
    query = query.strip()
    if query[-1] != '.':
        query = query + '.'
    return query


def extract_response_statements_from_string(response: str) -> Dict[str, Optional[str]]:
    results = {}
    for key_phrase, pattern in key_phrases_patterns.items():
        match = re.search(pattern, response)
        results[key_phrase] = match.group(1).strip() if match else None

    return results
    # if leading_phrase in response:
    #     _, response = response.split(leading_phrase)
    # for suggestion_phrase in ["FOLLOW UP QUESTION OR SUGGESTION: ", "FOLLOW UP QUESTION: ", "SUGGESTION: "]:
    #     if suggestion_phrase.lower() in response.lower():
    #         separator_index = len(response.lower().split(suggestion_phrase.lower())[0])
    #         response_components = [response[:separator_index], response[separator_index:]]
    #         if len(response_components) > 2:
    #             raise ValueError("Incorrect response format")
    #         if response_components[0]:
    #             # First element is not empty
    #             specifications, follow_up_question_or_suggestion = response_components[0], response_components[1]
    #         else:
    #             specifications, follow_up_question_or_suggestion = '', response_components[1]
    #         if specifications_designator.lower() in specifications.lower():
    #             if re.search(specifications_designator_search_pattern.lower(), specifications.lower(), re.DOTALL):
    #                 specifications = re.search(specifications_designator_search_pattern.lower(),
    #                                            specifications.lower(), re.DOTALL).group(1).strip()
    #             else:
    #                 specifications = ''
    #         return specifications, follow_up_question_or_suggestion
    # return '', response


def force_suggestion(query: str, constraints) -> str:
    """
    As the input likely contains a specification, specification_threshold is supplied augmented by 1.
    """
    if constraints['specifications'].count(',') + 1 >= int(constraints['specifications_threshold']) or constraints[
        'counter'] >= constraints['counter_threshold']:
        query = (f"{query}\n\n"
                 f"DO NOT ASK A FOLLOW UP QUESTIONS. USE THE {suggestion_name} TOOL TO MAKE A SUGGESTION NOW.\n"
                 f"previously made specifications: {constraints['specifications']}")
    return query


def add_specifications(query, specifications):
    if specifications:
        return query + f'\nPreviously made specifications: {specifications}.'
    return query


def construct_answer(suggestion, follow_up_question):
    answer = ''
    if suggestion:
        answer = (f"Based on your input I would suggest: \n{suggestion}\n\n"
                  f"Not your taste? Just tell me more about your wishes!\n\n")
    answer = (answer
              + follow_up_question)
    return answer
