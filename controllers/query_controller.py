from fastapi import Query
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from settings import settings

def query_route(message: str = Query(...), conversation_id: str = Query(...)):
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_KEY)
    vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings,collection_name=conversation_id)

    # Create retriever and QA chain
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=settings.OPENAI_KEY),
        retriever=retriever
    )


    response = qa_chain.invoke({"query": message})
    print(response)
    return {
        "message": message,
        "conversation_id": conversation_id,
        "response":response 
    }
