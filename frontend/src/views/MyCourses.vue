<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Course Portal</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <router-link to="/" class="nav-link text-white">Home</router-link>
          <router-link to="/mycourses" class="nav-link text-white">My Courses</router-link>
          <router-link to="/about" class="nav-link text-white">About</router-link>
        </div>
      </div>
    </nav>

    <div class="container mt-5">
      <h1 class="text-center">My Courses</h1>
      <div v-if="loading" class="text-center">
        <p>Loading...</p>
      </div>
      <div v-else-if="errorMessage" class="alert alert-danger text-center">
        {{ errorMessage }}
      </div>
      <div v-else class="row justify-content-center">
        <div class="col-md-6 mb-4" v-for="course in courses" :key="course.course_id">
          <div class="card shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">{{ course.name }}</h5>
              <p class="card-text">{{ course.description }}</p>
              <button class="btn btn-primary" @click="goToCourse(course.course_id)">View Course</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MyCoursesView",
  data() {
    return {
      courses: [],
      loading: true,
      errorMessage: "",
    };
  },
  mounted() {
    this.fetchCourses();
  },
  methods: {
    async fetchCourses() {
  this.loading = true;
  this.errorMessage = "";

  try {
    // Directly pass the token (Replace with actual token if needed)
    const token = "your_generated_token_here"; // Replace this manually

    const response = await axios.get("http://127.0.0.1:5000/api/mycourses", {
      headers: { Authorization: `Bearer $eyJ2ZXIiOiI1IiwidWlkIjoib21AdGVzdC5jb20iLCJmc19wYWEiOjE3NDE4NjQzMzYuMDI2MjU1OCwiZXhwIjowfQ.Z9K9kA.83Tn_1DhkxZRw936ZjOGmu3I3TY` },
    });

    if (response.status === 200) {
      this.courses = response.data;
    }
  } catch (error) {
    console.error("API error:", error);
    this.errorMessage = "Failed to load courses. Please try again.";
  } finally {
    this.loading = false;
  }
}

  },
};
</script>

<style scoped>
/* Custom Styling */
.container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
  min-height: 100vh;
}

h1 {
  color: #2c3e50;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card-title {
  color: #2c3e50;
}

.card-text {
  color: #555;
}

.btn-primary {
  background: #3498db;
  border: none;
}

.btn-primary:hover {
  background: #2980b9;
}
</style>
