<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\views\TaPage.vue -->
<template>
  <div class="ta-page">
    <nav class="navbar">
      <div class="nav-container">
        <h2 class="nav-title">TA - Python Course</h2>
      </div>
    </nav>
    
    <div class="content-container">
      <div class="actions">
        <button class="review-students">Review Students</button>
        <button class="approve-registration">Approve Registration</button>
        <router-link to="/taquery"><button class="student-queries">Student Queries</button></router-link>
      </div>
      
      <div class="analytics">
        <h3>Average Assignment Scores</h3>
        <img src="../assets/tagraph.png" alt="Assignment Scores Chart" style="width: 80%;" class="analytics-image" />
      </div>
    </div>
    
    <!-- Add the TA ChatBot component here -->
    <ChatBot_TA />
  </div>
</template>

<script>
import ChatBot_TA from '@/components/ChatBot_TA.vue';

export default {
  name: "TAPythonPage",
  components: {
    ChatBot_TA
  }
};
</script>

<style scoped>
/* Your existing styles */
.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 600;
}

.content-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.actions {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.review-students { background: #28a745; color: white; }
.approve-registration { background: #007bff; color: white; }
.student-queries { background: #dc3545; color: white; }

.analytics {
  margin-bottom: 2rem;
  text-align: center;
}

.analytics-image {
  width: 300px;
  height: auto;
}
</style>
