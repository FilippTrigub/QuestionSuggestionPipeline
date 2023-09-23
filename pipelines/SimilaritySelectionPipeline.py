from haystack import Document
from haystack.nodes import OpenAIAnswerGenerator, EmbeddingRetriever, PromptTemplate

from retrievers.InventoryItemStore import InventoryItemStore
from ConfigLoader import config
from base_pipelines.SimpleGenerativeQAPipeline import SimpleGenerativeQAPipeline


class SimilaritySelectionPipeline(SimpleGenerativeQAPipeline):

    def __init__(self, retriever, llm_key):
        """
        This is a pipeline to suggest products based on similarity with a stated product.
        """
        self.retriever = retriever
        prompt_template = PromptTemplate(
            prompt=f"You are an AI recommendation assistant. "
                   f"Your purpose is to present a fitting {config.suggestion_category} to the client. "
                   f"You will be given a list of wines similar to one the client already liked in the context."
                   f"The client might also state wishes in the CLIENT QUERY. "
                   "ONLY CHOOSE FROM THE OPTIONS IN THE CONTEXT. "
                   f"YOU ARE NOT ALLOWED TO SUGGEST A {config.suggestion_category}, WHICH IS NOT IN THE CONTEXT. "
                   "RESPONSE FORMAT: \n"
                   f"{config.leading_phrase} \n"
                   "SUGGESTION: "
                   f"Name: <name of the chosen {config.suggestion_category}> "
                   f"Description: <details about the {config.suggestion_category}>\n"
                   "\n\nCONTEXT:\n"
                   "{context}"
                   "\n\nCLIENT QUERY:\n"
                   "{query}\n"
        )
        self.generator = OpenAIAnswerGenerator(
            prompt_template=prompt_template,
            api_key=llm_key,
            model=config.suggestion_model,
            max_tokens=config.suggestion_max_tokens,
            presence_penalty=config.suggestion_presence_penalty,
            frequency_penalty=config.suggestion_frequency_penalty,
            top_k=config.suggestion_top_k,
            temperature=config.suggestion_temperature
        )
        super().__init__(generator=self.generator,
                         retriever=self.retriever)
