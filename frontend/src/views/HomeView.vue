<template>
  <div class="homeView">
    <!-- Welcome Section -->
    <div class="container text-center mt-0">
      <h1 class="welcome-title animated-fade">Welcome to the BS-Degree Program</h1>
      <p class="welcome-text animated-fade">
        Welcome to the learning portal powered by the auto bot - an AI agent designed
        to enhance your learning experience. It helps you answer your questions
        related to the subject and assists with queries about the degree program.
      </p>
    </div>

    <!-- Chatbot Section -->
    <div class="container text-center mt-4">
      <h3 class="animated-fade">Ask Your Pal</h3>
      <div class="chatbot-container">
        <img src="../assets/chatbot.png" alt="Chatbot" class="img-fluid chatbot-img animated-fade" />
        <span class="chatbot-tooltip">Chatbot is accessible only on course pages</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
};
</script>

<style scoped>
/* HomeView Background */
.homeView {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  flex-direction: column;
  justify-content: center; /* Center vertically */
}

/* Title & Welcome Text */
.welcome-title {
  color: #2c3e50;
  font-size: 2.5rem;
  font-weight: 600;
  margin-top: 0px; /* Moves it down */
}

.welcome-text {
  margin-top: 5px;
  color: #34495e;
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

/* Chatbot Image */
.chatbot-container {
  position: relative;
  display: inline-block;
}

.chatbot-img {
  margin-top: 20px;
  max-width: 200px;
  height: auto;
  cursor: pointer;
  transition: transform 0.3s ease-in-out;
}

.chatbot-img:hover {
  transform: scale(1.05);
}

/* Tooltip Styling */
.chatbot-tooltip {
  visibility: hidden;
  width: 220px;
  background-color: #2c3e50;
  color: #fff;
  text-align: center;
  padding: 8px;
  border-radius: 6px;
  font-size: 0.9rem;
  position: absolute;
  bottom: -35px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

/* Show tooltip on hover */
.chatbot-container:hover .chatbot-tooltip {
  visibility: visible;
  opacity: 1;
}

/* Fade-In Animation */
.animated-fade {
  opacity: 0;
  animation: fadeIn 1s ease-in forwards;
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

/* Responsive Styles */
@media (max-width: 768px) {
  .welcome-title {
    font-size: 2rem;
  }

  .welcome-text {
    font-size: 1rem;
  }

  .chatbot-img {
    max-width: 150px;
  }

  .chatbot-tooltip {
    width: 180px;
    font-size: 0.8rem;
  }
}
</style>
