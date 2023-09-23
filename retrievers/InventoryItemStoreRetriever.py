from haystack import Document
from haystack.nodes import EmbeddingRetriever

from ConfigLoader import config
from retrievers.InventoryItemStore import InventoryItemStore


class InventoryItemStoreRetriever(EmbeddingRetriever):

    def __init__(self, data_list_of_dicts: list, llm_key: str):
        self.inventory_store, self.document_store_is_new = InventoryItemStore()

        super().__init__(embedding_model=config.suggestion_retriever_embeddings_model,
                         document_store=self.inventory_store,
                         api_key=llm_key,
                         top_k=config.suggestion_retriever_top_k)
        self.write_data_to_document_store_and_update_embeddings(data_list_of_dicts, self.document_store_is_new)

    def write_data_to_document_store_and_update_embeddings(self, data_list_of_dict: list, document_store_is_new: bool):
        if document_store_is_new:
            if 'meta' in data_list_of_dict[0].keys():
                documents = [Document(content=row['content'], meta=row['meta']) for row in data_list_of_dict]
            else:
                documents = [Document(content=row['content']) for row in data_list_of_dict]
            self.inventory_store.write_documents(documents)
            print('\nData written to document store.\n')
        self.inventory_store.update_embeddings(self)
        self.inventory_store.save(index_path=config.faiss_index_path, config_path=config.faiss_config_path)

        print('Retriever set up.')
