# RAG System with FastAPI, LangChain, and OpenAI

## Overview
This project implements a **Retrieval-Augmented Generation (RAG)** system using **FastAPI**, **LangChain**, and **OpenAI**. It includes features such as:
- **User Authentication** (JWT-based login/signup)
- **Multiple Conversations** (User-specific chat history)
- **File Uploads** (For document-based retrieval)
- **RAG-based Question Answering**
- **Database Storage** (Using SQLite for users, chats, and documents)
- **Vector Database** (Using ChromaDB for retrieval)

## Tech Stack
- **Backend**: FastAPI, LangChain, OpenAI
- **Authentication**: JWT (JSON Web Token)
- **Database**: SQLite
- **Vector Database**: ChromaDB
- **LLM**: OpenAI GPT


### Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/rag-fastapi.git
   cd rag-fastapi
