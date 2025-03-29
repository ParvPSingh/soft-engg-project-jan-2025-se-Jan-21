<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\views\TaPage.vue -->
<template>
  <div class="ta-page">
    <nav class="navbar">
      <div class="nav-container">
        <h2 class="nav-title">TA - Python Course</h2>
      </div>
    </nav>
    
    <div class="content-container">
      <div class="actions">
        <router-link to="/managestudents"><button class="review-students">Review Students</button></router-link>
        <button class="approve-registration">Approve Registration</button>
        <router-link to="/taquery"><button class="student-queries">Student Queries</button></router-link>
      </div>
      
      <div class="analytics">
        <h3>Weekly Average Assignment Scores</h3>
        <canvas id="weeklyAverageChartTaPage"></canvas>
      </div>
    </div>
    
    <!-- Add the TA ChatBot component here -->
    <ChatBot_TA />
  </div>
</template>

<script>
import ChatBot_TA from '@/components/ChatBot_TA.vue';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: "TAPythonPage",
  components: {
    ChatBot_TA
  },
  mounted() {
    this.fetchWeeklyAverageScores();
  },
  methods: {
    async fetchWeeklyAverageScores() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/weekly-average-scores');
        const data = response.data.weekly_averages;
        const labels = Object.keys(data).map(week => `Week ${week}`);
        const scores = Object.values(data);

        this.renderChart(labels, scores);
      } catch (error) {
        console.error("Error fetching weekly average scores:", error);
      }
    },
    renderChart(labels, scores) {
  const ctx = document.getElementById('weeklyAverageChartTaPage').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Average Score',
        data: scores,
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 1500,
        easing: 'easeOutBounce'
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Average Score'
          },
          // ✨ Ensure bars rise from bottom up ✨
          suggestedMin: 0,
          animations: {
            y: {
              from: 0 // Start animation from 0
            }
          }
        },
        x: {
          title: {
            display: true,
            text: 'Weeks'
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `Score: ${context.raw}`;
            }
          }
        }
      }
    }
  });
}

  }
};
</script>

<style scoped>
/* Your existing styles */
.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 600;
}

.content-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.actions {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.review-students { background: #28a745; color: white; }
.approve-registration { background: #007bff; color: white; }
.student-queries { background: #dc3545; color: white; }

.analytics {
  margin-bottom: 2rem;
  text-align: center;
}

.analytics-image {
  width: 300px;
  height: auto;
}

canvas {
  max-height: 300px;
  width: 100%;
  margin-top: 1rem;
}
</style>
