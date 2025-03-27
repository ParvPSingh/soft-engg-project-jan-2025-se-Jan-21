<template>
  <div class="register-container">
    <div class="register-card">
      <h1>Create Account</h1>
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="name">Full Name</label>
          <input
            type="text"
            id="name"
            v-model="name"
            placeholder="Enter your full name"
            required
          />
        </div>

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
            placeholder="Create a password"
            required
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            placeholder="Confirm your password"
            required
          />
        </div>

        <button type="submit" class="register-button" :disabled="loading">
          {{ loading ? "Registering..." : "Register" }}
        </button>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>
    </div>
    
    
  </div>
</template>

<script>

import axios from "axios";

import ChatBot_TA from '@/components/ChatBot_TA.vue';


export default {
  name: "RegisterView",
  components: {
    ChatBot_TA
  },
  data() {
    return {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      loading: false,
      errorMessage: "",
    };
  },
  methods: {
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        this.errorMessage = "Passwords do not match!";
        return;
      }

      this.loading = true;
      this.errorMessage = "";

      try {
        const response = await axios.post("http://127.0.0.1:5000/signup", {
          name: this.name,
          email: this.email,
          password: this.password,
        });

        if (response.status === 201) {
          alert("Registration successful! Redirecting to login.");
          this.$router.push("/login");
        }
      } catch (error) {
        if (error.response && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = "Something went wrong. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Keeping Your Theme */
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.register-card {
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

.register-form {
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

input {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.register-button {
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

.register-button:hover {
  background: #2980b9;
}

.register-button:active {
  transform: scale(0.98);
}

/* Error Message Styling */
.error-message {
  color: red;
  text-align: center;
  font-weight: bold;
  margin-top: 10px;
}

/* Responsive Design */
@media (max-width: 576px) {
  .register-card {
    width: 90%;
    padding: 1.5rem;
  }
}
</style>
