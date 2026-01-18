import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file")

PDF_PATH = "esi_handbook.pdf"
DB_PATH = "./chroma_db"

def ingest():
    print(f"📄 Loading {PDF_PATH}...")
    if not os.path.exists(PDF_PATH):
        print(f"Error: {PDF_PATH} not found. Please add the PDF to this folder.")
        return

    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()
    print(f"   Found {len(pages)} pages.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(pages)
    print(f"   Created {len(chunks)} knowledge chunks.")


    print("Vectorizing and storing (this may take a moment)...")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    print(f"Success! Knowledge Base saved to {DB_PATH}")

if __name__ == "__main__":
    ingest()