from haystack.document_stores import FAISSDocumentStore

from ConfigLoader import config
from utils.SingletonMeta import SingletonMeta


class InventoryItemStore(metaclass=SingletonMeta):

    def __new__(cls, *args, **kwargs):
        # Load the saved index into a new DocumentStore instance if it exists, else create a new instance
        # todo: PermissionError stops deletion of store after attempt to load it >> fix that

        document_store_is_new = True
        try:
            document_store = FAISSDocumentStore.load(index_path=config.faiss_index_path,
                                                     config_path=config.faiss_config_path)
            document_store_is_new = False
        except (TypeError, ValueError):
            # todo clean_directory(document_store_directory)
            # init DocumentStore
            document_store = FAISSDocumentStore(
                sql_url=config.default_faiss_sql_url,
                faiss_index_factory_str=config.default_faiss_index_factory_str,
                embedding_dim=config.default_embedding_dim,
                return_embedding=config.default_return_embedding,
                similarity=config.default_similarity
            )
            # Save the DocumentStore
            document_store.save(index_path=config.faiss_index_path, config_path=config.faiss_config_path)

        return document_store, document_store_is_new
