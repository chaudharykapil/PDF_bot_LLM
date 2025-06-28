from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv
load_dotenv()
class PDFChatbot:
    def __init__(self):
        self.embeddings = None
        self.db = None
        self.qa = None

    def setEmbedding(self):
        # This line of code is initializing an instance of the `GoogleGenerativeAIEmbeddings` class
        # and assigning it to the `self.embeddings` attribute of the `PDFChatbot` class.
        if not self.embeddings:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                model="models/embedding-001"
            )
        # The line `self.db = Chroma("vectors", persist_directory="./vector_db",
        # embedding_function=self.embeddings)` in the `PDFChatbot` class is creating an instance of
        # the `Chroma` class and assigning it to the `self.db` attribute of the `PDFChatbot` class.
        if not self.db:
            self.db = Chroma("vectors",persist_directory="./vector_db",embedding_function=self.embeddings)
    def loadPDF(self,pdfpath):
        # The code snippet `pdfloader = PyMuPDFLoader(pdfpath)` is creating an instance of the
        # `PyMuPDFLoader` class, which is used for loading a PDF document located at the specified
        # `pdfpath`.
        pdfloader = PyMuPDFLoader(pdfpath)
        docs = pdfloader.load_and_split(text_splitter=RecursiveCharacterTextSplitter())

        
        # The code snippet `self.db.reset_collection()` is resetting the collection of documents
        # stored in the `Chroma` instance's database. This means that any existing documents in the
        # collection will be removed.
        self.db.reset_collection()
        self.db.add_documents(docs)
        self.__build_retriver_chain()

    def __build_retriver_chain(self):
        # The line `self.qa =
        # RetrievalQA.from_chain_type(llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",
        # convert_system_message_to_human=True), retriever=self.db.as_retriever())` in the
        # `PDFChatbot` class is creating an instance of the `RetrievalQA` class by specifying two
        # components:
        self.qa = RetrievalQA.from_chain_type(
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",convert_system_message_to_human=True),
            retriever = self.db.as_retriever()
        )

    def ask(self,query):
        answer = self.qa.invoke({"query":query})
        print(answer)
        return answer

