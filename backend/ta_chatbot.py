from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'chatbot', '.env'))

# Ensure the TOGETHER_API_KEY is set
if 'TOGETHER_API_KEY' not in os.environ:
    raise ValueError("The TOGETHER_API_KEY environment variable is not set.")

from langchain_together import ChatTogether, TogetherEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

llm = ChatTogether(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    temperature=0,
    max_tokens=300,
    api_key=os.getenv("TOGETHER_API_KEY")  # Pass the API key
)
system_message_ta = SystemMessage(
    content="""You are an AI assistant for the Teaching Assistants (TAs) and Admins of the IITM BS Data Science program.
    
    You assist with:
    - Course grading policies and assessment guidelines
    - Managing student inquiries and support requests
    - Academic integrity and plagiarism guidelines
    - Deadlines, resubmissions, and late penalties
    - Handling student complaints and escalations

    Guidelines:
    - Only respond to TA/Admin-related queries.
    - Do NOT provide direct assignment solutions or help with assessments.
    - If a question is beyond your scope, suggest the correct contact or resource.
    - Maintain professional and formal responses.
    - Use retrieved context from official documents when answering.
    - Python course grading formula: T = 0.1 GAA1 (objective) + 0.1 GAA2 (programming) + 0.1 Qz1 + 0.4 F + 0.25 max(PE1, PE2) + 0.15 min(PE1, PE2) — capped to 100."
    - Answer in bullet points for clarity.
    - Use the retrieved context to provide accurate and relevant information.
    Your goal is to support TAs and Admins in managing academic processes efficiently."""
)

prompt_ta = ChatPromptTemplate.from_messages([
    system_message_ta,  
    MessagesPlaceholder(variable_name="retrieved_context"),
    ("human", "{user_query}")
])

autobot_ta = prompt_ta | llm

# Load TA/Admin Guidelines Document - Update path to correct location
guidelines_path = os.path.join(os.path.dirname(__file__), 'chatbot', 'assets', 'TA-Admin-Guidelines.md')
loader_ta = TextLoader(guidelines_path)  
documents_ta = loader_ta.load()

# Split into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=720, chunk_overlap=72)
chunks_ta = text_splitter.split_documents(documents_ta)

embedding_model = TogetherEmbeddings()
vector_store_ta = FAISS.from_documents(chunks_ta , embedding_model)

def retrieve_context_ta(user_query):
    # Check if it's a simple greeting
    simple_greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    
    if user_query.lower().strip() in simple_greetings or user_query.lower().strip().rstrip("!") in simple_greetings:
        # Return empty context for simple greetings
        return [SystemMessage(content="")]
    
    # For normal queries, retrieve relevant context
    docs = vector_store_ta.similarity_search(user_query, k=3)
    content = "\n".join([doc.page_content for doc in docs])
    return [SystemMessage(content=content)]

def call_autobot_ta(user_query, retrieved_context):
    # Check if it's a simple greeting
    simple_greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    
    if user_query.lower().strip() in simple_greetings or user_query.lower().strip().rstrip("!") in simple_greetings:
        # Return a simple greeting response without invoking the full model
        from langchain.schema import AIMessage
        return AIMessage(content="Hello! I'm the TA assistant for IITM BS Data Science program. How can I help you today with course management, grading policies, or student inquiries?")
    
    # For normal queries, use the full model
    return autobot_ta.invoke({"user_query": user_query, "retrieved_context": retrieved_context})