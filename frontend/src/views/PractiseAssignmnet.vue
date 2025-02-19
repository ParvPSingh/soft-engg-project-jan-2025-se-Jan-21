<template>
    <div class="practice-assignment-page">
      <nav class="navbar">
        <div class="nav-container">
          <h2 class="nav-title">PYTHON - PRACTICE ASSIGNMENT PAGE</h2>
        </div>
      </nav>
      
      <div class="assignment-container">
        <div class="question-box">
          <h3>What will 3 * 2 ** 3 evaluate to?</h3>
          <ul>
            <li>A) 18</li>
            <li>B) 24</li>
            <li>C) 27</li>
            <li>D) 64</li>
          </ul>
          <button class="explain-button">Explain</button>
        </div>
        
        <div class="question-box">
          <h3>What will be the output of print("Hello"[::-1])?</h3>
          <ul>
            <li>A) Hello</li>
            <li>B) olleH</li>
            <li>C) Error</li>
            <li>D) H</li>
          </ul>
          <button class="explain-button">Explain</button>
        </div>
      </div>
      
      <aside class="chatbot">
        <h3>Ask your pal - Autobot</h3>
        <img src="../assets/chatbot.png" alt="">
        <p><i>Explain What will 3 * 2 ** 3 evaluate to</i></p>
        <p><strong>Let's break it down step by step! 😊</strong></p>
        <p>1. The ** operator means exponentiation (raising a number to a power).</p>
        <p>2. 2 ** 3 means 2 raised to the power of 3, which is 8.</p>
        <p>3. Now, multiply 3 * 8, which gives us 24.</p>
      </aside>
    </div>
  </template>
  
  <script>
  export default {
    name: "PracticeAssignmentPage"
  };
  </script>
  
  <style scoped>
  .navbar {
    background: #2c3e50;
    color: white;
    padding: 1rem;
    text-align: center;
  }
  .assignment-container {
    display: flex;
    justify-content: space-around;
    margin: 2rem;
  }
  .question-box {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    width: 40%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  .explain-button {
    background: #007bff;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    cursor: pointer;
    margin-top: 1rem;
  }
  .chatbot {
    background: #ffe4e1;
    padding: 1rem;
    border-radius: 8px;
    width: 800px;
    margin: 1rem auto;
  }
  </style>
  