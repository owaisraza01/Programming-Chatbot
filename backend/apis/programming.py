from flask_restx import Namespace, Resource
from flask import Flask, request, jsonify, make_response
import apis.config
import os
from pymongo import MongoClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

#Namespace Configuration
api = Namespace('programming', description='this is a chatbot for information regarding programming languages')
os.environ["OPENAI_API_KEY"] = apis.config.open_ai_api_key
MONGODB_ATLAS_CLUSTER_URI = apis.config.mongo_uri
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

#MongoDb Credantials
DB_NAME = "owais"
COLLECTION_NAME = "programmingrag"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

# Load the DOCUMENT
def process_and_store_documents():
    loader = UnstructuredFileLoader("apis/docs/programming.docx")
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    docs = text_splitter.split_documents(data)
    # Set manual URL for each document
    manual_url = "https://chatgpt.com/"
    for doc in docs:
        doc.metadata['source'] = manual_url  # Set manual URL for source
    print("Docs after splitting",docs[0])

     # insert the documents in MongoDB Atlas with their embedding
    vector_search = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        collection=MONGODB_COLLECTION,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

# process_and_store_documents()

vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    MONGODB_ATLAS_CLUSTER_URI,
    DB_NAME + "." + COLLECTION_NAME,
    OpenAIEmbeddings(disallowed_special=()),
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

qa_retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5},
)

prompt_template = """
Use the following pieces of context to answer the question at the end by summarizing the context. If the context does not contain sufficient information to answer the question, just say "I don't know".

{context}

Question: {question}
Answer: """
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=qa_retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
)

#Creating API
@api.route('/programmingchatbot')
class ProgrammingChatbot(Resource):
    def post(self):
        data = request.get_json()
        query = data.get('query')
        results = qa({"query": query})

        print("Result", results['source_documents'])

        # Check if any documents were found
        if not results['source_documents']:
            return make_response(jsonify({"answer": "No similar documents found", "query": query, "url": "No URL found"}), 404)
        
        # If there are documents, access the first one
        document_url = results['source_documents'][0].metadata.get('source', "No URL found")

        # Return the response
        return make_response(jsonify({"answer": results['result'], "query": query, "url": document_url}), 200)
