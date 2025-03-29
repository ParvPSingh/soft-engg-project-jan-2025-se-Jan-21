<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
      <div class="container-fluid">
        <!-- Logo -->
        <a class="navbar-brand" href="#">
          <img src="../assets/IIT-Madras-01.svg" alt="Logo" class="logo-image" />
        </a>
  
        <!-- Navbar Toggle Button (Mobile) -->
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
  
        <!-- Navbar Items -->
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <!-- Show Login/Register if Not Logged In -->
          <template v-if="!user">
            <button class="btn btn-primary me-2" @click="goToLogin">Login</button>
            <button class="btn btn-warning" @click="goToRegister">Register</button>
          </template>
  
          <!-- Show User Name & Logout Button if Logged In -->
          <template v-else>
            <span class="navbar-text me-3 fw-bold">Welcome, {{ user.name }}</span>
            <template v-if="user.role === 'Student'">
              <!-- <button class="btn btn-success me-2" @click="$router.push('/mycourses')">My Courses</button> -->
            </template>
            <button class="btn btn-danger" @click="handleLogout">Logout</button>
          </template>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  import mitt from "mitt"; // Import event bus
  
  export const eventBus = mitt(); // Create event bus
  
  export default {
    name: "Navbar",
    data() {
      return {
        user: null, // Store logged-in user data
      };
    },
    mounted() {
      this.checkUser();
      eventBus.on("user-updated", this.checkUser); // Listen for login/logout updates
    },
    methods: {
      checkUser() {
        const storedUser = localStorage.getItem("user");
        this.user = storedUser ? JSON.parse(storedUser) : null;
      },
      goToLogin() {
        this.$router.push("/login");
      },
      goToRegister() {
        this.$router.push("/register");
      },
      handleLogout() {
        localStorage.removeItem("user"); // Remove user from storage
        this.user = null;
        eventBus.emit("user-updated"); // Notify other components
        this.$router.push("/"); // Redirect to homepage

        setTimeout(() => {
          window.location.reload(); // Hard reload to clear user state everywhere
        }, 10); // Small delay to allow navigation before reload
      },

    },
  };
  </script>
  
  <style scoped>
  /* Logo Styling */
  .logo-image {
    height: 50px;
    width: auto;
  }
  </style>
  