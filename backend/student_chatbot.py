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
    
    llm = ChatTogether(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", temperature=0, max_tokens=300)
    
    context_adding_prompt = ChatPromptTemplate.from_messages([
        ("system", """"
  You are an AI assistant for the IITM BS Degree program.  

1. **Answer Directly for Concept Explanations & Course Queries**  
   - If a student asks about **grading, policies, deadlines, or concept explanations**, give a clear and direct answer.  
   - **Example:**  
     - **Student:** "What is Newton’s Second Law?"  
     - **AI:** "Newton's Second Law states that Force = Mass X Acceleration (F = ma)."  

2. **Use the Socratic Method for MCQs from Graded Assignments**  
   - If the question is a multiple-choice from a graded assignment, **do not give the direct answer**.  
   - Instead, provide **hints, leading questions, or step-by-step reasoning**.  
   - **Example:**  
     - **Student:** "What is the derivative of sin(x)?" (MCQ from an assignment)  
     - **AI:** "Think about how the sine function behaves. What happens to its slope at different points?"  

3. **Use Context When Available**  
   - If the question can be answered using the provided context, **use it to give a clear and direct answer**.  
   - If the answer **is not in the context**, politely say:  
     - *"I don’t have information on that. You may check IITM’s official resources for more details."*  
   - **Do not mention or reference the context explicitly.**  

         
         Context :\n\n{context}
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