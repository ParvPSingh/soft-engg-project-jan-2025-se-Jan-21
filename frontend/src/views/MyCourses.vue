<template>
  <div class="course-page">
    <header class="header">
      <h1 class="course-title">📚 My Courses</h1>
      <nav class="nav-links">
        <router-link to="/" class="nav-item">Home</router-link>
        <router-link to="/mycourses" class="nav-item">My Courses</router-link>
        <router-link to="/studentqueries" class="nav-item">
          My Queries
          <img v-if="hasUnseenReplies" src="../assets/notification.png" alt="Notification" class="notification-icon" />
        </router-link>
        <router-link to="/aboutpage" class="nav-item">About</router-link>
      </nav>
    </header>

    <div class="container">
      <div class="courses-content">
        <div class="courses-container">
          <div class="course-card question-block">
            <div class="course-icon">🐍</div>
            <h2 class="question-text">Python Programming</h2>
            <p class="course-description">Learn the fundamentals of Python programming language, from basic syntax to advanced concepts. This comprehensive course covers variables, data types, control structures, functions, and object-oriented programming.</p>
            <div class="course-details">
              <span class="detail-item">⏱️ 8 weeks</span>
              <span class="detail-item">📊 Beginner</span>
              <span class="detail-item">📘 24 lessons</span>
            </div>
            <div class="button-container">
              <router-link to="/coursepage" class="submit-button">View Course</router-link>
            </div>
          </div>

          <div class="course-card question-block">
            <div class="course-icon">📊</div>
            <h2 class="question-text">JavaScript Fundamentals</h2>
            <p class="course-description">Master the basics of JavaScript for web development. This interactive course teaches you DOM manipulation, event handling, asynchronous programming with promises, and modern ES6+ features.</p>
            <div class="course-details">
              <span class="detail-item">⏱️ 10 weeks</span>
              <span class="detail-item">📊 Intermediate</span>
              <span class="detail-item">📘 30 lessons</span>
            </div>
            <div class="button-container">
              <router-link to="/javascript-course" class="submit-button">View Course</router-link>
            </div>
          </div>

          <div class="course-card question-block">
            <div class="course-icon">🧠</div>
            <h2 class="question-text">Deep Learning</h2>
            <p class="course-description">Explore neural networks and advanced AI techniques in this cutting-edge course. Learn about convolutional neural networks, recurrent neural networks, and how to implement them using popular frameworks.</p>
            <div class="course-details">
              <span class="detail-item">⏱️ 12 weeks</span>
              <span class="detail-item">📊 Advanced</span>
              <span class="detail-item">📘 36 lessons</span>
            </div>
            <div class="button-container">
              <router-link to="/deep-learning" class="submit-button">View Course</router-link>
            </div>
          </div>
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
      hasUnseenReplies: false // Tracks if there are unseen replies
    };
  },
  mounted() {
    this.checkUnseenReplies();
  },
  methods: {
    async checkUnseenReplies() {
      try {
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user || !user.email) return;

        // Fetch unseen replies
        const response = await axios.get('http://127.0.0.1:5000/api/student-doubts');
        const unseenReplies = response.data.some(
          query => query.student_email === user.email && query.reply && !query.reply_seen
        );

        this.hasUnseenReplies = unseenReplies;
      } catch (error) {
        console.error("Error checking unseen replies:", error);
      }
    }
  }
};
</script>

<style scoped>
/* Global Styling */
.course-page {
  font-family: 'Arial', sans-serif;
  background-color: #f8f9fa;
  color: #333;
  min-height: 100vh;
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
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Courses Content */
.courses-content {
  width: 100%;
}

/* Courses Container */
.courses-container {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

/* Course Cards */
.course-card {
  flex: 1;
  max-width: calc(33.33% - 20px);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.course-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

/* Question Block (used for course cards) */
.question-block {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  border-top: 5px solid #3498db;
}

.course-icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
  background-color: #f0f7ff;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.question-text {
  font-weight: bold;
  font-size: 1.4rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.course-description {
  font-family: 'Open Sans', sans-serif;
  color: #555;
  line-height: 1.6;
  margin-bottom: 20px;
  font-size: 0.95rem;
}

/* Course Details */
.course-details {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  margin: 15px 0;
}

.detail-item {
  font-size: 0.9rem;
  color: #555;
  font-weight: 500;
}

/* Button Container */
.button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* Submit Button (used for View Course) */
.submit-button {
  background-color: #2980b9;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
  text-decoration: none;
}

.submit-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  background-color: #3498db;
}

/* Notification Icon */
.notification-icon {
  width: 30px;
  height: 30px;
  margin-left: 0px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .courses-container {
    flex-direction: column;
    align-items: center;
  }

  .course-card {
    width: 90%;
    max-width: 400px;
  }
}
</style>
