<template>
  <div class="homeView">
    <nav class="navbar">
      <div class="logo">
        <img src="../assets/IIT-Madras-01.svg" alt="Logo" class="logo-image" />
      </div>
      <div class="actions">
        <button class="login-button" @click="goToLogin">Login</button>
        <button class="register-button" @click="goToRegister">Register</button>
      </div>
    </nav>
    <div class="welcome-section">
      <h1 class="welcome-title">Welcome to the BS-Degree Program</h1>
      <p class="welcome-text">
        Welcome to the learning portal powered by the auto bot - an AI agent
        designed to enhance your learning experience. It helps you answer your
        questions related to the subject and assists with queries about the
        degree program.
      </p>
    </div>
    <div class="chatbot">
      <h3>Ask Your Pal</h3>
      <img src="../assets/chatbot.png" alt="">
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  methods: {
    goToLogin() {
      this.$router.push("/login");
    },
    goToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>

<style>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #f0f0f0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  margin-left: 20px;
}

.logo-image {
  height: 40px;
  width: 40px;
}

.actions {
  margin-right: 20px;
}

.login-button,
.register-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.login-button {
  background-color: #3498db;
  color: white;
}

.register-button {
  background-color: #e7753c;
  color: white;
  margin-left: 10px;
}

.login-button:hover,
.register-button:hover {
  opacity: 0.8;
}
.welcome-section {
  max-width: 800px;
  margin: 60px auto;
  padding: 0 20px;
  text-align: center;
  animation: fadeIn 1s ease-in;
}

.welcome-title {
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
  line-height: 1.2;
}

.welcome-text {
  color: #34495e;
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  font-weight: 400;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.homeView {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
.chatbot {
  max-width: 800px;
  margin: 60px auto;
  padding: 0 20px;
  text-align: center;
  animation: fadeIn 1s ease-in;
}
</style>
