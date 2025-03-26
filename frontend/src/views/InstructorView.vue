<template>
  <div class="container mt-4">
    <h1 class="text-center">Instructor Dashboard</h1>
    <br>
    <hr>
    <br>

    <!-- Centered Button for Supplementary Content Management -->
    <div class="text-center mt-3">
      <button @click="goToSupplementaryManage" class="btn btn-primary btn-lg">
        Manage Supplementary Content
      </button>
    </div>

    <!-- Courses Section -->
    <div v-if="courses.length" class="section mt-4">
      <h2>My Courses</h2>
      <div class="list-group">
        <div
          v-for="course in courses"
          :key="course.course_id"
          class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
        >
          <div>
            <h5>{{ course.name }}</h5>
            <p>{{ course.description }}</p>
          </div>
          <button @click="viewCourse(course.course_id)" class="btn btn-primary">Manage</button>
        </div>
      </div>
    </div>

    <!-- Students Section -->
    <div v-if="students.length" class="section mt-4">
      <h2>Enrolled Students</h2>
      <ul class="list-group">
        <li v-for="student in students" :key="student.id" class="list-group-item">
          {{ student.name }} - {{ student.email }}
        </li>
      </ul>
    </div>

    <!-- Assignments Section -->
    <div v-if="assignments.length" class="section mt-4">
      <h2>Assignments</h2>
      <ul class="list-group">
        <li v-for="assignment in assignments" :key="assignment.assignment_id" class="list-group-item">
          Assignment #{{ assignment.assignment_no }} - Week {{ assignment.week_no }}
        </li>
      </ul>
    </div>

    <!-- Feedback Section -->
    <div v-if="feedbacks.length" class="section mt-4">
      <h2>Student Feedback</h2>
      <ul class="list-group">
        <li v-for="feedback in feedbacks" :key="feedback.feed_id" class="list-group-item">
          {{ feedback.feed_content }} - <strong>Rating:</strong> {{ feedback.feed_rating }}/5
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "InstructorDashboard",
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
    async viewCourse(course_id) {
      this.$router.push(`/course/${course_id}`);
    },
    goToSupplementaryManage() {
      this.$router.push("/supplymentary"); // Redirects to supplementary content page
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
.container {
  max-width: 900px;
  margin: auto;
}
.section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
h1, h2 {
  color: #2c3e50;
}
.list-group-item {
  font-size: 1.1rem;
}
</style>
