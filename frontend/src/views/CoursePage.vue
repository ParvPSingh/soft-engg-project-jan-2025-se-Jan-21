<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\views\CoursePage.vue -->
<template>
  <div class="course-page">
    <header class="header">
      <h1 class="course-title">Python Course</h1>
      <nav class="nav-links">
        <router-link to="/" class="nav-item">Home</router-link>
        <router-link to="mycourses" class="nav-item">My Courses</router-link>
        <router-link to="studentqueries" class="nav-item">My Queries</router-link>
        
        <router-link to="aboutpage" class="nav-item">About</router-link>
      </nav>
    </header>

    <div class="container">
      <!-- Sidebar -->
      <aside class="sidebar">
        <h2 class="sidebar-title">📚 Course Outline</h2>
        <div v-for="week in weeks" :key="week.week_no" class="week">
          <div @click="toggleWeek(week.week_no)" class="week-title">
            Week {{ week.week_no }} 
            <span class="toggle-icon">{{ openWeeks.includes(week.week_no) ? '▲' : '▼' }}</span>
          </div>

          <div v-if="openWeeks.includes(week.week_no)" class="week-content">
            <div v-for="lecture in week.lectures" :key="lecture.lecture_id" class="lecture-title" @click="toggleLecture(lecture.lecture_id)">
              🎥 {{ lecture.lecture_no }}. {{ lecture.title }}
            </div>

            <!-- Supplementary Materials Section -->
            <div class="supplementary-section">
              <div class="supplementary-header">
                📚 Supplementary Materials
              </div>
              <div v-if="supplementaryMaterials[week.week_no] && supplementaryMaterials[week.week_no].length > 0">
                <div v-for="material in supplementaryMaterials[week.week_no]" :key="material.id" class="supplementary-item">
                  <a @click="viewSupplementary(material.file_url)" class="supplementary-link">
                    📄 {{ material.file_name }}
                  </a>
                </div>
              </div>
              <div v-else class="no-supplementary">
                No supplementary materials available
              </div>
            </div>

            <router-link to="prassignment" class="assignment-link">📝 Graded Assignment</router-link>
            <router-link to="prgassignment" class="assignment-link">💻 Programming Assignment</router-link>
          </div>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="content">
        <div v-if="currentLecture" class="lecture-view">
          <h2 class="lecture-title">{{ currentLecture.title }}</h2>
          <iframe width="560" height="315" :src="currentLecture.video_link" frameborder="0" allowfullscreen></iframe>
          <p class="transcript">📜 Transcripts will appear here...</p>
        </div>
        <div class="doubt-section">
          <h3>Ask a Question</h3>
          <textarea 
            v-model="doubtText" 
            placeholder="Type your question here"
            class="doubt-textarea"
          ></textarea>
          <button @click="submitDoubt" :disabled="!isValid" class="submit-button">
            Submit Question
          </button>
        </div>
      </main>
    </div>
    <ChatBot_Student />
  </div>
</template>

<script>
import ChatBot_Student from '@/components/ChatBot_Student.vue';
import axios from 'axios';

export default {
  components: {
    ChatBot_Student
  },
  data() {
    return {
      doubtText: '',
      studentName: 'John Doe', // Replace with actual student name
      openWeeks: [],
      currentLecture: null,
      // New data property for supplementary materials
      supplementaryMaterials: {},
      courseId: 1, // Default to course ID 1
      weeks: [
        {
          week_no: 1,
          lectures: [
            { lecture_id: 1, lecture_no: "1.1", title: "Introduction", video_link: "https://www.youtube.com/embed/8ndsDXohLMQ" },
            { lecture_id: 2, lecture_no: "1.2", title: "Introduction to Replit", video_link: "https://www.youtube.com/embed/NgZZ0HIUqbs" },
            { lecture_id: 3, lecture_no: "1.3", title: "A Quick Introduction to Variables", video_link: "https://www.youtube.com/embed/Yg6xzi2ie5s" },
            { lecture_id: 4, lecture_no: "1.4", title: "Variables and Literals", video_link: "https://www.youtube.com/embed/tDaXdoKfX0k" },
            { lecture_id: 5, lecture_no: "1.5", title: "Data Types", video_link: "https://www.youtube.com/embed/8n4MBjuDBu4" },
            { lecture_id: 6, lecture_no: "1.6", title: "Operators and Expressions", video_link: "https://www.youtube.com/embed/8pu73HKzNOE" },
            { lecture_id: 7, lecture_no: "1.7", title: "Intro to Strings", video_link: "https://www.youtube.com/embed/sS89tiDuqoM" }
          ]
        },
        {
          week_no: 2,
          lectures: [
            { lecture_id: 8, lecture_no: "2.1", title: "Variables", video_link: "https://www.youtube.com/embed/XZSnqseRbZY" },
            { lecture_id: 9, lecture_no: "2.2", title: "String Methods", video_link: "https://www.youtube.com/embed/bRAo6TJJjCU" },
            { lecture_id: 10, lecture_no: "2.3", title: "Introduction to the if Statement", video_link: "https://www.youtube.com/embed/FTX5wF_3J9Q" },
            { lecture_id: 11, lecture_no: "2.4", title: "If, Else, and Elif Conditions", video_link: "https://www.youtube.com/embed/-dBqiRCHbNw" },
            { lecture_id: 12, lecture_no: "2.5", title: "Introduction to Import Library", video_link: "https://www.youtube.com/embed/OdjXL5U95eI" }
          ]
        },
        {
          week_no: 3,
          lectures: [
            { lecture_id: 13, lecture_no: "3.1", title: "Introduction to For Loop", video_link: "https://www.youtube.com/embed/lvXuQ_x7EsI" },
            { lecture_id: 14, lecture_no: "3.2", title: "While Loop", video_link: "https://www.youtube.com/embed/SqMeT9caxpE" },
            { lecture_id: 15, lecture_no: "3.3", title: "Formatted Printing", video_link: "https://www.youtube.com/embed/DR0BhSzGnPo" },
            { lecture_id: 16, lecture_no: "3.4", title: "Nested For Loop", video_link: "https://www.youtube.com/embed/-4MRaWABCuo" },
            { lecture_id: 17, lecture_no: "3.5", title: "Break, Continue, and Pass", video_link: "https://www.youtube.com/embed/SVAVQHfJbE0" }
          ]
        }
      ]
    };
  },
  
  mounted() {
    // Initialize by fetching supplementary materials
    this.fetchSupplementaryMaterials();
  },
  
  methods: {
    toggleWeek(weekNo) {
      if (this.openWeeks.includes(weekNo)) {
        this.openWeeks = this.openWeeks.filter((w) => w !== weekNo);
      } else {
        this.openWeeks.push(weekNo);
        // Fetch supplementary materials when opening a week
        this.fetchWeekSupplementaryMaterials(weekNo);
      }
    },
    
    toggleLecture(lectureId) {
      this.currentLecture = this.weeks.flatMap(week => week.lectures).find(lecture => lecture.lecture_id === lectureId);
    },
    
    // Method to fetch all supplementary materials
    async fetchSupplementaryMaterials() {
      try {
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user || !user.token) {
          console.error('User is not authenticated');
          return;
        }
        
        // Initialize an empty object for all weeks
        const materials = {};
        
        // Fetch materials for each week
        for (const week of this.weeks) {
          const weekNo = week.week_no;
          materials[weekNo] = await this.fetchWeekSupplementaryMaterials(weekNo);
        }
        
        this.supplementaryMaterials = materials;
      } catch (error) {
        console.error('Error fetching all supplementary materials:', error);
      }
    },
    
    // Method to fetch supplementary materials for a specific week
    async fetchWeekSupplementaryMaterials(weekNo) {
      try {
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user || !user.token) {
          console.error('User is not authenticated');
          return [];
        }
        
        const response = await axios.get(
          `http://127.0.0.1:5000/api/supplementary/${this.courseId}/${weekNo}`,
          {
            headers: {
              'Authorization': `Bearer ${user.token}`
            }
          }
        );
        
        // Update the specific week's materials
        this.supplementaryMaterials = {
          ...this.supplementaryMaterials,
          [weekNo]: response.data || []
        };
        
        return response.data || [];
      } catch (error) {
        console.error(`Error fetching supplementary materials for week ${weekNo}:`, error);
        return [];
      }
    },
    
    // Method to view supplementary PDF
    viewSupplementary(fileUrl) {
      if (fileUrl) {
        // Make sure to prepend the base URL if needed
        const absoluteUrl = fileUrl.startsWith('http') 
          ? fileUrl 
          : `http://127.0.0.1:5000${fileUrl}`;
        
        window.open(absoluteUrl, '_blank');
      } else {
        console.error('Invalid file URL');
      }
    },
    
    async submitDoubt() {
      if (!this.isValid || !this.currentLecture) {
        alert('Please select a lecture before submitting a doubt.');
        return;
      }

      // Retrieve user details from localStorage
      const userData = JSON.parse(localStorage.getItem('user'));

      if (!userData || !userData.name || !userData.email) {
        alert('User information is missing. Please log in again.');
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/submit-doubt', {
          doubtText: this.doubtText,
          videoTitle: this.currentLecture.title, // Send title instead of ID
          studentName: userData.name, // Send student name
          studentEmail: userData.email // Send student email
        });

        if (response.status === 201 || response.status === 200) {
          alert('Your question has been submitted successfully!');
          this.doubtText = '';
        } else {
          throw new Error('Failed to submit question');
        }
      } catch (error) {
        console.error('Error submitting doubt:', error);
        alert('Failed to submit your question. Please try again.');
      }
    }
  },
  
  computed: {
    isValid() {
      return this.doubtText.trim() !== '';
    }
  }
};
</script>

<style scoped>
/* Global Styling */
.course-page {
  font-family: 'Arial', sans-serif;
  background-color: #f8f9fa;
  color: #333;
}

/* Header */
.header {
  background-color: #2c3e50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
}

.course-title {
  font-size: 1.8rem;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-item {
  color: white;
  text-decoration: none;
  font-size: 1rem;
  transition: 0.3s ease-in-out;
}

.nav-item:hover {
  color: #f39c12;
}

/* Container Layout */
.container {
  display: flex;
  gap: 20px;
  padding: 20px;
}

/* Sidebar */
.sidebar {
  width: 30%;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.sidebar-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: #34495e;
}

.week-title {
  cursor: pointer;
  font-weight: bold;
  padding: 10px;
  background: #ecf0f1;
  border-radius: 5px;
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: 0.3s;
}

.week-title:hover {
  background: #d5dbdb;
}

.toggle-icon {
  font-size: 1.2rem;
}

.lecture-title {
  cursor: pointer;
  color: #2980b9;
  margin: 8px 0;
  transition: 0.3s;
  padding-left: 10px;
}

.lecture-title:hover {
  text-decoration: underline;
}

/* Supplementary Materials Styling */
.supplementary-section {
  margin-top: 15px;
  border-left: 3px solid #3498db;
  padding-left: 10px;
}

.supplementary-header {
  font-weight: bold;
  color: #3498db;
  margin-bottom: 8px;
}

.supplementary-item {
  margin: 8px 0;
}

.supplementary-link {
  color: #16a085;
  cursor: pointer;
  display: block;
  transition: 0.2s;
  text-decoration: none;
}

.supplementary-link:hover {
  color: #1abc9c;
  transform: translateX(5px);
}

.no-supplementary {
  font-style: italic;
  color: #95a5a6;
  font-size: 0.9rem;
  margin: 5px 0;
}

/* Assignment Links */
.assignment-link {
  display: block;
  color: #e74c3c;
  font-weight: bold;
  margin-top: 10px;
  text-decoration: none;
  padding-left: 10px;
  transition: 0.3s ease-in-out;
}

.assignment-link:hover {
  color: #c0392b;
}

/* Main Content */
.content {
  width: 65%;
  text-align: center;
}

.lecture-view {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.lecture-title {
  font-size: 1.5rem;
  color: #2c3e50;
}

.transcript {
  font-size: 1rem;
  color: #7f8c8d;
  margin-top: 10px;
}

.doubt-section {
  margin-top: 20px;
  text-align: left;
}

.doubt-textarea {
  width: 100%;
  height: 150px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
}

.submit-button {
  background-color: #2980b9;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>