import unittest
from unittest.mock import patch, MagicMock
from utils.string_operations import (
    format_query,
    extract_response_statements_from_string,
    force_suggestion,
    add_specifications,
    add_comparison_description,
    construct_answer,
    extract_category_and_object_of_comparison,
    clean_string,
)


class TestYourModule(unittest.TestCase):

    @patch('ConfigLoader.config')
    def test_format_query(self, mock_config):
        # Tests if a period is appended to the query string if it’s not already there, and it also trims any white space.
        self.assertEqual(format_query("test"), "test.")
        self.assertEqual(format_query("test."), "test.")
        self.assertEqual(format_query("   test   "), "test.")

    @patch('ConfigLoader.config')
    def test_extract_response_statements_from_string(self, mock_config):
        # Tests if the method properly extracts key phrases based on provided patterns.
        mock_config.key_phrases_patterns = MagicMock()
        mock_config.key_phrases_patterns.__dict__ = {'SPECIFICATIONS': 'test'}
        self.assertEqual(extract_response_statements_from_string("SPECIFICATIONS: test"),
                         {'SPECIFICATIONS': 'test', 'FOLLOW_UP_QUESTION': None, 'SUGGESTION': None})
        self.assertEqual(extract_response_statements_from_string("no match"),
                         {'SPECIFICATIONS': None, 'FOLLOW_UP_QUESTION': None, 'SUGGESTION': None})

    @patch('ConfigLoader.config')
    def test_force_suggestion(self, mock_config):
        # Tests if the correct warning message is appended based on the given constraints.
        mock_config.suggestion_name = 'Selection'
        constraints = {
            'specifications': 'spec1,spec2,spec3,spec4,spec5',
            'specifications_threshold': '2',
            'counter': 1,
            'counter_threshold': 2
        }
        expected_result = ("test\n\n"
                           f"DO NOT ASK A FOLLOW UP QUESTIONS. USE THE {mock_config.suggestion_name} TOOL TO MAKE A SUGGESTION NOW.\n"
                           "previously made specifications: spec1,spec2,spec3,spec4,spec5")
        self.assertEqual(force_suggestion("test", constraints), expected_result)

    def test_add_specifications(self):
        # Tests if specifications are appended correctly to the query.
        self.assertEqual(add_specifications("test", "spec1,spec2"),
                         "test\nPreviously made specifications: spec1,spec2.")
        self.assertEqual(add_specifications("test", ""), "test")

    def test_add_comparison_description(self):
        # Tests if comparison descriptions are appended correctly to the query.
        self.assertEqual(add_comparison_description("test", "desc"),
                         "test\nChoose one similar to the following description: desc")
        self.assertEqual(add_comparison_description("test", ""), "test")

    def test_construct_answer(self):
        # Tests if answers are constructed correctly based on whether a suggestion is provided or not.
        result = ("Based on your input I would suggest: \nSuggestion\n\n"
                  "Not your taste? Just tell me more about your wishes!\n\n"
                  "Follow Up")
        self.assertEqual(construct_answer("Suggestion", "Follow Up"), result)
        self.assertEqual(construct_answer("", "Follow Up"), "Follow Up")

    @patch('ConfigLoader.config')
    @patch('utils.string_operations.clean_string')
    def test_extract_category_and_object_of_comparison(self, mock_clean_string, mock_config):
        # Tests if category and object of comparison are extracted correctly from the response string.
        mock_config.selected_pipeline_phrase = 'selected'
        mock_config.object_for_comparison_phrase = 'object'
        mock_clean_string.side_effect = lambda x: x  # return same string
        response = ("category: cat\n"
                    "object for comparison: obj")
        self.assertEqual(extract_category_and_object_of_comparison(response),
                         {'CATEGORY': 'cat', 'OBJECT FOR COMPARISON': 'obj'})
        with self.assertRaises(ValueError):
            # Tests if a ValueError is raised when the response string does not contain valid information.
            extract_category_and_object_of_comparison("invalid input")

    def test_clean_string(self):
        # Tests if the input string is cleaned correctly, allowing only specific characters.
        self.assertEqual(clean_string("test[123]"), "test[123]")
        self.assertEqual(clean_string("test@#$%^&*()_+"), "test()")
