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
│── /frontend  # Vue.js application  
│   ├── /public #contains favicons
│   ├── /src 
│   ├── ├── /assets # necessary static files
│   │   ├── /components  # Vue components  
│   │   ├── /views  # Router views/pages  
│   │   ├── /router
│   │   ├── ├── /index.js  # Vue Router setup  
│   │   ├── App.vue  # Main App component  
│   │   ├── main.js  # Vue entry point  
│   ├── /#all other necessary fie=les with vue.config.js and frontend readme.md files. 
│── /backend  # Flask API  
│   ├── main.py  # Main Flask app 
│   ├── student_chatbot.py  # Student Chatbot 
│   ├── ta_chatbot.py  # TA and instructor Chatbot 
│   ├── local_sb.sqlite3 # DataBase
│   ├── requirements_cleaned.txt # requirements.txt file ( required python packages)
│   ├── readme.md # backend readme file
│   ├── / extra py files  # Required for inital setup (for demo purpose)
│   ├── /application  # App files  
│   │   ├── controllers.py  #controller of API
│   │   ├── resources.py  # APIs  
│   │   ├── models.py  
│   │   ├── extra py files # Configuration files  
│   ├── /Chatbot  # Chatbot files  
│   │   ├── Chatbot files  # Necessary python notebooks and rag files  
│   ├── /migrations  # Database migration files  
│   ├── /server   
│   ├── /static   
│   ├── ├──/uploads # Uploaded Supplymentary Content files   
│── requirements.txt  # Python dependencies  
│── package.json  # Node.js dependencies  
│── README.md  # Project documentation  



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
   If required install extra packages manually
   ```sh
   axios
   mitt
   vue-router
   bootstrap
   chart.js
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
   pip install -r requirements_cleaned.txt
   ```

4. Start the Flask server: (inside backend folder)
   ```sh
   python main.py
   ```

5. The API should now be running at:
   ```
   http://127.0.0.1:5000/
   


