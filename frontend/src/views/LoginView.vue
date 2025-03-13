<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Welcome Back</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Enter your email"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />
        </div>

        <div class="form-group">
          <label for="role">Role</label>
          <select id="role" v-model="role" required>
            <option value="" disabled selected>Select your role</option>
            <option value="student">Student</option>
            <option value="instructor">Instructor</option>
            <option value="ta">Teaching Assistant</option>
          </select>
        </div>

        <button type="submit" class="login-button" :disabled="loading">
          {{ loading ? "Logging in..." : "Login" }}
        </button>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { eventBus } from "../components/NavBar.vue";  // Import event bus

export default {
  name: "LoginView",
  data() {
    return {
      email: "",
      password: "",
      role: "",
      loading: false,
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.errorMessage = "";

      try {
        const response = await axios.post("http://127.0.0.1:5000/api/login", {
          email: this.email,
          password: this.password,
        });

        if (response.status === 200) {
          const userData = response.data;

          // Store user data in localStorage (can be used for authentication later)
          localStorage.setItem("user", JSON.stringify(userData));
          eventBus.emit("user-updated"); // Notify navbar of login

          // Redirect based on role
          if (this.role === "student") {
            this.$router.push("/mycourses");
          } else if (this.role === "instructor") {
            this.$router.push("/instructor");
          } else if (this.role === "ta") {
            this.$router.push("/ta");
          }
        }
      } catch (error) {
        if (error.response && error.response.data.error_message) {
          this.errorMessage = error.response.data.error_message;
        } else {
          this.errorMessage = "Invalid credentials. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Keeping the Same Theme */
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.9rem;
}

input,
select {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input:focus,
select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.login-button {
  background: #3498db;
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background: #2980b9;
}

.login-button:active {
  transform: scale(0.98);
}

/* Error Message Styling */
.error-message {
  color: red;
  text-align: center;
  font-weight: bold;
  margin-top: 10px;
}

/* Mobile Responsiveness */
@media (max-width: 576px) {
  .login-card {
    width: 90%;
    padding: 1.5rem;
  }
}
</style>
