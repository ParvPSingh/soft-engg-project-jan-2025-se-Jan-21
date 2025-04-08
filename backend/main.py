from flask import Flask, request, jsonify
from flask_cors import CORS
from application.models import db, User, Role
from application.resources import api
from config import DevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from application.sec import datastore
from ta_chatbot import retrieve_context_ta, call_autobot_ta
from student_chatbot import retrieve_context_student, call_autobot_student
from application.sec import datastore
from application.models import db
from werkzeug.security import generate_password_hash

# Import necessary libraries for Qdrant vector database
from dotenv import load_dotenv
import os
import logging
from langchain_community.document_loaders import TextLoader  # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_together import TogetherEmbeddings
from langchain_community.vectorstores import Qdrant  # Updated import
from qdrant_client import QdrantClient

from qdrant_client.http.models import Distance, VectorParams, HnswConfigDiff

# Import Flask-Migrate
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()



# Global variable to store the vector store
student_vector_store = None

def initialize_database():
    with app.app_context():
        # Check if database is already initialized by looking for a user
        if not datastore.find_user(email='instructor@ds.study.iitm.ac.in'):
            db.create_all()
            datastore.find_or_create_role(name='Instructor', description='Instructor role found/created')
            datastore.find_or_create_role(name='TA', description='TA role found/created')
            datastore.find_or_create_role(name='Student', description='Student role found/created')
            
            # Create initial users
            datastore.create_user(
                name='Instructor', 
                email='instructor@ds.study.iitm.ac.in', 
                password=generate_password_hash('instructor', method="pbkdf2:sha256"), 
                roles=['Instructor']
            )
            datastore.create_user(
                name='TA', 
                email='ta@ds.study.iitm.ac.in', 
                password=generate_password_hash('tata', method="pbkdf2:sha256"), 
                roles=['TA']
            )
            db.session.commit()
            print("Database initialized with default roles and users.")
        else:
            print("Database already initialized.")

def initialize_vector_store():
    """Initialize the Qdrant vector store for student chatbot"""
    global student_vector_store
    
    print("Starting vector store initialization...")
    
    # Load Course Materials
    python_content_path = os.path.join(os.path.dirname(__file__), 'chatbot', 'assets', 'Intro-to-python.md')
    
    
    try:
        loader = TextLoader(python_content_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 800, chunk_overlap = 150
        )
        chunks = text_splitter.split_documents(documents)
        
        
        embedding_model = TogetherEmbeddings()
        
        # Connect to Qdrant Cloud
        client = QdrantClient(
            url=os.getenv("Qdrant_URL"), 
            api_key=os.getenv("Qdrant_API_KEY")
        )
        
        
        # Create collection if it doesn't exist
        collection_name = "student_docs"
        vector_size = 768
        hnsw_config=HnswConfigDiff(
            m=16,           # Default, good balance for most cases
            ef_construct=100,  # Increase for better recall during indexing
            
        )
        
        # Check if collection exists and create it if it doesn't
        collections = client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        if collection_name not in collection_names:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE,hnsw_config=hnsw_config,on_disk=False)
            )

        
        # Create vector store
        student_vector_store = Qdrant.from_documents(
            chunks, 
            embedding_model,
            url=os.getenv("Qdrant_URL"),
            api_key=os.getenv("Qdrant_API_KEY"),
            collection_name=collection_name
        )
        print("Vector store successfully initialized")
        
        return student_vector_store
        
    except Exception as e:
        print(f"Error initializing vector store: {e}")
        raise

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    CORS(app, resources={r"/*":{'origins': "*"}})
    #CORS(app, resources={r"/*":{'origins': 'http://127.0.0.1:8080', "allow_headers":"Access-Control-Allow-Origin"}})
    db.init_app(app)
    api.init_app(app)
    app.security = Security(app, datastore=datastore)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    with app.app_context():
        import application.controllers
        db.create_all()
    
    #TA chatbot endpoint
    @app.route('/api/chatbot/ta', methods=['POST'])
    def ta_chatbot():
        data = request.get_json()
        user_query = data.get('message')
        retrieved_context = retrieve_context_ta(user_query)
        response = call_autobot_ta(user_query, retrieved_context)
        return jsonify({'response': response.content})
    
    #Student chatbot endpoint
    @app.route('/api/chatbot/student', methods=['POST'])
    def student_chatbot():
        try:
            data = request.get_json()
            user_query = data.get('message')
            session_id = data.get("session_id","default_user")
            # This will use the pre-initialized vector store from student_chatbot module
            retrieved_context = retrieve_context_student(user_query)
            response = call_autobot_student(user_query, retrieved_context,session_id)
            return jsonify({'response': response.content})
        except Exception as e:
            print(f"Error in student chatbot: {str(e)}")
            return jsonify({'response': "I'm sorry, I'm having trouble connecting to my knowledge base right now. Please try again in a few moments."}), 500

    return app

app = create_app()

if __name__ == '__main__':
    initialize_database()
    # Initialize vector store when server starts
    initialize_vector_store()
    # Export the vector store to the student_chatbot module
    import student_chatbot
    student_chatbot.vector_store = student_vector_store
    app.run(debug=True,use_reloader=False)