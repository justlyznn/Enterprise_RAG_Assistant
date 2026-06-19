import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class RAGPipeline:
    def __init__(self):
        # Setup embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        
        # Setup vector store connection
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            raise ValueError("DATABASE_URL is not set")
            
        self.vector_store = PGVector(
            embedding_function=self.embeddings,
            collection_name="customer_intelligence_kb_multi",
            connection_string=db_url
        )
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        
        # Setup LLM
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is not set")
            
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile", # updated from decommissioned llama3-8b-8192
            temperature=0.2,
            api_key=groq_api_key,
            max_tokens=1024,
        )
        
        # Setup prompt
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful customer service assistant. 
            Use the following pieces of retrieved context to answer the user's question. 
            If you don't know the answer, just say that you don't know. Keep the answer concise.

            Context: {context}

            Question: {question}

            Answer:"""
        )
        
        # Setup Chain
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def answer_question(self, question: str) -> str:
        return self.chain.invoke(question)

# Singleton instance
rag_pipeline = None

def get_rag_pipeline():
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline
