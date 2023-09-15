from haystack import Document
from haystack.nodes import OpenAIAnswerGenerator, EmbeddingRetriever, PromptTemplate

from document_stores.InventoryItemStore import InventoryItemStore
from ConfigLoader import config
from tool_pipelines.SimpleGenerativeQAPipeline import SimpleGenerativeQAPipeline


class InventoryItemSelectionPipeline(SimpleGenerativeQAPipeline):
    NAME = config.suggestion_name
    DESCRIPTION = f"This tool determines the most fitting {config.suggestion_category} based on its description."

    def __init__(self, data_list_of_dict, llm_key):
        """
        Sets the pipeline for the model. The pipeline consists of a retriever and a generator.
        The retriever is used to find the most relevant messages to the question.
        The generator is used to generate an answer to the question based on the retrieved messages.
        The document store is used to store the messages.
        """
        self.wine_store, document_store_is_new = InventoryItemStore()
        self.retriever = EmbeddingRetriever(embedding_model=config.suggestion_retriever_embeddings_model,
                                            document_store=self.wine_store,
                                            api_key=llm_key)
        self.write_data_to_document_store_and_update_embeddings(data_list_of_dict, document_store_is_new)
        prompt_template = PromptTemplate(
            prompt=f"You are an AI recommendation assistant. "
                   f"Your purpose is to present a fitting {config.suggestion_category} to the client. "
                   f"You will be given a description of a desired {config.suggestion_category} and fitting options in the context. "
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

    def write_data_to_document_store_and_update_embeddings(self, data_list_of_dict: list, document_store_is_new: bool):
        if document_store_is_new:
            if 'meta' in data_list_of_dict[0].keys():
                documents = [Document(content=row['content'], meta=row['meta']) for row in data_list_of_dict]
            else:
                documents = [Document(content=row['content']) for row in data_list_of_dict]
            self.wine_store.write_documents(documents)
            print('\nData written to document store.\n')
        self.wine_store.update_embeddings(self.retriever)
        print('Retriever set up.')
