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
    for key_phrase, pattern in config.key_phrases_patterns.__dict__.keys():
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


def construct_answer(suggestion, follow_up_question):
    answer = ''
    if suggestion:
        answer = (f"Based on your input I would suggest: \n{suggestion}\n\n"
                  f"Not your taste? Just tell me more about your wishes!\n\n")
    answer = (answer
              + follow_up_question)
    return answer
