<template>
    <div>
      <nav class="navbar">
        <div class="nav-container">
          <h2 class="nav-title">Course Portal</h2>
          <ul class="nav-links">
            <li><a href="/">Home</a></li>
            <li><router-link to="/mycourses">My Courses</router-link></li>
            <li><a href="/about">About</a></li>
          </ul>
        </div>
      </nav>
      <div class="courses-container">
        <h1>My Courses</h1>
        <div class="courses-grid">
          <div class="course-card" v-for="course in courses" :key="course.id">
            <h2>{{ course.name }}</h2>
            <p>{{ course.description }}</p>
            <button class="enroll-button" @click="coursepage">View Course</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "MyCoursesView",
    data() {
      return {
        courses: [
          { id: 1, name: "Python", description: "Learn the fundamentals of Python programming." },
          { id: 2, name: "Java", description: "Master Java concepts and object-oriented programming." },
          { id: 3, name: "Statistics-1", description: "Introduction to basic statistical methods and analysis." }
        ]
      };
    },
    methods: {
      coursepage() {
        this.$router.push("/coursepage");
      }
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
  
  .nav-container {
    display: flex;
    align-items: center;
    width: 100%;
    justify-content: space-between;
  }
  
  .nav-title {
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  .nav-links {
    list-style: none;
    display: flex;
    gap: 1.5rem;
  }
  
  .nav-links li {
    display: inline;
  }
  
  .nav-links a {
    color: white;
    text-decoration: none;
    font-weight: 600;
  }
  
  .nav-links a:hover {
    text-decoration: underline;
  }
  
  .courses-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 2rem;
  }
  
  h1 {
    color: #2c3e50;
    margin-bottom: 2rem;
    font-size: 2rem;
  }
  
  .courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    width: 100%;
    max-width: 900px;
  }
  
  .course-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  h2 {
    color: #2c3e50;
    margin-bottom: 1rem;
    font-size: 1.5rem;
  }
  
  p {
    color: #555;
    margin-bottom: 1.5rem;
  }
  
  .enroll-button {
    background: #3498db;
    color: white;
    padding: 0.8rem 1.2rem;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .enroll-button:hover {
    background: #2980b9;
  }
  
  .enroll-button:active {
    transform: scale(0.98);
  }
  </style>
  