<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\views\TADashboardView.vue -->
<template>
    <div class="ta-dashboard-container">
      <h1>TA Dashboard</h1>
      <ChatBot_TA />
    </div>
  </template>
  
  <script>
  import ChatBot_TA from '@/components/ChatBot_TA.vue';
  
  export default {
    name: "TADashboardView",
    components: {
      ChatBot_TA
    }
  };
  </script>
  
  <style scoped>
  .ta-dashboard-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  }
  </style>