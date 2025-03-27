<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\views\InstructorView.vue -->
<template>
  <div class="instructor-page">
    <nav class="navbar">
      <div class="nav-container">
        <h2 class="nav-title">Instructor Dashboard</h2>
      </div>
    </nav>

    <div class="content-container">
      <div class="actions">
        <button @click="goToSupplementaryManage" class="manage-content">Manage Supplementary Content</button>
        <button @click="goToEnrolledStudents" class="manage-students">Manage Enrolled Students</button>
        <button @click="goToStudentQueries" class="manage-queries">Manage Students Queries</button>
      </div>

      <div v-if="courses.length" class="section">
        <h3>My Courses</h3>
        <!-- Course content -->
      </div>

      <div v-if="students.length" class="section">
        <h3>Enrolled Students</h3>
        <ul class="list-container">
          <li v-for="student in students" :key="student.id" class="list-item">{{ student.name }} - {{ student.email }}</li>
        </ul>
      </div>

      <div v-if="assignments.length" class="section">
        <h3>Assignments</h3>
        <ul class="list-container">
          <li v-for="assignment in assignments" :key="assignment.assignment_id" class="list-item">
            Assignment #{{ assignment.assignment_no }} - Week {{ assignment.week_no }}
          </li>
        </ul>
      </div>

      <div v-if="feedbacks.length" class="section">
        <h3>Student Feedback</h3>
        <ul class="list-container">
          <li v-for="feedback in feedbacks" :key="feedback.feed_id" class="list-item">
            {{ feedback.feed_content }} - <strong>Rating:</strong> {{ feedback.feed_rating }}/5
          </li>
        </ul>
      </div>
    </div>

    <!-- Add the TA ChatBot component here -->
    <ChatBot_TA />
  </div>
</template>

<script>
import axios from "axios";
import ChatBot_TA from '@/components/ChatBot_TA.vue';

export default {
  name: "InstructorDashboard",
  components: {
    ChatBot_TA
  },
  data() {
    return {
      courses: [],
      students: [],
      assignments: [],
      feedbacks: []
    };
  },
  methods: {
    async fetchCourses() {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        const response = await axios.get(`http://127.0.0.1:5000/api/course/${user.user_id}`, {
          headers: { Authorization: `Bearer ${user.token}` },
        });
        this.courses = response.data;
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    },
    async fetchStudents() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/enrollment/1", {
          headers: { Authorization: `Bearer ${JSON.parse(localStorage.getItem("user")).token}` },
        });
        this.students = response.data;
      } catch (error) {
        console.error("Error fetching students:", error);
      }
    },
    async fetchAssignments() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/assignment/1", {
          headers: { Authorization: `Bearer ${JSON.parse(localStorage.getItem("user")).token}` },
        });
        this.assignments = response.data;
      } catch (error) {
        console.error("Error fetching assignments:", error);
      }
    },
    async fetchFeedback() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/feedback/1", {
          headers: { Authorization: `Bearer ${JSON.parse(localStorage.getItem("user")).token}` },
        });
        this.feedbacks = response.data;
      } catch (error) {
        console.error("Error fetching feedback:", error);
      }
    },
    viewCourse(course_id) {
      this.$router.push(`/course/${course_id}`);
    },
    goToSupplementaryManage() {
      this.$router.push("/supplymentary");
    },
    goToEnrolledStudents() {
      this.$router.push("/enrolled-students");
    },
    goToStudentQueries() {
      this.$router.push("/student-queries");
    }
  },
  mounted() {
    this.fetchCourses();
    this.fetchStudents();
    this.fetchAssignments();
    this.fetchFeedback();
  }
};
</script>
<style scoped>
.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.manage-content { background: #007bff; color: white; }
.manage-students { background: #28a745; color: white; }
.manage-queries { background: #dc3545; color: white; }

.section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 80%;
  margin-bottom: 2rem;
}

.list-container {
  list-style: none;
  padding: 0;
}

.list-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.manage {
  background: #007bff;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}
</style>
