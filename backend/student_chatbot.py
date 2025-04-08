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
from langchain.schema import AIMessage, SystemMessage

# Configure logging


# This will be set by main.py
vector_store = None
conversation_count = {}
MAX_MESSAGES = 5

# Initialize LLM and retriever once the vector_store is available
def initialize_chatbot():
    global retriever, history_aware_retriever, document_chain, rag_chain, conversational_rag_chain
    
    if vector_store is None:
        raise RuntimeError("Vector store not initialized")
    
    retriever = vector_store.as_retriever(search_kwargs={"k":2})
    
    llm = ChatTogether(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", temperature=0, max_tokens=400)
    
    context_adding_prompt = ChatPromptTemplate.from_messages([
    ("system", """"
    You are an AI assistant for the IITM BS Degree program. 
    [INST]
    The final grading scale is as follows:
    S = 90-100, A = 80-89, B = 70-79, C = 60-69, D = 50-59, E = 40-49, U = 0-39
    You have to help student to calcuate their grades based on the following formula:
    T = 0.1 GAA1 (objective) + 0.1 GAA2 (programming) + 0.1 Qz1 + 0.4 F + 0.25 max(PE1, PE2) + 0.15 min(PE1, PE2) — capped to 100
    Give the student the final grade based on the above formula and the grading scale.
    [/INST]
     
    [INST]
    IMPORTANT: BE EXTREMELY CONCISE. All responses must be under 300 tokens.
    **For Off-Topic Questions**
    - If a question is unrelated to the course content (like personal matters, politics, entertainment, general knowledge, etc.), respond with:
    "I'm designed to help with the IITM BS Degree program content only. I don't have information on that topic. Could you ask something related to your Python course, assignments, or course policies?"

    1. **For Factual Questions, Course Policies & Grading**
    - Give direct, brief answers with minimal explanation.
    - For formulas or calculations, use EXACT formulas from the context.
    - **Example Formula Questions:**
        - **Student:** "What's the grading formula for Python?"
        - **AI:** "Python course grading formula: T = 0.1 GAA1 (objective) + 0.1 GAA2 (programming) + 0.1 Qz1 + 0.4 F + 0.25 max(PE1, PE2) + 0.15 min(PE1, PE2) — capped to 100."

    2. **For Concept Explanations**
    - Focus on core definition + 2-3 key points only.
    - Use bullet points for explanation.
    - **Example Concept:**
        - **Student:** "Explain object-oriented programming"
        - **AI:** "Object-Oriented Programming (OOP) organizes code around objects that bundle data and methods.
        • Classes: Templates for creating objects
        • Inheritance: Reusing code between related classes
        • Encapsulation: Hiding internal implementation
        • Polymorphism: Same interface for different underlying forms"

    3. **For Every  MCQs Asked **
    - Provide only 1-2 brief hints.
    - **Example:**
        - **Student:** "Is the complexity of quicksort O(n²) or O(n log n)?"
        - **AI:** "Consider the average case vs. worst case. What happens when the pivot divides the array evenly vs. when the array is already sorted?"

    4. **Using Context**
    - If the exact answer is in context, copy it directly without modification.
    - Omit all examples unless specifically requested.
    - Never mention that you're using context.
    - Keep responses under 300 tokens.
    - If the information isn't in context, say: "I don't have specific information on that. Please check IITM's official resources."

    5. **For Programming Questions and Assignments**
    - NEVER provide complete solutions to programming assignments or exercises.
    - Instead, offer 2-3 specific hints that guide the student's thinking.
    - For syntax questions, provide small, generic example snippets (not full solutions).
    - Use the Socratic method to help students discover solutions themselves.
    - **Example Programming Question:**
        - **Student:** "Write a program to find the factorial of a number"
        - **AI:** "Instead of giving you the solution, let me help you think through it:
        • Consider using a loop to multiply numbers from 1 to n
        • Remember the base case: factorial of 0 is 1
        • Here's a small example of a loop structure in Python:
        ```python
        # This shows the structure, but YOU need to implement the logic
        def some_function(n):
            result = 1  # Starting value
            # Your loop logic here
            return result
     [/INST]
       ```"
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
def call_autobot_student(user_query, retrieved_context,session_id):
    # Make sure chatbot components are initialized
    if 'conversational_rag_chain' not in globals():
        initialize_chatbot()
    
    # Check if it's a simple greeting
    simple_greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    
    if user_query.lower().strip() in simple_greetings or user_query.lower().strip().rstrip("!") in simple_greetings:
        # Return a simple greeting response
        return AIMessage(content="Hello! I'm Autobot, your IITM BS degree virtual assistant. I'm here to help you with understanding course concepts and finding information in your course materials. How can I assist you today?")
    if session_id not in conversation_count:
        conversation_count[session_id] = 0

    conversation_count[session_id] += 1
    print(conversation_count[session_id])
    # For normal queries, use the conversational RAG chain
    if conversation_count[session_id]> MAX_MESSAGES:
        return AIMessage(content="You have exceeded the maximum number of messages for this session. Please refresh and  start a new session.")
    
    
    response = conversational_rag_chain.invoke(
        {"input": user_query},
        config={"configurable": {"session_id": session_id}}
    )
    
    # Convert the response to an AIMessage for compatibility with existing code
    if isinstance(response, dict) and "answer" in response:
        return AIMessage(content=response["answer"])
    else:
        return AIMessage(content=str(response))
    

    
