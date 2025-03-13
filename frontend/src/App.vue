<template>
  <!-- <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav> -->
  <Navbar/>
  <router-view />
</template>

<style></style>

<script>
import Navbar from "./components/NavBar.vue";
export default { components: { Navbar } };
</script>
