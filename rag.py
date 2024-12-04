from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import TextEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import os


class PDFChatbot():
    """
    A class for interacting with PDF documents to answer questions using a RAG-based approach.
    """
    def __init__(self):
        """
        Initializes the PDFChatbot with a language model, text splitter, prompt template, and embedding service.
        """
        # Language model for answering questions
        self.language_model = ChatOllama(
            model="llama3.1",
            base_url="http://localhost:11434",
            temperature=0.7
        )
        
        # Text splitter to handle document chunking
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        
        # Prompt template for generating queries
        self.prompt_template = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for answering questions. Use the following context to answer the question. 
            If you do not know the answer, simply say you don't know. [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )
        
        # Embedding service for vectorization
        self.embedding_service = TextEmbedEmbeddings(
            model="sentence-transformers/all-MiniLM-L12-v2",
            api_key="TextEmbed"
        )
        
        # Set up persistent directory for Chroma
        self.persist_directory = "chroma_db"
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)
            
        # Initialize Chroma client
        self.chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Initialize placeholders for vector store, retriever, and query chain
        self.vector_store = None
        self.retriever = None
        self.query_chain = None

    def load_and_index_pdf(self, pdf_file_path: str):
        """
        Loads a PDF file, splits it into chunks, creates a vector store, and sets up the query chain.
        """
        documents = PyPDFLoader(file_path=pdf_file_path).load()
        chunks = self.text_splitter.split_documents(documents)
        filtered_chunks = filter_complex_metadata(chunks)

        # Initialize Chroma with persistent directory
        self.vector_store = Chroma.from_documents(
            documents=filtered_chunks,
            embedding=self.embedding_service,
            persist_directory=self.persist_directory,
            client=self.chroma_client
        )
        
        # Persist the vector store
        self.vector_store.persist()
        
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
        )

        self.query_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt_template
            | self.language_model
            | StrOutputParser()
        )

    def answer_question(self, query: str):
        """
        Answers a question using the query chain if a PDF has been ingested.
        """
        if not self.query_chain:
            return "Please, add a PDF document first."

        return self.query_chain.invoke(query)

    def reset(self):
        """
        Clears the vector store, retriever, and query chain.
        """
        if self.vector_store is not None:
            self.vector_store.delete_collection()
            self.vector_store = None
        self.retriever = None
        self.query_chain = None