from haystack.nodes import PromptTemplate

from ConfigLoader import config
from base_pipelines.SimpleGenerativePromptNode import SimpleGenerativePromptNode
from utils.string_operations import extract_category_and_object_of_comparison


class MinimalDecisionPromptNode(SimpleGenerativePromptNode):

    def __init__(self, llm_key):
        prompt_template = PromptTemplate(
            prompt=f"You are an AI tasked with categorizing {config.suggestion_category}-related requests. "
                   f"Your goal is to determine whether each input falls into the following categories: "
                   "\nCATEGORIES:\n"
                   + '\n'.join([key + ': ' + value
                                for key, value in config.pipeline_selection_pipelines.__dict__.items()]) +
                   "Never provide a response without referring to the input query. "
                   "DO ONLY USE INFORMATION PROVIDED BY THE CLIENT. "
                   "YOU MUST FOLLOW THE RESPONSE FORMAT: "
                   "\nRESPONSE FORMAT:\n"
                   "< explanations >;\n"
                   f"{config.selected_pipeline_phrase}: < choice of category >;\n"
                   f"{config.object_for_comparison_phrase}: <object for comparison or None>;"
                   f"\n\nEXAMPLES:\n"
                   f"1:\n"
                   f"Query: Give me a similar wine to one called Estampa 2011 Estate Viognier-Chardonnay (Colchagua Valley). \n"
                   f"Response: The correct choice is {list(config.pipeline_selection_pipelines.__dict__.keys())[0]}, "
                   f"because the user seems to want a wine similar to one called Estampa 2011 Estate Viognier-Chardonnay (Colchagua Valley). \n"
                   f"{config.selected_pipeline_phrase}: {list(config.pipeline_selection_pipelines.__dict__.keys())[0]};\n"
                   f"{config.object_for_comparison_phrase}: Estampa 2011 Estate Viognier-Chardonnay (Colchagua Valley);\n"
                   f"2:\n"
                   f"Query: I want a dry italian wine."
                   f"Response: The correct choice is {list(config.pipeline_selection_pipelines.__dict__.keys())[1]}, "
                   f"because the use is indicating a preference based on attributes. \n"
                   f"{config.selected_pipeline_phrase}: {list(config.pipeline_selection_pipelines.__dict__.keys())[1]};\n"
                   f"{config.object_for_comparison_phrase}: None;\n"
                   "\n\nINPUT QUERY:\n"
                   "{query}\n"
        )

        super().__init__(default_prompt_template=prompt_template,
                         model_name_or_path=config.pipeline_selection_generative_model,
                         api_key=llm_key,
                         model_kwargs=config.pipeline_selection_model_settings.__dict__
                         )

    @staticmethod
    def get_results_from_output(output):
        return extract_category_and_object_of_comparison(output[0]['results'][0])
