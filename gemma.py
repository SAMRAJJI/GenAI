import os 
import streamlit as st
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv

load_dotenv()

groq_api = os.getenv("groq_api_key")
os.environ['GOOGLE_API_KEY'] = os.getenv("google_api_key")
st.title("gemma model question")
llm = ChatGroq(groq_api_key = groq_api, model="llama-3.1-8b-instant")

prompt= ChatPromptTemplate.from_template("""
    answer the question based on the provided context only please provide the most 
    accurate response based on the question <context>
    {context}
    <context>
    question:{input}
    """)

def vector_embeddings():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        task_type="RETRIEVAL_DOCUMENT",
        google_api_key=os.getenv("google_api_key"))
        st.session_state.loader = PyPDFDirectoryLoader("./census")
        st.session_state.docs=st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap = 200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
        
prompt1 = st.text_input("what you want to ask from the documents")

if st.button("create"):
    vector_embeddings()
    st.write("vectors are stored in DB and ready")
    
import time

if prompt1:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    start = time.process_time()
    res = retrieval_chain.invoke({'input': prompt1})
    st.write(res['answer'])