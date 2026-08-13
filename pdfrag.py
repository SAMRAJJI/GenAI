# import streamlit as st
# from PyPDF2 import PdfReader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# import os
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import google.generativeai as genai
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import ChatGoogleGenerativeAI
# # from langchain.chains.question_answering import load_qa_chain
# from langchain_classic.chains import RetrievalQA
# from langchain_core.prompts import PromptTemplate
# from dotenv import load_dotenv


# load_dotenv()

# genai.configure(api_key=os.getenv("google_api_key"))

# def get_pdf(pdf_doc):
#     text = ""
#     for pdf in pdf_doc:
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader:
#             text+= page.extract_text()
#     return text

# def get_text_chunks(text):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 1000)
#     chunks = text_splitter.split_text(text)
#     return chunks

# def get_vector_store(text_chunks):
#     embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
#     vectore_store = FAISS.from_texts(text_chunks, embedding=embeddings)
#     vectore_store.save_local("faiss_index")

# def get_conversation_chain():
#     prompt_template = """
#     Answer the question as detailed as possible from the provided context, make sure to provide answer
#     if answer is not avail just say , "answer is not available in the content", don't provide false info
#     Context:\n {context}\n
#     Question: \n {question}\n
    
#     Answer:
#     """
#     model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature = 0.3)
#     prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
#     chain = RetrievalQA(model, chain_type="stuff", prompt =prompt)
#     return chain

# def user_input(user_question):
#     embeddings = GoogleGenerativeAIEmbeddings(model= "models/embedding-001")
#     new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
#     docs = new_db.similarity_search(user_question)
#     chain = get_conversation_chain()
#     res = chain({"input_documents":docs, 
#      "question": user_question}, return_only_outputs=True)
    
#     print(res)
#     st.write("reply: ", res["output_text"])


# def main():
#     st.set_page_config("chat with multipdf RAG Application")
#     st.header("chat with multiple PDF using Gemini😎")
    
#     user_question = st.text_input("Ask a Question from the PDF Files")
#     if user_question:
#         user_input(user_question)
        
#     with st.sidebar:
#         st.title("Menu: ")
#         pdf_doc = st.file_uploader("upload the pdf file")
#         if st.button("submit"):
#             with st.spinner("processing---"):
#                 raw = get_pdf(pdf_doc)
#                 text_chuck =get_text_chunks(raw)
#                 get_vector_store(text_chuck)
#                 st.success("Done")
                
                
# if __name__ == "__main__":
#     main()
import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate
# from langchain.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

GOOGLE_API_KEY = os.getenv("google_api_key")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY is not set in your .env file.")
    st.stop()


# --------------------------------------------------
# PDF TEXT EXTRACTION
# --------------------------------------------------

def get_pdf_text(pdf_docs):
    text = ""

    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        except Exception as e:
            st.error(f"Could not read '{getattr(pdf, 'name', 'file')}': {e}")

    return text


# --------------------------------------------------
# TEXT CHUNKING
# --------------------------------------------------

def get_text_chunks(text):
    # Chunk size kept well under the embedding model's input token limit
    # (large chunks risk silent truncation or embedding errors).
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_text(text)

    return chunks


# --------------------------------------------------
# EMBEDDINGS (cached so it's created once per session)
# --------------------------------------------------

@st.cache_resource
def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )


# --------------------------------------------------
# CREATE FAISS VECTOR STORE
# --------------------------------------------------

def get_vector_store(text_chunks):
    embeddings = get_embeddings()

    vector_store = FAISS.from_texts(
        text_chunks,
        embedding=embeddings
    )

    vector_store.save_local("faiss_index")


# --------------------------------------------------
# CREATE RAG CHAIN (cached so it's built once, not on every question)
# --------------------------------------------------

@st.cache_resource
def get_conversation_chain():

    prompt_template = """
Answer the question using ONLY the provided context.

If the answer is not available in the context, say:
"Answer is not available in the provided documents."

Do not use outside knowledge.
Do not make up information.

Context:
{context}

Question:
{input}

Answer:
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "input"]
    )

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=GOOGLE_API_KEY,
    )

    document_chain = create_stuff_documents_chain(
        llm=model,
        prompt=prompt
    )

    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    return retrieval_chain


# --------------------------------------------------
# USER QUESTION
# --------------------------------------------------

def user_input(user_question):

    if not os.path.exists("faiss_index"):
        st.warning("Please upload and process PDF files first.")
        return

    try:
        chain = get_conversation_chain()
        response = chain.invoke({
            "input": user_question
        })
        answer = response["answer"]

        st.write("### Answer")
        st.write(answer)

    except Exception as e:
        st.error(f"Something went wrong while answering: {e}")


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

def main():

    st.set_page_config(
        page_title="Chat with Multiple PDFs",
        page_icon="📚"
    )

    st.header("📚 Chat with Multiple PDFs using Gemini")

    user_question = st.text_input(
        "Ask a question from the PDF files"
    )

    if user_question:
        user_input(user_question)

    with st.sidebar:

        st.title("Menu")

        pdf_docs = st.file_uploader(
            "Upload your PDF files",
            type=["pdf"],
            accept_multiple_files=True
        )

        if st.button("Submit & Process"):

            if not pdf_docs:
                st.warning("Please upload at least one PDF.")
            else:
                with st.spinner("Processing PDFs..."):

                    # Extract text
                    raw_text = get_pdf_text(pdf_docs)

                    if not raw_text.strip():
                        st.error("Could not extract text from the PDFs.")
                    else:
                        # Split text
                        text_chunks = get_text_chunks(raw_text)

                        # Create vector database
                        try:
                            get_vector_store(text_chunks)
                            # Clear cached chain so it rebuilds against the new index
                            get_conversation_chain.clear()
                            st.success("PDFs processed successfully!")
                        except Exception as e:
                            st.error(f"Failed to build the vector store: {e}")


if __name__ == "__main__":
    main()