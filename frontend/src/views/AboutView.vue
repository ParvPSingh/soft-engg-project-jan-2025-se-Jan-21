<template>
  <div class="about-page">
    <header class="header">
      <h1 class="page-title">📊 Student Profile</h1>
      <nav class="nav-links">
        <router-link to="/" class="nav-item">Home</router-link>
        <router-link to="/mycourses" class="nav-item">My Courses</router-link>
        <router-link to="/aboutpage" class="nav-item">About</router-link>
      </nav>
    </header>
    
    <div class="about-container">
      <div class="profile-header">
        <div class="profile-avatar">
          <span>{{ getInitials(userName) }}</span>
        </div>
        <h1> {{ userName }}</h1>
      </div>
      
      <div class="dashboard-grid">
        <section class="dashboard-card">
          <h2>Academic Information</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">CGPA</span>
              <span class="info-value">8.9</span>
            </div>
            <div class="info-item">
              <span class="info-label">Project CGPA</span>
              <span class="info-value">9.2</span>
            </div>
            <div class="info-item">
              <span class="info-label">Credits Earned</span>
              <span class="info-value">102</span>
            </div>
            <div class="info-item">
              <span class="info-label">Credits Pursuing</span>
              <span class="info-value">12</span>
            </div>
            <div class="info-item">
              <span class="info-label">Courses Completed</span>
              <span class="info-value">24</span>
            </div>
            <div class="info-item">
              <span class="info-label">Current Level </span>
              <span class="info-value">B.S</span>
            </div>
          </div>
        </section>

        <section class="dashboard-card">
          <h2>Current Courses</h2>
          <ul class="course-list">
            <li class="course-item">
              <div class="course-icon">🐍</div>
              <div class="course-name">Python</div>
            </li>
            <li class="course-item">
              <div class="course-icon">JS</div>
              <div class="course-name">Introduction to JavaScript</div>
            </li>
            <li class="course-item">
              <div class="course-icon">🧠</div>
              <div class="course-name">Deep Learning</div>
            </li>
          </ul>
        </section>

        <section class="dashboard-card">
          <h2>Completed Courses (Degree Level)</h2>
          <ul class="course-list">
            <li class="course-item completed">
              <div class="course-icon">✓</div>
              <div class="course-name">Software Testing</div>
            </li>
            <li class="course-item completed">
              <div class="course-icon">✓</div>
              <div class="course-name">Strategies for Professional Growth</div>
            </li>
            <li class="course-item completed">
              <div class="course-icon">✓</div>
              <div class="course-name">AI: Search Methods for Problem Solving</div>
            </li>
          </ul>
        </section>
      </div>
    </div>
    <!-- ChatBot_Student component -->
    <ChatBot_Student />
  </div>
</template>

<script>
import ChatBot_Student from '@/components/ChatBot_Student.vue';

export default {
  name: 'AboutView',
  components: {
    ChatBot_Student
  },
  data() {
    return {
      userName: ''
    }
  },
  mounted() {
  const userData = JSON.parse(localStorage.getItem('user'));
  if (userData && userData.name) {
    this.userName = userData.name; // Correctly extracting the name
  } else {
    this.userName = 'Student';
  }
},

  methods: {
    getInitials(name) {
      if (!name) return 'S';
      return name.split(' ').map(n => n[0]).join('').toUpperCase();
    }
  }
}
</script>

<style scoped>
/* Global Styles */
.about-page {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
  color: #333;
  min-height: 100vh;
}

/* Header & Navbar Styles */
.header {
  background-color: #2c3e50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.page-title {
  font-size: 1.5rem;
  margin: 0;
  color: white;
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
  padding: 8px 12px;
  border-radius: 4px;
}

.nav-item:hover {
  color: #f39c12;
  background-color: rgba(255, 255, 255, 0.1);
}

.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
  color: #f39c12;
}

/* Container Styles */
.about-container {
  max-width: 1000px;
  margin: 30px auto;
  padding: 0 20px;
}

/* Profile Header */
.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  gap: 20px;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  background-color: #3498db;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
  font-weight: bold;
}

.profile-header h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 2.2rem;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.dashboard-card {
  background-color: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.dashboard-card h2 {
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.4rem;
  border-bottom: 2px solid #f1f1f1;
  padding-bottom: 10px;
}

/* Academic Info Grid */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-label {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin-bottom: 5px;
}

.info-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3498db;
}

/* Course Lists */
.course-list {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.course-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding: 12px 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.course-item:hover {
  background-color: #e9ecef;
}

.course-icon {
  width: 35px;
  height: 35px;
  background-color: #3498db;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  color: white;
  font-weight: bold;
  font-size: 1.1rem;
}

.course-item.completed .course-icon {
  background-color: #2ecc71;
}

.course-name {
  font-weight: 500;
}

@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .header {
    flex-direction: column;
    padding: 15px;
  }
  
  .page-title {
    margin-bottom: 15px;
  }
  
  .nav-links {
    width: 100%;
    justify-content: space-around;
  }
}
</style>
