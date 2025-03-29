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
          <th class="reply-column">REPLY</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="doubt in doubts" :key="doubt.doubt_id">
          <td class="name-column">{{ doubt.student_name }}</td>
          <td class="email-column">{{ doubt.student_email }}</td>
          <td><b>{{ doubt.doubt_text }}</b></td>
          <td class="video-column">{{ doubt.video_title }}</td>
          <td class="reply-column">
            <!-- Show "View Reply" button if a reply exists -->
            <div v-if="doubt.reply">
              <button class="view-reply-button" @click="fetchReply(doubt)">View Reply</button>
              <div v-if="doubt.showReplyBox" class="reply-display">
                <p>{{ doubt.reply }}</p>
                <button class="close-button" @click="doubt.showReplyBox = false">Close</button>
              </div>
            </div>
            <!-- Show "Reply" button if no reply exists -->
            <div v-else>
              <div v-if="doubt.showReplyBox">
                <textarea v-model="doubt.replyText" placeholder="Enter your reply here"></textarea>
                <button @click="submitReply(doubt)">Submit</button>
                <button @click="doubt.showReplyBox = false">Cancel</button>
              </div>
              <button v-else @click="doubt.showReplyBox = true">Reply</button>
            </div>
          </td>
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
        this.doubts = response.data.map(doubt => ({
          ...doubt,
          showReplyBox: false,
          replyText: ''
        }));
      } catch (error) {
        this.error = "Failed to fetch student queries. Please try again.";
        console.error("Error fetching doubts:", error);
      } finally {
        this.loading = false;
      }
    },
    async submitReply(doubt) {
      if (!doubt.replyText.trim()) {
        alert("Reply cannot be empty.");
        return;
      }
      try {
        const response = await axios.post(`${this.baseURL}/api/doubts/reply`, {
          doubt_id: doubt.doubt_id,
          reply: doubt.replyText
        });
        alert("Reply submitted successfully!");
        doubt.reply = doubt.replyText; // Update the reply in the UI
        doubt.replyText = '';
        doubt.showReplyBox = false;
      } catch (error) {
        console.error("Error submitting reply:", error);
        alert("Failed to submit reply. Please try again.");
      }
    },
    async fetchReply(doubt) {
      try {
        const response = await axios.get(`${this.baseURL}/api/doubts/${doubt.doubt_id}/reply`);
        doubt.reply = response.data.reply; // Update the reply in the UI
        doubt.showReplyBox = true;
      } catch (error) {
        console.error("Error fetching reply:", error);
        alert("Failed to fetch reply. Please try again.");
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

textarea {
  width: 100%;
  height: 60px;
  margin-bottom: 10px;
  resize: none;
}

button {
  margin-right: 5px;
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color: #ddd;
}

.reply-column button {
  background-color: #3498db;
  color: white;
}

.reply-column button:hover {
  background-color: #2980b9;
}

.view-reply-button {
  background-color: #28a745; /* Green for "View Reply" */
  color: white;
}

.view-reply-button:hover {
  background-color: #218838;
}

.close-button {
  background-color: #dc3545; /* Red for "Close" */
  color: white;
}

.close-button:hover {
  background-color: #c82333;
}

.reply-display {
  margin-top: 10px;
  padding: 10px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
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