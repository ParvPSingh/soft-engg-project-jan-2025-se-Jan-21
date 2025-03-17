<!-- <template>
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
</style> -->


<template>
  <div class="courses-page">
    <header class="header">
      <h1 class="page-title">📚 My Courses</h1>
      <nav class="nav-links">
        <a href="#" class="nav-item">Home</a>
        <a href="#" class="nav-item">My Courses</a>
        <a href="#" class="nav-item">About</a>
      </nav>
    </header>

    <div class="courses-container">
      <div class="course-card">
        <h2>🐍 Python</h2>
        <p>Learn the fundamentals of Python programming.</p>
        <router-link to="/coursepage" class="view-course-button">View Course</router-link>
      </div>

      
    </div>
  </div>
</template>

<style scoped>
/* Background and Layout */
.courses-page {
  font-family: 'Arial', sans-serif;
  text-align: center;
  background: linear-gradient(135deg, #eef2f3 0%, #8e9eab 100%);
  min-height: 100vh;
  padding: 30px 20px;
}

/* Header */
.header {
  background-color: #2c3e50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-radius: 8px;
}

.page-title {
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

/* Courses Container */
.courses-container {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 50px;
  flex-wrap: wrap;
}

/* Course Cards */
.course-card {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 280px;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
}

.course-card h2 {
  font-size: 1.4rem;
  margin-bottom: 10px;
  color: #34495e;
}

.course-card p {
  font-size: 1rem;
  color: #7f8c8d;
  margin-bottom: 15px;
}

/* Buttons */
.view-course-button {
  display: inline-block;
  margin-top: 10px;
  padding: 12px 18px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  font-size: 1rem;
  font-weight: bold;
  transition: background 0.3s ease-in-out, transform 0.2s ease-in-out;
}

.view-course-button:hover {
  background: #217dbb;
  transform: scale(1.05);
}

/* Responsive Design */
@media (max-width: 768px) {
  .courses-container {
    flex-direction: column;
    align-items: center;
  }

  .course-card {
    width: 90%;
    max-width: 350px;
  }
}
</style>
