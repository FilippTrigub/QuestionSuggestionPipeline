# data path
data_path = '<YOUR PATH>'
dev_data_path = '<YOUR PATH>'

# document store settings
document_store_directory = 'document_store'
default_faiss_sql_url = 'sqlite:///document_store/faiss_document_store.db'
faiss_index_path = 'document_store/faiss_document_index.faiss'
faiss_config_path = 'document_store/faiss_document_config.json'
default_faiss_index_factory_str = "Flat"
default_embedding_dim = 768
default_return_embedding = False
default_similarity = "dot_product"

# Bot Settings
suggestion_category = '<YOUR_ITEM>'
all_useful_attributes = ['title', 'description', 'price', 'categoryName', 'address', 'totalScore', 'permanentlyClosed',
                         'temporarilyClosed', 'categories', 'reviewsDistribution',
                         'reviewsCount', 'reviewContext', 'reviewDetailedRating', 'text']
criteria_for_selection = ['title', 'description', 'category', 'price']

# Bot modes
bot_modes = ['quick', 'advanced']
specifications_threshold_modes = {bot_modes[0]: '2', bot_modes[1]: '6'}

# Bot key phrases
leading_phrase = 'RESPONSE:'
specifications_designator = "Specifications: "
specifications_designator_search_pattern = r'Specifications: (.*)'

# Follow-up Question tool settings
follow_up_question_tool_name = "Question"
tool_generative_model = 'gpt-3.5-turbo'
follow_up_question_model_settings = {
    'max_tokens': 300,
    'presence_penalty': 0.1,
    'frequency_penalty': 0.1,
    'top_k': 1,
    'temperature': 0.6
}

# Inventory Item Selection tool settings
suggestion_name = "Selection"
suggestion_retriever_embeddings_model = 'sentence-transformers/all-mpnet-base-v2'
suggestion_model = "text-davinci-003"
suggestion_max_tokens = 300
suggestion_presence_penalty = 0.1
suggestion_frequency_penalty = 0.1
suggestion_top_k = 1
suggestion_temperature = 0.1

# response patterns
specifications_phrase = 'SPECIFICATIONS'
follow_up_question_phrase = 'FOLLOW UP QUESTION'
suggestion_phrase = 'SUGGESTION'
key_phrases_patterns = {
    specifications_phrase: r'SPECIFICATIONS:\s*(.*?)\s*(?:FOLLOW UP QUESTION:|RESPONSE:|$)',
    follow_up_question_phrase: r'FOLLOW UP QUESTION:\s*(.*?)\s*(?:TOOL:|Thought:|$)',
    suggestion_phrase: r'SUGGESTION:\s*(.*?)\s*(?:TOOL:|Thought:|$)'
}
