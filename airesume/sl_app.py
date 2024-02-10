import streamlit as st
import openai
import os
import tempfile
from langchain.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.llms import GPT4All
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from mpl_toolkits import mplot3d
from gpt4all import Embed4All
from langchain.embeddings.openai import OpenAIEmbeddings


with st.sidebar:
    api_key = st.text_input("API Key", key="file_qa_api_key", type="password")
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 CV Screener")
# uploaded_file = st.file_uploader("Upload an article")
uploaded_files = st.file_uploader(label="Upload PDF files", type=["pdf"], accept_multiple_files=True)

question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_files,
)

if uploaded_files and question and not api_key:
    st.info("Please add your API key to continue.")


if uploaded_files and question and api_key:

    openai.api_key = api_key
    
    ###
    data = []
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())
        loader = PyPDFLoader(temp_filepath)
        data.extend(loader.load())
    ###

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1500, chunk_overlap = 100)
    all_splits = text_splitter.split_documents(data)
    
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(openai_api_key=api_key))

    ###
    # If you have a beefy computer you can download and run gpt4all locally
# local_path = (os.path.join(os.getcwd(), "models/wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin"))
# llm = GPT4All(model=local_path, verbose=True)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)

    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationBufferMemory

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa_chain = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)
    
    # instructions = "Please answer the following questions about the candidate. Your answers should be bullet points."
    instructions = ""  
    ans1 = qa_chain({"question": instructions+question})

    st.write("### Answer")
    st.write(ans1["answer"])
