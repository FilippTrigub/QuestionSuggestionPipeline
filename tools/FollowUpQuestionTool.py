from haystack.nodes import PromptTemplate

from default_config import suggestion_category, follow_up_question_tool_name, leading_phrase, tool_generative_model, \
    criteria_for_selection, follow_up_question_model_settings
from tool_pipelines.SimpleGenerativePromptNode import SimpleGenerativePromptNode


class FollowUpQuestionPromptNode(SimpleGenerativePromptNode):
    NAME = follow_up_question_tool_name
    DESCRIPTION = "This tool extracts the specifications made by the user and formulates a follow up question."

    def __init__(self, llm_key):
        """

        """
        prompt_template = PromptTemplate(
            prompt=f"You are an AI guide. "
                   f"You must figure out, what kind of {suggestion_category} the client is looking for. "
                   "DO ONLY USE INFORMATION PROVIDED BY THE CLIENT. "
                   f"Inquire the client to specify his or her wishes regarding the {suggestion_category}. "
                   f"You can ask for input regarding the following criteria: {', '.join(criteria_for_selection)}. \n"
                   "Summarize the clients wishes taken from your memory and the client inputs each time you answer the client. "
                   "RESPONSE FORMAT: \n"
                   f"{leading_phrase} \n"
                   "SPECIFICATIONS: <all previously made specifications separated by commas>\n"
                   "FOLLOW UP QUESTION: <follow up question or suggestion>\n"
                   "EXAMPLES:\n"
                   "1:\n"
                   "INPUT: \n"
                   f"I want a nice and cozy {suggestion_category} with an outdoor kitchen.\n"
                   f"{leading_phrase}\n"
                   "SPECIFICATIONS: description: nice and cozy with outdoor kitchen. \n"
                   "FOLLOW UP QUESTION: That's a wonderful choice! Which cuisine would you prefer? \n"
                   "2:\n"
                   "INPUT: \n"
                   "Vietnamese cuisine! \n"
                   f"{leading_phrase}\n"
                   "SPECIFICATIONS: cuisine: Vietnamese \n"
                   "FOLLOW UP QUESTION: Perfect! Would you like to sit outside or inside? \n"
                   "INPUT: \n"
                   "Outside\nPreviously made specifications: cuisine: Vietnamese \n"
                   f"{leading_phrase}\n"
                   "SPECIFICATIONS: cuisine: vietnamese, seating: outside \n"
                   "FOLLOW UP QUESTION: Perfect! Which price range would for you? \n"
                   "\n\nCLIENT QUERY:\n"
                   "{query}\n"
        )

        super().__init__(default_prompt_template=prompt_template,
                         model_name_or_path=tool_generative_model,
                         api_key=llm_key,
                         model_kwargs=follow_up_question_model_settings
                         )
