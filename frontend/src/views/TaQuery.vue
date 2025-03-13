<template>
    <div class="ta-queries-page">
      <nav class="navbar">
        <div class="nav-container">
          <h2 class="nav-title">TA [ STUDENT QUERIES ]</h2>
        </div>
      </nav>
      
      <div class="filter-section">
        <select class="course-dropdown">
          <option>Python</option>
          <option>Data Structures</option>
          <option>Algorithms</option>
        </select>
        <select class="week-dropdown">
          <option>WEEK 1</option>
          <option>WEEK 2</option>
          <option>WEEK 3</option>
        </select>
      </div>
      
      <table class="queries-table">
        <thead>
          <tr>
            <th>NAME</th>
            <th>ROLL NO.</th>
            <th>QUERY</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Tushar Bharti</td>
            <td>21f10056</td>
            <td>What is the difference between == and is in Python?</td>
          </tr>
          <tr>
            <td>Podey Om Prabhakar</td>
            <td>21f20009</td>
            <td>Are there any interactive coding platforms to practice Python?</td>
          </tr>
          <tr>
            <td>Akshat Kaushik</td>
            <td>21f30003</td>
            <td>Can you explain how list comprehension works?</td>
          </tr>
        </tbody>
      </table>
      
      <aside class="chatbot">
        <h3>Ask your pal - Autobot</h3>
        <img src="../assets/chatbot.png" alt="">
        <p><strong>What are the most common queries students are raising?</strong></p>
        <ul>
          <li>Concept Understanding</li>
          <li>Assignment & Scores</li>
          <li>Study Materials & Practice</li>
          <li>General Coding Help</li>
        </ul>
      </aside>
    </div>
  </template>
  
  <script>
  export default {
    name: "TAQueriesPage"
  };
  </script>
  
  <style scoped>
  .navbar {
    background: #2c3e50;
    color: white;
    padding: 1rem;
    text-align: center;
  }
  
  .filter-section {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 1rem 0;
  }
  
  .queries-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
  }
  
  .queries-table th, .queries-table td {
    border: 1px solid #ddd;
    padding: 0.8rem;
    text-align: left;
  }
  
  .chatbot {
    background: #ffe4e1;
    padding: 1rem;
    border-radius: 8px;
    width: 300px;
    margin: 1rem auto;
  }
  </style>
  