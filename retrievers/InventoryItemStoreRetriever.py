from typing import Optional

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

    def find_document_by_title(self, query_title: str, max_difference: int = 2) -> Optional[Document]:
        """
        Method finds the document, whose title is similar to the query_title.
        Similar means, it's a subset of the document title at least half as long
        and differs in at most max_difference characters.
        :param query_title: title of product for which the Document in the document store is searched
        :param max_difference: maximum difference in characters
        :return: Document with the similar title or None
        """

        def get_character_defference(s1: str, s2: str) -> int:
            difference = 0
            if len(s1) > len(s2):
                s1, s2 = s2, s1

            for index in range(len(s1)):
                if s1[index] != s2[index]:
                    difference += 1
            return difference

        for doc in self.inventory_store.get_all_documents():
            if (len(query_title) >= len(doc.meta['title']) // 2
                    and (query_title in doc.meta['title']
                         or get_character_defference(doc.meta['title'], query_title) <= max_difference)):
                return doc

        return None
