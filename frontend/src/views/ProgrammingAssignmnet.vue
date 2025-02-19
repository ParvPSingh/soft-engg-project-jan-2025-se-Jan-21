<template>
    <div class="practice-programming-assignment">
      <nav class="navbar">
        <div class="nav-container">
          <h2 class="nav-title">PYTHON</h2>
          <h3 class="sub-title">PRACTICE PROGRAMMING ASSIGNMENT PAGE</h3>
        </div>
      </nav>
  
      <div class="assignment-container">
        <div class="assignment-box">
          <p class="assignment-text">
            Accept a non-zero integer as input. Print "Positive" if it is greater than zero and "Negative" if it is less than zero.
          </p>
          
          <select class="language-dropdown">
            <option>Python 3</option>
            <option>Python 3.1</option>
          </select>
  
          <div class="code-editor">
            <textarea rows="8" cols="50" v-model="codeSnippet"></textarea>
          </div>
  
          <div class="button-group">
            <button class="test-cases">Test Cases</button>
            <button class="test-run">Test Run</button>
            <button class="autobot">Autobot! 🤖</button>
            <button class="submit">Submit</button>
          </div>
        </div>
  
        <aside class="autobot-container">
          <h3>Ask your pal - Autobot</h3>
          <img src="../assets/chatbot.png" alt="">
          <p class="autobot-question"><strong>Where am I going wrong?</strong></p>
          <div class="autobot-response">
            <p>The issue here is that <code>input()</code> takes the value as a string, so comparing it with 0 (an integer) causes an error.</p>
            <p><strong>Correct Solution:</strong></p>
            <pre>
  num = int(input("Enter a non-zero integer: "))
  if num > 0:
      print("Positive")
  else:
      print("Negative")
            </pre>
          </div>
        </aside>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "PracticeProgrammingAssignment",
    data() {
      return {
        codeSnippet: "num = input(\"Enter a non-zero integer: \")\nif num > 0:\n    print(\"Positive\")\nelse:\n    print(\"Negative\")"
      };
    }
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
    padding: 1rem;
  }
  
  .assignment-box {
    width: 60%;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: #f8f9fa;
  }
  
  .language-dropdown {
    width: 100%;
    padding: 0.5rem;
    margin: 0.5rem 0;
  }
  
  .code-editor textarea {
    width: 100%;
    border: 1px solid #ddd;
    padding: 0.5rem;
    font-family: monospace;
  }
  
  .button-group {
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
  }
  
  .button-group button {
    padding: 0.5rem 1rem;
    border: none;
    cursor: pointer;
    border-radius: 5px;
  }
  
  .test-cases { background: #3498db; color: white; }
  .test-run { background: #2ecc71; color: white; }
  .autobot { background: #f1c40f; color: black; }
  .submit { background: #e74c3c; color: white; }
  
  .autobot-container {
    width: 30%;
    background: #ffe4e1;
    padding: 1rem;
    border-radius: 8px;
  }
  
  .autobot-response {
    background: white;
    padding: 0.8rem;
    border-radius: 5px;
  }
  </style>
  