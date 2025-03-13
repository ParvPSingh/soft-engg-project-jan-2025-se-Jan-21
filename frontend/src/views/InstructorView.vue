<template>
    <div class="instructor-page">
      <nav class="navbar">
        <div class="nav-container">
          <h2 class="nav-title">Instructor - Python Course</h2>
          <ul class="nav-links">
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/dashboard">Dashboard</router-link></li>
            <li><router-link to="/logout">Logout</router-link></li>
          </ul>
        </div>
      </nav>
      
      <div class="content-container">
        <div class="actions">
          <button class="review-students">Review Students</button>
          <button class="academic-content">Academic Content</button>
          <button class="delete-course">Delete Course</button>
        </div>
        
        <div class="analytics">
          <h3>Course Analytics</h3>
          <img src="../assets/instructorgraph.png" alt="Analytics Chart" class="analytics-image" />
        </div>
        
        <aside class="chatbot">
          <h3>Ask your AI Pal - Autobot</h3>
          <img src="../assets/chatbot.png" alt="">
          <div class="chat-box">
            <p><strong>Can you provide relevant study materials for Recursion?</strong></p>
            <p>Recommended study materials: WS3Schools, GeeksforGeeks, and Python Docs. Links available in the course materials.</p>
          </div>
          <input type="text" placeholder="Ask a question..." class="chat-input" />
        </aside>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "InstructorPythonPage"
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
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
  }
  
  .actions {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  button {
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
  }
  
  .review-students { background: #28a745; color: white; }
  .academic-content { background: #007bff; color: white; }
  .delete-course { background: #dc3545; color: white; }
  
  .analytics {
    margin-bottom: 0rem;
    text-align: center;
  }
  
  .analytics-image {
    width: 350px;
    height: auto;
  }
  
  .chatbot {
    background: #ffe4e1;
    padding: 1rem;
    border-radius: 8px;
    width: 800px;
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
