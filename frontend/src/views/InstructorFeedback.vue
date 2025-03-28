<template>
  <div class="feedback-page">
    <nav class="navbar">
      <div class="nav-container">
        <h2 class="nav-title">COURSE FEEDBACKS</h2>
      </div>
    </nav>
        
    <p style="text-align: center; font-size: 1.2rem; margin-top: 20px;">Some Feedbacks about course from students.</p>



    <div v-if="loading" class="loading">
      Loading feedbacks...
    </div>
    
    <div v-else-if="feedbacks.length === 0" class="no-data">
      No feedbacks found.
    </div>
    
    <table v-else class="feedback-table">
      <thead>
        <tr>
          
          <th>FEEDBACK</th>
          <th class="rating-column">RATING</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(feedback, index) in feedbacks" :key="index">
          
          <td>{{ feedback.feed_content }}</td>
          <td class="rating-column">{{ feedback.feed_rating }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "FeedbackPage",
  data() {
  return {
    baseURL: "http://127.0.0.1:5000",
    feedbacks: [
      { student_name: "John Doe", student_email: "john@example.com", feedback_text: "Great course!", rating: 5 }
    ],
    loading: false,
    error: null
  };
/*************  ✨ Codeium Command ⭐  *************/
  /**
   * Lifecycle hook. Fetches the feedbacks when the component is mounted.
   */
/******  9616ffca-8c6b-4333-b39e-300d15a89a8d  *******/ 
},  mounted() {
  console.log("Component mounted");
  this.fetchFeedbacks();
},

  methods: {
    async fetchFeedbacks() {
  console.log("fetchFeedbacks() called");  // Debugging line
  try {
    this.loading = true;
    const response = await axios.get(`${this.baseURL}/api/feedback/full`);
    console.log("API Response:", response.data);  // Check API response
    this.feedbacks = response.data;

    console.log("Feedbacks Array:", this.feedbacks);
  } catch (error) {
    this.error = "Failed to fetch feedbacks. Please try again.";
    console.error("Error fetching feedbacks:", error);
  } finally {
    this.loading = false;
  }
}
  }
};
</script>

<style scoped>
.feedback-page {
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

.feedback-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 5px;
  overflow: hidden;
}

.feedback-table th {
  background-color: #010911;
  color: white;
  padding: 1rem;
  text-align: left;
}

.feedback-table td {
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

.rating-column {
  color: #f39c12; /* Orange for rating */
}

th.name-column, th.email-column, th.rating-column {
  color: white;
}

.feedback-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.feedback-table tr:hover {
  background-color: #f1f1f1;
}

.loading, .no-data {
  text-align: center;
  padding: 2rem;
  color: #666;
}

@media (max-width: 768px) {
  .feedback-table {
    font-size: 0.9rem;
  }
}
</style>
