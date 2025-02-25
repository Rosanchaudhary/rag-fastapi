import os
import pypdf
from fastapi import UploadFile, File, Form,HTTPException
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from settings import settings


UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)  # Ensure the folder exists

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text

async def upload_file(file: UploadFile = File(...), conversation_id: str = Form(...)):
    file_location = UPLOAD_FOLDER / file.filename
    try:
        with file_location.open("wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File saving failed: {str(e)}") 
    
    if file.content_type == "application/pdf":
        extracted_text = extract_text_from_pdf(str(file_location))
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(extracted_text)
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_KEY)
        Chroma.from_texts(chunks, embedding=embeddings, persist_directory="./chroma_db",collection_name=conversation_id)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "conversation_id": conversation_id,
        "file_path": str(file_location)
    }

