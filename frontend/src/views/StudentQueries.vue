<template>
  <div class="student-queries-page">
    <nav class="navbar">
      <div class="nav-container">
        <h2 class="nav-title">My Queries</h2>
        
      </div>
    </nav>

    <div v-if="loading" class="loading">
      Loading your queries...
    </div>

    <div v-else-if="queries.length === 0" class="no-data">
      No queries found.
    </div>

    <table v-else class="queries-table">
      <thead>
        <tr>
          <th>QUERY</th>
          <th>ANSWER</th>
          <th>STATUS</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="query in queries" :key="query.doubt_id">
          <td><b>{{ query.doubt_text }}</b></td>
          <td v-if="query.reply">{{ query.reply }}</td>
          <td v-else>No reply yet</td>
          <td>
            <span v-if="query.reply" class="status-answered">Answered</span>
            <span v-else class="status-pending">Pending</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "StudentQueriesPage",
  data() {
    return {
      queries: [],
      loading: true,
      error: null,
      baseURL: 'http://127.0.0.1:5000',
      user: null
    };
  },
  mounted() {
    this.fetchUserDetails();
    this.fetchQueries();
  },
  methods: {
    fetchUserDetails() {
      // Fetch user details from local storage
      const user = JSON.parse(localStorage.getItem('user'));
      if (user) {
        this.user = user;
      } else {
        alert("User not logged in. Redirecting to login page.");
        this.$router.push('/login'); // Redirect to login page
      }
    },
    async fetchQueries() {
      try {
        this.loading = true;

        // Debugging: Log the student email before marking replies as seen
        console.log("Attempting to mark replies as seen for:", this.user.email);

        // Mark replies as seen
        const markSeenResponse = await axios.post(`${this.baseURL}/api/replies/mark-seen`, {
          student_email: this.user.email
        });

        // Debugging: Log the response from the mark-seen endpoint
        console.log("Mark replies as seen response:", markSeenResponse.data);

        // Fetch updated queries
        const response = await axios.get(`${this.baseURL}/api/student-doubts`);
        this.queries = response.data.filter(query => query.student_email === this.user.email);
      } catch (error) {
        console.error("Error fetching queries or marking replies as seen:", error);
        this.error = "Failed to fetch your queries. Please try again.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.student-queries-page {
  width: 100%;
  margin: 0 auto;
  position: relative;
}

.navbar {
  background: #2c3e50;
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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

.status-answered {
  color: #28a745;
  font-weight: bold;
}

.status-pending {
  color: #dc3545;
  font-weight: bold;
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