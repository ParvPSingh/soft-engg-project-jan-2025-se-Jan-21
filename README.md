# 🚀 AI-Driven Academic Guidance Chatbot  
An AI-powered academic assistant for student queries and course guidance.

## 📌 Overview  
This project is an **AI-driven chatbot** designed to assist students with academic queries related to **student enrollment analysis, course recommendations, and general academic guidance**. The system is built with **Vue.js for the frontend** and **Flask for the backend**, ensuring a seamless user experience.

## 🛠️ Tech Stack  
- **Frontend:** Vue.js, Vue Router  
- **Backend:** Flask, Flask-RESTful  
- **Database:** SQLite   
- **Styling:** Bootstrap  
- **APIs:** OpenAI and other llms API 

## 📂 Project Structure  
/project-root
│── /frontend # Vue.js application
│ ├── /src
│ │ ├── /components # Vue components
│ │ ├── /views # Router views/pages
│ │ ├── router.js # Vue Router setup
│ │ ├── App.vue # Main App component
│ │ ├── main.js # Vue entry point
│ ├── public # Static assets
│── /backend # Flask API
│ ├── main.py # Main Flask app
│ ├── /application #app files 
| | ├── controllers.py
| | ├── resources.py #apis
| | ├── controllers.py
| | ├── models.py
│── requirements.txt # Python dependencies
│── package.json # Node.js dependencies
│── README.md # Project documentation


# 🚀 Installation & Setup

## Frontend (Vue.js) Setup

1. Navigate to the frontend folder:
   ```sh
   cd frontend
   ```

2. Install dependencies:
   ```sh
   npm install
   ```

3. Start the Vue.js server:
   ```sh
   npm run serve
   ```

4. Open the app in a browser at:
   ```
   http://localhost:8080/
   ```

---

## Backend (Flask) Setup

1. Navigate to the backend folder:
   ```sh
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv  
   source venv/bin/activate  # On macOS/Linux  
   venv\Scripts\activate  # On Windows  
   ```

3. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```sh
   python app.py
   ```

5. The API should now be running at:
   ```
   http://127.0.0.1:5000/
   


