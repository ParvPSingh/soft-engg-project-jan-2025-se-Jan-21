<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\views\HomeView.vue -->
<template>
  <div class="homeView">
    <!-- Student Profile Header Section -->
    <div class="profile-header">
      <div class="profile-container">
        <!-- Left side with profile info -->
        <div class="profile-left">
          <div class="profile-avatar">{{ getInitials(userName) }}</div>
          <div class="profile-info">
            <h2>{{ userName }}</h2>
            <p>BS Degree Student</p>
          </div>
        </div>
        
        <!-- Right side with navigation links -->
        <div class="nav-links">
          <router-link to="/" class="nav-item active">Home</router-link>
          <router-link to="/mycourses" class="nav-item">My Courses</router-link>
          <router-link to="/aboutpage" class="nav-item">Profile</router-link>
        </div>
      </div>
    </div>

    <!-- Welcome Section -->
    <div class="container text-center mt-5">
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
    
    <!-- Add Student Chatbot -->
    <ChatBot_Student />
  </div>
</template>

<script>
import ChatBot_Student from '@/components/ChatBot_Student.vue';

export default {
  name: "HomeView",
  components: {
    ChatBot_Student
  },
  data() {
    return {
      userName: 'Student'
    }
  },
  mounted() {
    // Get user data from localStorage if available
    const userData = JSON.parse(localStorage.getItem('user'));
    if (userData && userData.name) {
      this.userName = userData.name;
    }
  },
  methods: {
    getInitials(name) {
      if (!name) return 'S';
      return name.split(' ').map(n => n[0]).join('').toUpperCase();
    },
    handleLogout() {
      localStorage.removeItem('user');
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.profile-header {
  background-color: white;
  padding: 15px 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}


.profile-container {
  display: flex;
  align-items: center;
  justify-content: space-between; /* This pushes content to left and right edges */
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.profile-left {
  display: flex;
  align-items: center;
}

.profile-avatar {
  width: 45px;
  height: 45px;
  background: #3498db;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 18px;
  margin-right: 15px;
}

.profile-info {
  display: flex;
  flex-direction: column;
}

.profile-info h2 {
  margin: 0;
  font-size: 18px;
  color: #2c3e50;
}

.profile-info p {
  margin: 0;
  font-size: 14px;
  color: #7f8c8d;
}

.nav-links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-item {
  color: #34495e;
  text-decoration: none;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 4px;
  transition: all 0.2s;
}

.nav-item:hover, .nav-item.active {
  background-color: #f0f3f6;
  color: #3498db;
}

/* Keep other existing styles */
</style>
