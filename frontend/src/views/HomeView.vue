<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\views\HomeView.vue -->
<template>
  <div class="homeView">
    <!-- Student/Instructor/TA Profile Header Section - Only shown when logged in -->
    <div v-if="isLoggedIn" class="profile-header">
      <div class="profile-container">
        <!-- Left side with profile info -->
        <div class="profile-left">
          <div class="profile-avatar">{{ getInitials(userName) }}</div>
          <div class="profile-info">
            <h2>{{ userName }}</h2>
            <p>{{ getUserRoleText(userRole) }}</p> 
          </div>
        </div>
        
        <!-- Right side with navigation links -->
        <div class="nav-links">
          <router-link to="/" class="nav-item active">Home</router-link>
          
          <!-- Show specific buttons based on user role -->
          <template v-if="userRole === 'Student'">
          <router-link to="/mycourses" class="nav-item">My Courses</router-link>
            <router-link to="/studentqueries" class="nav-item">
              My Queries
              <img v-if="hasUnseenReplies" src="../assets/notification.png" alt="Notification" class="notification-icon" />
            </router-link>
          <router-link to="/aboutpage" class="nav-item">Profile</router-link>
          </template>
          
          <template v-if="userRole === 'Instructor'">
            <router-link to="/instructor" class="nav-item">Dashboard</router-link>
          </template>
          
          <template v-if="userRole === 'TA'">
            <router-link to="/ta" class="nav-item">Dashboard</router-link>
          </template>
          
        </div>
      </div>
    </div>

    

    <!-- Welcome Section - Visible to all -->
    <div class="container text-center mt-5">
      <h1 class="welcome-title animated-fade">Welcome to the BS-Degree Program</h1>
      <p class="welcome-text animated-fade">
        Welcome to the learning portal powered by the auto bot - an AI agent designed
        to enhance your learning experience. It helps you answer your questions
        related to the subject and assists with queries about the degree program.
      </p>
    </div>

    <!-- Chatbot Section - Always visible but with different content -->
    <div class="container text-center mt-4">
      <template v-if="hasUnseenReplies">
        
       <router-link to="/studentqueries"> <img src="../assets/botnotification.png" alt="botNotification" class="botnotification-icon" /></router-link>
      </template>
      <template v-else>
      <h3 class="animated-fade">Ask Your Pal</h3>
      
        <img src="../assets/chatbot.png" alt="Chatbot" class="img-fluid chatbot-img animated-fade" />
        </template>
  
    </div>
    
    <!-- Add Student Chatbot only if logged in -->
    <ChatBot_Student v-if="isLoggedIn" />
  </div>
</template>

<script>
import ChatBot_Student from '@/components/ChatBot_Student.vue';
import axios from 'axios';

export default {
  name: "HomeView",
  components: {
    ChatBot_Student
  },
  data() {
    return {
      userName: 'Student',
      userRole: '', // Stores user role (Student, Instructor, TA)
      isLoggedIn: false,
      hasUnseenReplies: false // Tracks if there are unseen replies
    };
  },
  mounted() {
    // Get user data from localStorage if available
    const userData = JSON.parse(localStorage.getItem('user'));
    if (userData && userData.name && userData.role) {
      this.userName = userData.name;
      this.userRole = userData.role; // Store the user's role
      this.isLoggedIn = true; // Set logged in status
      this.checkUnseenReplies(userData.email); // Check for unseen replies
    }
  },
  methods: {
    getInitials(name) {
      if (!name) return 'S';
      return name.split(' ').map(n => n[0]).join('').toUpperCase();
    },
    getUserRoleText(role) {
      if (role === 'Instructor') return 'BS Degree Instructor';
      if (role === 'TA') return 'BS Degree Teaching Assistant';
      return 'BS Degree Student';
    },
    async checkUnseenReplies(email) {
      try {
        console.log("Checking unseen replies for:", email); // Debugging log

        // Fetch unseen replies
        const response = await axios.get('http://127.0.0.1:5000/api/student-doubts');
        const unseenReplies = response.data.some(
          query => query.student_email === email && query.reply && !query.reply_seen
        );

        console.log("Unseen replies found:", unseenReplies); // Debugging log
        this.hasUnseenReplies = unseenReplies;
      } catch (error) {
        console.error("Error checking unseen replies:", error);
      }
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
  justify-content: space-between; /* Pushes content to left and right */
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

.notification-icon {
  width: 40px;
  height: 40px;
  margin-left: 0px;
}
.botnotification-icon {
  width: 230px;
  height: 200px;
  margin-left: 0px;
}
</style>
