import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.documents import Document
from typing import List, TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
load_dotenv()

model = init_chat_model('gemini-2.5-flash', model_provider="google_genai")
file_path='./app/sample.pdf'
latex_path='./app/resume.tex'
# Load sample document for retrieval
loader = TextLoader(latex_path,encoding='utf-8')
datas = loader.load()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
chroma_db = Chroma.from_documents(datas, embeddings, persist_directory="./rag")
retriever = chroma_db.as_retriever()

rag = f"""
As a rag i want you to use the pdf handed to you from the chromadb vector db and answer user's queries with your
own response i also want u to answer questions related to technologies in the pdf anything else that is not mentionned 
in the pdf or isn't a programming technology (Django , Swing, Discord.py ,etc....) .You're not allowed to answer it . 
The pdf is a resume. your response can be detailed to explain to the user who is the person, refer to the person you're talking about s as achraf chahin
and if you're ask you who u are you're an a achraf chahin's assistant
"""
# nlp_prompt_template = ChatPromptTemplate.from_messages([
#     ('system', rag),
#     ('user', "Question: {question}")
# ])


@tool
def retrieve(query: str):
    """This is a function will retrieve from a pdf and use semantic search to give you all the results needed"""
    context = retriever.invoke(query)
    documents = "\n\n".join(doc.page_content for doc in context)
    return documents
checkpointer = InMemorySaver()
rag_agent = create_agent(model, tools=[retrieve],system_prompt=rag, name="RAG_agent",checkpointer=checkpointer)
import random
def ask_rag_agent(question: str) -> str:
    """Run the RAG agent and return the final answer."""
    # prompt = nlp_prompt_template.invoke({'question': question})
    systemprompt = """As a rag i want you to use the pdf handed to you from the chromadb vector db and answer user's queries with your
own response i also want u to answer questions related to technologies in the pdf anything else that is not mentionned 
in the pdf or isn't a programming technology (Django , Swing, Discord.py ,etc....) .You're not allowed to answer it . 
The pdf is a resume. your response can be detailed to explain to the user who is the person
"""
    result = rag_agent.invoke({"messages":[{'role':'user','content':question}]},config={'configurable':{'thread_id':random.randint(1,100)}})
  
        
    return result["messages"][-1].content
    
