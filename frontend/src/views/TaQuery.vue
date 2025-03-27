<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\views\TaQuery.vue -->
<template>
  <div class="ta-queries-page">
    <nav class="navbar">
      <div class="nav-container">
        <h2 class="nav-title">TA [ STUDENT QUERIES ]</h2>
      </div>
    </nav>
    
    <div v-if="loading" class="loading">
      Loading student queries...
    </div>
    
    <div v-else-if="doubts.length === 0" class="no-data">
      No student queries found.
    </div>
    
    <table v-else class="queries-table">
      <thead>
        <tr>
          <th class="name-column">NAME</th>
          <th class="email-column">EMAIL</th>
          <th>QUERY</th>
          <th class="video-column">VIDEO</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="doubt in doubts" :key="doubt.doubt_id">
          <td class="name-column">{{ doubt.student_name }}</td>
          <td class="email-column">{{ doubt.student_email }}</td>
          <td>{{ doubt.doubt_text }}</td>
          <td class="video-column">{{ doubt.video_title }}</td>
        </tr>
      </tbody>
    </table>
    
    <!-- Remove static chatbot aside and only use the dynamic component -->
    <ChatBot_TA />
  </div>
</template>

<script>
import axios from 'axios';
import ChatBot_TA from '@/components/ChatBot_TA.vue';

export default {
  name: "TAQueriesPage",
  components: {
    ChatBot_TA
  },
  data() {
    return {
      doubts: [],
      loading: true,
      error: null,
      baseURL: 'http://127.0.0.1:5000'
    };
  },
  mounted() {
    this.fetchDoubts();
  },
  methods: {
    async fetchDoubts() {
      try {
        this.loading = true;
        const response = await axios.get(`${this.baseURL}/api/student-doubts`);
        this.doubts = response.data;
      } catch (error) {
        this.error = "Failed to fetch student queries. Please try again.";
        console.error("Error fetching doubts:", error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.ta-queries-page {
  width: 100%;
  margin: 0 auto;
  position: relative;
}

.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
  width: 100%;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.nav-title {
  margin: 0;
  font-size: 1.8rem;
}

.queries-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 5px;
  overflow: hidden;
}

.queries-table th {
  background-color: #010911;
  color: white;
  padding: 1rem;
  text-align: left;
}

.queries-table td {
  border-bottom: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

/* Different colors for specific columns */
.name-column {
  color: #3498db; /* Blue for name */
  font-weight: bold;
}

.email-column {
  color: #9b59b6; /* Purple for email */
}

.video-column {
  color: #e74c3c; /* Red for video */
}

/* Keep the header text white */
th.name-column, th.email-column, th.video-column {
  color: white;
}

.queries-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.queries-table tr:hover {
  background-color: #f1f1f1;
}

.loading, .no-data {
  text-align: center;
  padding: 2rem;
  color: #666;
}

@media (max-width: 768px) {
  .queries-table {
    font-size: 0.9rem;
  }
}
</style>