<template>
  <!-- <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav> -->
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #eeeeee;
  
}
nav {
  padding: 30px;
}
body {
  background-color:#2D2D2D;
}
nav a {
  font-weight: bold;
  color: #4ecca3;
}

nav a.router-link-exact-active {
  color: #393e99;
}
</style>
