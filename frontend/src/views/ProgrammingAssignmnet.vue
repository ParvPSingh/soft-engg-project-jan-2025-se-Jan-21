<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\views\ProgrammingAssignmnet.vue -->
<template>
  <div class="course-page">
    <!-- Header and Navigation from Graded Assignment -->
    <header class="header">
      <h1 class="course-title">Python Programming Assignment</h1>
      <nav class="nav-links">
        <router-link to="/" class="nav-item">Home</router-link>
        <router-link to="/mycourses" class="nav-item">My Courses</router-link>
        <router-link to="/coursepage" class="nav-item">Python Course</router-link>
        <router-link to="/aboutpage" class="nav-item">About</router-link>
      </nav>
    </header>

    <div class="container">
      <div class="assignment-content">
        <div class="problem-statement">
          <h2>Prime Number Checker</h2>
          <p>Write a function called <code>is_prime(n)</code> that checks if a number is prime.</p>
          <p>A prime number is a natural number greater than 1 that is not a product of two smaller natural numbers.</p>
          <p><strong>Function Signature:</strong> <code>def is_prime(n)</code></p>
          <p><strong>Input:</strong> An integer <code>n</code> (1 ≤ n ≤ 10^6)</p>
          <p><strong>Output:</strong> Return <code>True</code> if the number is prime, otherwise return <code>False</code></p>
        </div>
        
        <!-- AutoBot hint container -->
        <div v-if="showingHint" class="hint-container">
          <div class="hint-header">
            <span class="hint-icon">💡</span>
            <h4>AutoBot Hint:</h4>
            <button class="close-hint" @click="hideHint">×</button>
          </div>
          <p class="hint-text">{{ currentHint }}</p>
        </div>
        
        <div class="editor-container">
          <textarea 
            v-model="code" 
            class="code-editor" 
            spellcheck="false"
            @keydown.tab.prevent="handleTab"
          ></textarea>
        </div>
        
        <div class="button-container">
          <button @click="runCode" class="submit-button">Run Code</button>
          <button @click="resetCode" class="retry-button">Reset</button>
          <button @click="submitCode" class="submit-button">Submit</button>
          <!-- AutoBot hint button -->
          <button @click="showHint" class="autobot-button">
            <span class="autobot-icon">🤖</span> AutoBot!
          </button>
        </div>
        
        <div v-if="result" class="result" :class="{ success: isSuccess, error: !isSuccess }">
          <h3>{{ resultTitle }}</h3>
          <pre>{{ result }}</pre>
        </div>
        
        <div v-if="showTestCases" class="test-cases">
          <h3>Test Cases</h3>
          <pre>{{ testCasesOutput }}</pre>
        </div>
      </div>
    </div>
    <ChatBot_Student />
  </div>
</template>

<script>
import ChatBot_Student from '@/components/ChatBot_Student.vue';

export default {
  components: {
    ChatBot_Student
  },
  name: 'ProgrammingAssignment',
  data() {
    return {
      code: `def is_prime(n):
  # Write your code here
  pass

# You can test your function with the following code
# Uncomment to test
# print(is_prime(7))  # Should return True
# print(is_prime(10))  # Should return False
`,
      result: '',
      isSuccess: false,
      resultTitle: '',
      showTestCases: false,
      testCasesOutput: '',
      pyodide: null,
      isLoading: false,
      
      // AutoBot hint feature
      showingHint: false,
      currentHint: '',
      hintLevel: 0,
      hintMessages: [
        "Think about what makes a number prime: it's a natural number greater than 1 that is only divisible by 1 and itself.",
        "Start by handling edge cases: numbers less than 2 are not prime. Then check if the number is divisible by any smaller number.",
        "For efficiency, you only need to check divisibility up to the square root of the number. Can you understand why?",
        "Here's a pseudocode approach: (1) Check if n < 2, return False. (2) Check if n is divisible by any number from 2 to sqrt(n), return False if so. (3) Otherwise, return True."
      ]
    }
  },
  mounted() {
    this.loadPyodide();
    
    // Add event listener for tab key in textarea
    window.addEventListener('keydown', this.preventTabDefault);
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.preventTabDefault);
  },
  methods: {
    // AutoBot hint methods
    showHint() {
      this.showingHint = true;
      // Cycle through hints
      this.currentHint = this.hintMessages[this.hintLevel % this.hintMessages.length];
      this.hintLevel++;
    },
    
    hideHint() {
      this.showingHint = false;
    },

    // Code editor methods
    preventTabDefault(e) {
      if (e.key === 'Tab' && e.target.classList.contains('code-editor')) {
        e.preventDefault();
      }
    },
    
    handleTab(e) {
      // Insert 4 spaces at cursor position
      const start = e.target.selectionStart;
      const end = e.target.selectionEnd;
      
      this.code = this.code.substring(0, start) + '    ' + this.code.substring(end);
      
      // Move cursor position
      this.$nextTick(() => {
        e.target.selectionStart = e.target.selectionEnd = start + 4;
      });
    },
    
    // Pyodide setup and code execution
    async loadPyodide() {
      this.isLoading = true;
      this.result = 'Loading Python environment...';
      this.isSuccess = true;
      this.resultTitle = 'Status';
      
      try {
        // Dynamically load the Pyodide script
        if (!window.loadPyodide) {
          const script = document.createElement('script');
          script.src = 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js';
          script.async = true;
          document.head.appendChild(script);
          
          await new Promise((resolve, reject) => {
            script.onload = resolve;
            script.onerror = reject;
          });
        }
        
        // Initialize Pyodide
        this.pyodide = await window.loadPyodide();
        await this.pyodide.loadPackagesFromImports('import sys');
        
        // Set up stdout capture
        this.pyodide.runPython(`
          import sys
          import io
          sys.stdout = io.StringIO()
        `);
        
        this.result = 'Python environment loaded successfully!';
        this.isSuccess = true;
      } catch (error) {
        this.result = `Failed to load Python environment: ${error.message}`;
        this.isSuccess = false;
        this.resultTitle = 'Error';
      } finally {
        this.isLoading = false;
      }
    },
    
    async runCode() {
      if (!this.pyodide) {
        this.result = 'Python environment is still loading. Please wait...';
        this.isSuccess = false;
        this.resultTitle = 'Error';
        return;
      }
      
      if (this.isLoading) return;
      
      this.isLoading = true;
      this.showTestCases = false;
      
      try {
        // Reset stdout
        this.pyodide.runPython('sys.stdout = io.StringIO()');
        
        // Run the user's code
        await this.pyodide.runPythonAsync(`
${this.code}

# Test with a sample input
try:
  if 'is_prime' not in globals():
    raise NameError("Function 'is_prime' not found in your code.")
  result = is_prime(17)
  print(f"Function executed successfully!\\nFor input 17, your function returned: {result}")
except Exception as e:
  print(f"Error: {str(e)}")
        `);
        
        // Get the output
        const output = this.pyodide.runPython("sys.stdout.getvalue()");
        const error = output.includes("Error:");
        
        this.result = output;
        this.isSuccess = !error;
        this.resultTitle = error ? 'Error' : 'Success';
      } catch (error) {
        this.result = `Error executing code: ${error.message}`;
        this.isSuccess = false;
        this.resultTitle = 'Error';
      } finally {
        this.isLoading = false;
      }
    },
    
    async submitCode() {
      if (!this.pyodide) {
        this.result = 'Python environment is still loading. Please wait...';
        this.isSuccess = false;
        this.resultTitle = 'Error';
        return;
      }
      
      if (this.isLoading) return;
      
      this.isLoading = true;
      this.showTestCases = true;
      
      try {
        // Reset stdout
        this.pyodide.runPython('sys.stdout = io.StringIO()');
        
        // Run the test cases
        await this.pyodide.runPythonAsync(`
${this.code}

def check_solution():
  try:
    # Check if the function exists
    if 'is_prime' not in globals():
      return False, "Error: Function 'is_prime' not found in your code."
    
    # Test cases
    test_cases = [
      (1, False),
      (2, True),
      (3, True),
      (4, False),
      (7, True),
      (11, True),
      (15, False),
      (97, True),
      (100, False),
      (541, True)  # 100th prime number
    ]
    
    # Run test cases
    results = []
    all_passed = True
    
    for num, expected in test_cases:
      try:
        result = is_prime(num)
        passed = result == expected
        if not passed:
          all_passed = False
        results.append(f"Input: {num}, Expected: {expected}, Got: {result}, {'✓' if passed else '✗'}")
      except Exception as e:
        all_passed = False
        results.append(f"Input: {num}, Error: {str(e)}")
    
    return all_passed, "\\n".join(results)
  except Exception as e:
    return False, f"Error: {str(e)}"

success, message = check_solution()
print(f"SUCCESS: {success}")
print(f"MESSAGE: {message}")
        `);
        
        // Get the output
        const output = this.pyodide.runPython("sys.stdout.getvalue()");
        const lines = output.split('\n');
        
        // Parse the results
        const successLine = lines.find(line => line.startsWith('SUCCESS:'));
        const success = successLine && successLine.includes('True');
        
        // Extract the message (test case results)
        const messageIndex = lines.findIndex(line => line.startsWith('MESSAGE:'));
        let message = '';
        if (messageIndex >= 0) {
          message = lines[messageIndex].replace('MESSAGE: ', '');
          if (messageIndex + 1 < lines.length) {
            message = lines.slice(messageIndex).join('\n').replace('MESSAGE: ', '');
          }
        } else {
          message = 'Could not retrieve test results';
        }
        
        this.testCasesOutput = message;
        this.result = success 
          ? 'Congratulations! Your solution passed all test cases.' 
          : 'Your solution did not pass all test cases. Please check the details below.';
        this.isSuccess = success;
        this.resultTitle = success ? 'All Tests Passed!' : 'Tests Failed';
      } catch (error) {
        this.testCasesOutput = `Error executing code: ${error.message}`;
        this.result = 'An error occurred while testing your code.';
        this.isSuccess = false;
        this.resultTitle = 'Error';
      } finally {
        this.isLoading = false;
      }
    },
    
    resetCode() {
      this.code = `def is_prime(n):
  # Write your code here
  pass

# You can test your function with the following code
# Uncomment to test
# print(is_prime(7))  # Should return True
# print(is_prime(10))  # Should return False
`;
      this.result = '';
      this.showTestCases = false;
    }
  }
}
</script>

<style scoped>
/* Global Styling from Graded Assignment */
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
  border-radius: 8px;
}

.course-title {
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

/* Container Layout */
.container {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

/* Assignment Content */
.assignment-content {
  width: 100%;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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

.problem-statement {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
  border-left: 4px solid #4CAF50;
}

.editor-container {
  margin-bottom: 20px;
}

.code-editor {
  width: 100%;
  height: 300px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #2d2d2d;
  color: #f8f8f2;
  resize: vertical;
  tab-size: 4;
  -moz-tab-size: 4;
  white-space: pre;
  overflow-wrap: normal;
  overflow-x: auto;
}

/* Button Container */
.button-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
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

/* AutoBot Button */
.autobot-button {
  background-color: #9b59b6;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.autobot-button:hover {
  background-color: #8e44ad;
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.autobot-icon {
  font-size: 1.2rem;
}

/* Button Hover Effects */
.submit-button:hover:not(:disabled),
.retry-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Hint Container */
.hint-container {
  background-color: #f0f9ff;
  border-left: 4px solid #3498db;
  padding: 15px;
  margin: 15px 0;
  border-radius: 4px;
  animation: fadeIn 0.5s ease;
}

.hint-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.hint-icon {
  font-size: 1.3rem;
  margin-right: 8px;
  color: #f39c12;
}

.hint-header h4 {
  margin: 0;
  color: #3498db;
  flex-grow: 1;
}

.close-hint {
  background: none;
  border: none;
  color: #7f8c8d;
  font-size: 1.2rem;
  cursor: pointer;
}

.hint-text {
  color: #34495e;
  line-height: 1.5;
  font-size: 1rem;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.result {
  margin-top: 20px;
  padding: 15px;
  border-radius: 5px;
}

.success {
  background-color: #dff0d8;
  color: #3c763d;
  border: 1px solid #d6e9c6;
}

.error {
  background-color: #f2dede;
  color: #a94442;
  border: 1px solid #ebccd1;
}

.test-cases {
  margin-top: 20px;
  background-color: #e8f4f8;
  padding: 15px;
  border-radius: 5px;
}

pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap;
}
</style>
