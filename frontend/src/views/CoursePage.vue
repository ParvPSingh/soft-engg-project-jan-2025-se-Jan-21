<template>
    <div class="course-page">
      <nav class="navbar">
        <div class="nav-container">
          <h2 class="nav-title">Python Course</h2>
          <ul class="nav-links">
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/mycourses">My Courses</router-link></li>
            <li><router-link to="/about">About</router-link></li>
          </ul>
        </div>
      </nav>
      
      <div class="content-container">
        <aside class="sidebar">
          <h3>Course Outline</h3>
          <ul>
            <li>Week 1</li>
            <ul>
              <li>1.1 Introduction</li>
              <li>1.2 Variables</li>
              <li>Practice Assignment 1</li>
              <li>Graded Assignment 1</li>
              <li>PPA 1</li>
              <li>GPA 1</li>
            </ul>
          </ul>
        </aside>
        
        <main class="video-section">
          <h2>L1.1 A Quick Introduction to Variables</h2>
          <iframe 
            width="560" 
            height="315" 
            src="https://www.youtube.com/embed/8ndsDXohLMQ?si=KxAX_tAxLx5lSDk1" 
            title="Python Introduction" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
          </iframe>
          <p>Transcripts will appear here...</p>
        </main>
        
        <aside class="chatbot">
          <h3>Ask your AI Pal - Autobot</h3>
          <img src="../assets/chatbot.png" alt="">
          <div class="chat-box">
            <p><strong>What is a variable in Python?</strong></p>
            <p>In Python, a variable is used to store data that can be referenced and manipulated. It acts as a container for values and does not require explicit declaration of type.</p>
          </div>
          <input type="text" placeholder="Ask a question..." class="chat-input" />
        </aside>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "PythonCoursePage"
  };
  </script>
  
  <style scoped>
  .navbar {
    background: #2c3e50;
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .nav-container {
    display: flex;
    align-items: center;
    width: 100%;
    justify-content: space-between;
  }
  
  .nav-links {
    list-style: none;
    display: flex;
    gap: 1.5rem;
  }
  
  .nav-links a {
    color: white;
    text-decoration: none;
    font-weight: 600;
  }
  
  .content-container {
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    gap: 1rem;
    padding: 2rem;
  }
  
  .sidebar {
    background: #f4f4f4;
    padding: 1rem;
    border-radius: 8px;
  }
  
  .video-section {
    text-align: center;
  }
  
  .chatbot {
    background: #ffe4e1;
    padding: 1rem;
    border-radius: 8px;
  }
  
  .chat-box {
    background: white;
    padding: 0.8rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
  }
  
  .chat-input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  </style>
  