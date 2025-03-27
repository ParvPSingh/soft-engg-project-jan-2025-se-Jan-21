<template>
  <div class="course-page">
    <header class="header">
      <h1 class="course-title">Python Graded Assignment</h1>
      <nav class="nav-links">
        <router-link to="/" class="nav-item">Home</router-link>
        <router-link to="/mycourses" class="nav-item">My Courses</router-link>
        <router-link to="/coursepage" class="nav-item">Python Course</router-link>

        <router-link to="/aboutpage" class="nav-item">About</router-link>
      </nav>
    </header>

    <div class="container">
      <div class="assignment-content">
        <!-- <header class="lecture-view">
          <h1 class="lecture-title">📖 Graded Assignment</h1>
        </header> -->

        <!-- Score display section -->
        <div v-if="submitted" class="score-display">
          <h2>Your Score: {{ correctAnswers }} / {{ questions.length }}</h2>
          <div class="progress-bar">
            <div class="progress" :style="{ width: (correctAnswers / questions.length) * 100 + '%' }"></div>
          </div>
          <p class="score-message">{{ scoreMessage }}</p>
        </div>

        <div v-for="(question, index) in questions" :key="index" class="question-block">
          <p class="question-text">{{ index + 1 }}) {{ question.text }}</p>
          
          <pre v-if="question.code" class="code-block">{{ question.code }}</pre>

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

            <p v-if="!checkAnswer(index)" class="answer-explanation">
              Correct answer: <span class="correct-answer">{{ questions[index].correctAnswer }}</span>
            </p>

            <p class="answer-explanation" v-html="getExplanation(index)"></p>
          </div>
        </div>

        <div class="button-container">
          <button class="submit-button" @click="submitAnswers" :disabled="submitted">
            {{ submitted ? 'Submitted' : 'Submit' }}
          </button>
          <button v-if="submitted" class="retry-button" @click="resetQuiz">Try Again</button>
        </div>
      </div>
    </div>
    <ChatBot_Student />
  </div>
</template>

<script>
import ChatBot_Student from '@/components/ChatBot_Student.vue';
import axios from 'axios';

export default {
    components: {
      ChatBot_Student
    },
    data() {
      return {
        submitted: false,
        userAnswers: Array(12).fill(""),
        correctAnswers: 0,
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
            text: "What is the output of the following code?",
            code: "x = [1, 2, 3]\ny = x\ny.append(4)\nprint(x)",
            type: "multiple",
            options: ["[1, 2, 3]", "[1, 2, 3, 4]", "[1, 2, 3, [4]]", "Error"],
            correctAnswer: "[1, 2, 3, 4]",
            explanation: "In Python, when you assign a list to another variable, both variables reference the same list object. Changes made through either variable affect the same underlying object."
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
            text: "Find the error in the following code:",
            code: "def calculate_average(numbers):\n    total = 0\n    for num in numbers\n        total += num\n    return total / len(numbers)",
            type: "multiple",
            options: ["Missing colon after for loop", "Incorrect indentation", "Division by zero error", "Function name is invalid"],
            correctAnswer: "Missing colon after for loop",
            explanation: "The for loop statement is missing a colon at the end. It should be 'for num in numbers:'"
          },
          {
            text: "Which keyword is used to define a function in Python?",
            type: "multiple",
            options: ["func", "def", "function", "lambda"],
            correctAnswer: "def",
            explanation: "In Python, the 'def' keyword is used to define a function."
          },
          {
            text: "What is the output of this list comprehension?",
            code: "[x**2 for x in range(5) if x % 2 == 0]",
            type: "multiple",
            options: ["[0, 4, 16]", "[0, 2, 4]", "[0, 4]", "[0, 1, 4, 9, 16]"],
            correctAnswer: "[0, 4, 16]",
            explanation: "This list comprehension squares each value in range(5) [0,1,2,3,4] but only includes those where x % 2 == 0 [0,2,4]. So the result is [0², 2², 4²] which equals [0, 4, 16]."
          },
          {
            text: "What will this code print?",
            code: "try:\n    print(1/0)\nexcept ZeroDivisionError:\n    print('Error')\nfinally:\n    print('Done')",
            type: "multiple",
            options: ["Error", "Done", "Error\\nDone", "ZeroDivisionError\\nDone"],
            correctAnswer: "Error\\nDone",
            explanation: "The code attempts to divide by zero, which raises a ZeroDivisionError. The except block catches this error and prints 'Error'. The finally block always executes and prints 'Done'."
          },
          {
            text: "What is the output of this dictionary operation?",
            code: "d = {'a': 1, 'b': 2}\nd.update({'b': 3, 'c': 4})\nprint(d)",
            type: "multiple",
            options: ["{'a': 1, 'b': 2}", "{'a': 1, 'b': 3, 'c': 4}", "{'a': 1, 'b': 2, 'c': 4}", "Error"],
            correctAnswer: "{'a': 1, 'b': 3, 'c': 4}",
            explanation: "The update() method updates the dictionary with elements from another dictionary. It updates the value of 'b' to 3 and adds a new key-value pair 'c': 4."
          },
          {
            text: "What is the time complexity of this function?",
            code: "def mystery(n):\n    result = 0\n    for i in range(n):\n        for j in range(n):\n            result += i * j\n    return result",
            type: "multiple",
            options: ["O(n)", "O(n²)", "O(n log n)", "O(2ⁿ)"],
            correctAnswer: "O(n²)",
            explanation: "The function has two nested loops, each iterating n times. This results in n × n = n² operations, giving a time complexity of O(n²)."
          },
          {
            text: "Find the error in this recursive function:",
            code: "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n)",
            type: "multiple",
            options: ["Missing base case", "Incorrect return value", "Infinite recursion", "Syntax error"],
            correctAnswer: "Infinite recursion",
            explanation: "The recursive call should be factorial(n-1), not factorial(n). As written, this will cause infinite recursion since the parameter never changes."
          }
        ]
      };
    },
    computed: {
      scoreMessage() {
        const percentage = (this.correctAnswers / this.questions.length) * 100;
        if (percentage >= 90) return "Excellent! You've mastered Python basics!";
        if (percentage >= 70) return "Good job! You have a solid understanding of Python.";
        if (percentage >= 50) return "Not bad! Keep practicing to improve your Python skills.";
        return "Keep studying! Python takes practice to master.";
      }
    },
    methods: {
      submitAnswers() {
        this.submitted = true;
        this.correctAnswers = 0;
        
        // Calculate score
        for (let i = 0; i < this.questions.length; i++) {
          if (this.checkAnswer(i)) {
            this.correctAnswers++;
          }
        }
      },
      checkAnswer(index) {
        const question = this.questions[index];
        return this.userAnswers[index] == question.correctAnswer;
      },
      getExplanation(index) {
        return this.questions[index].explanation;
      },
      resetQuiz() {
        this.submitted = false;
        this.userAnswers = Array(this.questions.length).fill("");
        this.correctAnswers = 0;
      }
    }
};
</script>

<style scoped>

.courses-page {
  font-family: 'Arial', sans-serif;
  text-align: center;
  background: linear-gradient(135deg, #eef2f3 0%, #8e9eab 100%);
  min-height: 100vh;
  padding: 30px 20px;
}

/* Header */
.header {
  background-color: #2c3e50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-radius: 8px;
}

.page-title {
  font-size: 1.8rem;
}

/* Navigation */
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
/* Global Styling */
.course-page {
  font-family: 'Arial', sans-serif;
  background-color: #f8f9fa;
  color: #333;
}

/* Header */
.header {
  background-color: #2c3e50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
}

.course-title {
  font-size: 1.8rem;
}

/* Container Layout */
.container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

/* Assignment Content */
.assignment-content {
  width: 100%;
}

/* Lecture View / Assignment Header */
.lecture-view {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  text-align: center;
}

.lecture-title {
  font-size: 1.5rem;
  color: #2c3e50;
}

/* Score Display */
.score-display {
  background-color: #ecf0f1;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.score-display h2 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.progress-bar {
  width: 100%;
  height: 20px;
  background-color: #dfe6e9;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  transition: width 0.5s ease-in-out;
}

.score-message {
  font-size: 1.1rem;
  color: #2c3e50;
  font-weight: bold;
}

/* Question Block */
.question-block {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.question-text {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 10px;
  color: #34495e;
}

/* Code block styling */
.code-block {
  background-color: #282c34;
  color: #abb2bf;
  padding: 15px;
  border-radius: 5px;
  font-family: 'Courier New', monospace;
  overflow-x: auto;
  margin: 10px 0;
}

/* Option styling */
.option {
  margin: 8px 0;
  display: flex;
  align-items: center;
}

.option label {
  margin-left: 8px;
  cursor: pointer;
  color: #2c3e50;
}

/* Numeric Input */
.numeric-input {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Button Container */
.button-container {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

/* Submit Button */
.submit-button {
  background-color: #2980b9;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.submit-button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

/* Retry Button */
.retry-button {
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

/* Button Hover Effects */
.submit-button:hover:not(:disabled),
.retry-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Correct / Incorrect Styling */
.correct {
  color: #27ae60;
  font-weight: bold;
  font-size: 1.1rem;
}

.incorrect {
  color: #e74c3c;
  font-weight: bold;
  font-size: 1.1rem;
}

.correct-answer {
  font-weight: bold;
  color: #27ae60;
}

/* Explanation Styling */
.answer-explanation {
  margin-top: 10px;
  font-size: 1rem;
  color: #7f8c8d;
  line-height: 1.5;
}
</style>
