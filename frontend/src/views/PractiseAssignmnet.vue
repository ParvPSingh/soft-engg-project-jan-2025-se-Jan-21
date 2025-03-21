<!-- <template>
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
   -->

   <template>
    <div class="assignment-container">
      <header class="navbar">
        <h1 class="navbar-title">My Courses</h1>
       
      </header>
  
      <div class="assignment-content">
        <header class="header">
          <h1>📖 Graded Assignment</h1>
          <p class="due-date">⏳ Due on 2025-01-26, 23:59 IST</p>
          <p class="submission-status">✅ Last submitted on: 2025-01-26, 21:08 IST</p>
        </header>
  
        <div v-for="(question, index) in questions" :key="index" class="question-block">
          <p class="question-text">{{ index + 1 }}) {{ question.text }}</p>
  
          <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option">
            <input type="radio" :id="'q' + index + '-opt' + optIndex" :name="'q' + index" 
              :value="option" v-model="userAnswers[index]" />
            <label :for="'q' + index + '-opt' + optIndex">{{ option }}</label>
          </div>
  
          <p v-if="submitted && userAnswers[index] !== ''" 
            :class="{ 'correct': userAnswers[index] === question.correctAnswer, 'incorrect': userAnswers[index] !== question.correctAnswer }">
            {{ userAnswers[index] === question.correctAnswer ? '✔ Correct' : '✖ Incorrect' }}
          </p>
        </div>
  
        <button class="submit-button" @click="submitAnswers">Submit</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        submitted: false,
        userAnswers: Array(10).fill(""),
        questions: [
          {
            text: "What does CPU stand for?",
            options: ["Central Processing Unit", "Computer Processing Unit", "Central Program Unit", "Control Processing Unit"],
            correctAnswer: "Central Processing Unit"
          },
          {
            text: "Which language is known as the backbone of web development?",
            options: ["Python", "Java", "HTML", "C++"],
            correctAnswer: "HTML"
          },
          {
            text: "Which company developed Java?",
            options: ["Microsoft", "Apple", "Sun Microsystems", "Google"],
            correctAnswer: "Sun Microsystems"
          },
          {
            text: "Which protocol is used for secure communication over the Internet?",
            options: ["HTTP", "FTP", "SSH", "HTTPS"],
            correctAnswer: "HTTPS"
          },
          {
            text: "Which data structure uses LIFO (Last In First Out) method?",
            options: ["Queue", "Stack", "Array", "Linked List"],
            correctAnswer: "Stack"
          },
          {
            text: "Who is known as the father of computers?",
            options: ["Alan Turing", "Charles Babbage", "Bill Gates", "Steve Jobs"],
            correctAnswer: "Charles Babbage"
          },
          {
            text: "Which symbol is used for comments in Python?",
            options: ["//", "#", "/* */", "--"],
            correctAnswer: "#"
          },
          {
            text: "What is the default port number for HTTP?",
            options: ["21", "80", "443", "8080"],
            correctAnswer: "80"
          },
          {
            text: "Which one is a relational database?",
            options: ["MongoDB", "Redis", "MySQL", "Neo4j"],
            correctAnswer: "MySQL"
          },
          {
            text: "Which OS is open-source?",
            options: ["Windows", "MacOS", "Linux", "iOS"],
            correctAnswer: "Linux"
          }
        ]
      };
    },
    methods: {
      submitAnswers() {
        this.submitted = true;
      }
    }
  };
  </script>
  
  <style scoped>
  /* 🎨 General Styles */
  body {
    font-family: Arial, sans-serif;
    background: #f0f2f5;
  }
  
  /* 🚀 Navbar */
  .navbar {
    background-color: #2c3e50;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-radius: 8px;
  }
  
  .navbar-title {
    font-size: 1.8rem;
  }
  
  .nav-links {
    display: flex;
    gap: 20px;
  }
  
  .nav-item {
    color: white;
    text-decoration: none;
    font-size: 1rem;
    transition: 0.3s ease-in-out;
  }
  
  .nav-item:hover {
    color: #f39c12;
  }
  
  /* 📚 Assignment Container */
  .assignment-container {
    max-width: 800px;
    margin: 30px auto;
    padding: 20px;
    background: white;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
  }
  
  /* 🔥 Assignment Header */
  .header {
    background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
    color: white;
    padding: 20px;
    text-align: center;
    border-radius: 8px 8px 0 0;
  }
  
  .due-date {
    color: #e74c3c;
    font-weight: bold;
  }
  
  .submission-status {
    color: #27ae60;
  }
  
  /* 🎯 Question Block */
  .question-block {
    background: #f9f9f9;
    padding: 20px;
    margin-top: 15px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  }
  
  .question-text {
    font-weight: bold;
    font-size: 1.1rem;
    color: #34495e;
  }
  
  .option {
    margin: 8px 0;
    font-size: 1rem;
  }
  
  /* ✅ Correct & ❌ Incorrect */
  .correct {
    color: green;
    font-weight: bold;
  }
  
  .incorrect {
    color: red;
    font-weight: bold;
  }
  
  /* 🎯 Submit Button */
  .submit-button {
    width: 100%;
    padding: 12px;
    background: #3498db;
    color: white;
    border: none;
    font-size: 1.1rem;
    cursor: pointer;
    margin-top: 20px;
    border-radius: 5px;
    transition: background 0.3s ease-in-out, transform 0.2s ease-in-out;
  }
  
  .submit-button:hover {
    background: #217dbb;
    transform: scale(1.05);
  }
  
  /* 📱 Responsive Design */
  @media (max-width: 768px) {
    .assignment-container {
      max-width: 90%;
    }
  
    .nav-links {
      gap: 10px;
      font-size: 0.9rem;
    }
  
    .question-text {
      font-size: 1rem;
    }
  }
  </style>
  