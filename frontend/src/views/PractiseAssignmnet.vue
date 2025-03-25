<template>
  <div class="assignment-container">
    <header class="navbar">
      <h1 class="navbar-title">My Courses</h1>
      <nav class="nav-links">
        <a href="#" class="nav-item">Home</a>
        <a href="#" class="nav-item">Assignments</a>
        <a href="#" class="nav-item">Profile</a>
      </nav>
    </header>

    <div class="assignment-content">
      <header class="header">
        <h1>📖 Graded Assignment</h1>
      </header>

      <div v-for="(question, index) in questions" :key="index" class="question-block">
        <p class="question-text">{{ index + 1 }}) {{ question.text }}</p>

        <div v-if="question.type === 'multiple'">
          <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option">
            <input type="radio" :id="'q' + index + '-opt' + optIndex" :name="'q' + index" 
              :value="option" v-model="userAnswers[index]" />
            <label :for="'q' + index + '-opt' + optIndex">{{ option }}</label>
          </div>
        </div>

        <div v-if="question.type === 'numeric'">
          <input type="number" v-model.number="userAnswers[index]" class="numeric-input" placeholder="Enter number" />
        </div>

        <div v-if="submitted">
          <p v-if="userAnswers[index] !== ''" 
            :class="{ 'correct': checkAnswer(index), 'incorrect': !checkAnswer(index) }">
            {{ checkAnswer(index) ? '✔ Correct' : '✖ Incorrect' }}
          </p>

          <p v-if="checkAnswer(index)" class="answer-explanation" v-html="getExplanation(index)"></p>
        </div>
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
          text: "Which of the following is a valid variable name in Python?",
          type: "multiple",
          options: ["2variable", "variable_2", "variable-2", "variable 2"],
          correctAnswer: "variable_2",
          explanation: "Variable names in Python must start with a letter or underscore and cannot contain spaces or hyphens."
        },
        {
          text: "What is the correct syntax to declare a string literal in Python?",
          type: "multiple",
          options: ["string = 'Hello'", "string = Hello", "string = \"Hello\"", "Both A and C"],
          correctAnswer: "Both A and C",
          explanation: "Both single quotes and double quotes can be used for strings in Python."
        },
        {
          text: "What is 10 + 5 in Python?",
          type: "numeric",
          correctAnswer: 15,
          explanation: "In Python, the '+' operator adds numbers together. So, 10 + 5 equals 15."
        },
        {
          text: "What is 7 * 6 in Python?",
          type: "numeric",
          correctAnswer: 42,
          explanation: "In Python, the '*' operator performs multiplication. So, 7 * 6 equals 42."
        },
        {
          text: "What is the result of 50 / 5 in Python?",
          type: "numeric",
          correctAnswer: 10,
          explanation: "In Python, the '/' operator performs division. So, 50 / 5 equals 10."
        },
        {
          text: "Which operator is used for exponentiation in Python?",
          type: "multiple",
          options: ["^", "**", "*", "//"],
          correctAnswer: "**",
          explanation: "In Python, '**' is used for exponentiation (raising a number to a power)."
        },
        {
          text: "What will be the output of `len('Python')` in Python?",
          type: "multiple",
          options: ["6", "'Python'", "[6]", "'6'"],
          correctAnswer: "6",
          explanation: "The 'len()' function returns the number of characters in a string, so `len('Python')` equals 6."
        },
        {
          text: "What is the result of 15 - 8 in Python?",
          type: "numeric",
          correctAnswer: 7,
          explanation: "In Python, the '-' operator performs subtraction. So, 15 - 8 equals 7."
        },
        {
          text: "Which keyword is used to define a function in Python?",
          type: "multiple",
          options: ["func", "def", "function", "lambda"],
          correctAnswer: "def",
          explanation: "In Python, the 'def' keyword is used to define a function."
        },
        {
          text: "What is the square root of 64 in Python?",
          type: "numeric",
          correctAnswer: 8,
          explanation: "In Python, you can calculate the square root of a number using the '**0.5' exponent or the 'math.sqrt()' function. The square root of 64 is 8."
        }
      ]
    };
  },
  methods: {
    submitAnswers() {
      this.submitted = true;
    },
    checkAnswer(index) {
      const question = this.questions[index];
      return this.userAnswers[index] == question.correctAnswer;
    },
    getExplanation(index) {
      return this.questions[index].explanation;
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
}

/* 🎯 Question Block */
.question-block {
  background-color: #f9f9f9;
  margin-bottom: 20px;
}

/* Numeric Input */
.numeric-input {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Submit Button Hover Effect */
.submit-button:hover {
  transform: scale(1.05);
}

/* Correct / Incorrect Styling */
.correct {
  color: green;
  font-size: 1.2rem;
}

.incorrect {
  color: red;
  font-size: 1.2rem;
}

/* Explanation Styling */
.answer-explanation {
  margin-top: 10px;
  font-size: 1.1rem;
  color: #555;
}
</style>
