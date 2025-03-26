from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'chatbot', '.env'))

# Ensure the TOGETHER_API_KEY is set
if 'TOGETHER_API_KEY' not in os.environ:
    raise ValueError("The TOGETHER_API_KEY environment variable is not set.")

from langchain_together import ChatTogether, TogetherEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

llm = ChatTogether(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    temperature=0,
    api_key=os.getenv("TOGETHER_API_KEY")  # Pass the API key
)

system_message_student = SystemMessage(
    content="""You are Autobot, an IITM BS degree virtual assistant designed to help students navigate the BS Data Science program.  

    Your role is to:  
    - Assist students with understanding course concepts and guidelines.  
    - Provide explanations, hints, and study strategies without giving direct answers.  
    - Help students locate relevant sections in their course materials.  
    - Encourage academic integrity by guiding students toward self-learning.  
    - Should not provide answers of questions directly. Instead provide a hint to the correct answer.

    **Guidelines:**  
    - DO NOT provide direct answers to assignments, quizzes, or exams.  
    - DO NOT generate or suggest additional resources—only the TA or instructor bot can do that.  
    - Use only the retrieved context to answer questions. If the information is unavailable, say, "I don't have that information."  
    - If a student asks for a resource, politely inform them that TAs or instructors can provide those.  
    - Maintain a professional yet supportive tone to encourage learning.  

    Your goal is to **assist students in learning while maintaining academic integrity**.  
    """
)

prompt_student = ChatPromptTemplate.from_messages([
    system_message_student,  
    MessagesPlaceholder(variable_name="retrieved_context"),
    ("human", "{user_query}")
])

autobot_student = prompt_student | llm

# Load Course Materials
python_content_path = os.path.join(os.path.dirname(__file__), 'chatbot', 'assets', 'Intro-to-python.md')
loader_student = TextLoader(python_content_path)  
documents_student = loader_student.load()

# Split into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=720, chunk_overlap=72)
chunks_student = text_splitter.split_documents(documents_student)

embedding_model = TogetherEmbeddings()
vector_store_student = FAISS.from_documents(chunks_student, embedding_model)

def retrieve_context_student(user_query):
    # Check if it's a simple greeting
    simple_greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    
    if user_query.lower().strip() in simple_greetings or user_query.lower().strip().rstrip("!") in simple_greetings:
        # Return empty context for simple greetings
        return [SystemMessage(content="")]
    
    # For normal queries, retrieve relevant context
    docs = vector_store_student.similarity_search(user_query, k=3)
    content = "\n".join([doc.page_content for doc in docs])
    return [SystemMessage(content=content)]

def call_autobot_student(user_query, retrieved_context):
    # Check if it's a simple greeting
    simple_greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    
    if user_query.lower().strip() in simple_greetings or user_query.lower().strip().rstrip("!") in simple_greetings:
        # Return a simple greeting response
        return AIMessage(content="Hello! I'm Autobot, your IITM BS degree virtual assistant. I'm here to help you with understanding course concepts and finding information in your course materials. How can I assist you today?")
    
    # For normal queries, use the full model
    return autobot_student.invoke({"user_query": user_query, "retrieved_context": retrieved_context})