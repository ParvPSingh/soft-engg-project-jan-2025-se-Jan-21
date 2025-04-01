from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

from langchain.chains import create_history_aware_retriever
from langchain_together import ChatTogether, TogetherEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain.chains import LLMChain, MultiPromptChain
from langchain.chains.router import MultiPromptChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_together import TogetherEmbeddings
from langchain_together import ChatTogether, TogetherEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents  import create_stuff_documents_chain
from langchain_community.vectorstores import Qdrant
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema import AIMessage

# Configure logging


# This will be set by main.py
vector_store = None

# Initialize LLM and retriever once the vector_store is available
def initialize_chatbot():
    global retriever, history_aware_retriever, document_chain, rag_chain, conversational_rag_chain
    
    if vector_store is None:
        raise RuntimeError("Vector store not initialized")
    
    retriever = vector_store.as_retriever(search_kwargs={"k":2})
    
    llm = ChatTogether(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", temperature=0, max_tokens=400)
    
    context_adding_prompt = ChatPromptTemplate.from_messages([
    ("system", """"
You are an AI assistant for the IITM BS Degree program. Keep responses under 300 tokens.

1. Off-Topic Questions: 
   Respond: "I only help with IITM BS Degree program content. Please ask about courses or policies."

2. Course Content:
   - Give direct answers from context
   - Use bullet points
   - Include formulas exactly as shown
   - No examples unless requested

3. Programming Help:
   - Never give complete solutions
   - Provide 2-3 hints
   - Show minimal code snippets
   - Guide through questions

If information isn't in context: "Please check IITM's official resources."

Context:\n\n{context}
\n\n{context}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", """
    1. You are AutoBot, an assistant for the IITM BS Degree program. Always identify yourself as AutoBot and do not assume any other role. Maintain a professional, clear, and concise tone in all your responses.
         """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    history_aware_retriever = create_history_aware_retriever(
        llm=llm, 
        retriever=retriever, 
        prompt=qa_prompt
    )
    
    document_chain = create_stuff_documents_chain(llm, context_adding_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, document_chain)
    
    # Store conversation history
    store = {}
    
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]
    
    # Create the conversational RAG chain with message history
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    

# Define function to retrieve context
def retrieve_context_student(user_query):
    # Make sure chatbot components are initialized
    if 'conversational_rag_chain' not in globals():
        initialize_chatbot()
    
    # Check if it's a simple greeting
    simple_greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    
    if user_query.lower().strip() in simple_greetings or user_query.lower().strip().rstrip("!") in simple_greetings:
        # Return empty context for simple greetings
        return [SystemMessage(content="")]
    
    # For normal queries, use the retriever
    docs = vector_store.similarity_search(user_query, k=2)
    content = "\n".join([doc.page_content for doc in docs])
    return [SystemMessage(content=content)]

# Define function to handle chatbot calls
def call_autobot_student(user_query, retrieved_context):
    # Make sure chatbot components are initialized
    if 'conversational_rag_chain' not in globals():
        initialize_chatbot()
    
    # Check if it's a simple greeting
    simple_greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    
    if user_query.lower().strip() in simple_greetings or user_query.lower().strip().rstrip("!") in simple_greetings:
        # Return a simple greeting response
        return AIMessage(content="Hello! I'm Autobot, your IITM BS degree virtual assistant. I'm here to help you with understanding course concepts and finding information in your course materials. How can I assist you today?")
    
    # For normal queries, use the conversational RAG chain
    session_id = "default_user"  # In a real app, you would get a unique session ID for each user
    response = conversational_rag_chain.invoke(
        {"input": user_query},
        config={"configurable": {"session_id": session_id}}
    )
    
    # Convert the response to an AIMessage for compatibility with existing code
    if isinstance(response, dict) and "answer" in response:
        return AIMessage(content=response["answer"])
    else:
        return AIMessage(content=str(response))
    

    
