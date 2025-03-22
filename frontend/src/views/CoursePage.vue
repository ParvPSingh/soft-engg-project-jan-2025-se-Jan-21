<!-- <template>
    <div class="course-page">
      <nav class="navbar">
        <div class="nav-container">
          <h2 class="nav-title">Python Course</h2>
          <ul class="nav-links">
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/mycourses">My Courses</router-link></li>
            <li><router-link to="/about">About</router-link></li>
          </ul>
        </div>
      </nav>
      
      <div class="content-container">
        <aside class="sidebar">
          <h3>Course Outline</h3>
          <ul>
            <li>Week 1</li>
            <ul>
              <li>1.1 Introduction</li>
              <li>1.2 Variables</li>
              <li><router-link to="/prassignment"> Practice Assignment 1 </router-link></li>
              <li>Graded Assignment 1</li>
              <li><router-link to="/prgassignment"> PPA 1</router-link></li>
              <li>GPA 1</li>
            </ul>
            <li><router-link to="/weeklyperformance">Weekly Performance Report</router-link></li>
          </ul>
        </aside>
        
        <main class="video-section">
          <h2>L1.1 A Quick Introduction to Variables</h2>
          <iframe 
            width="560" 
            height="315" 
            src="https://www.youtube.com/embed/8ndsDXohLMQ?si=KxAX_tAxLx5lSDk1" 
            title="Python Introduction" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
          </iframe>
          <p>Transcripts will appear here...</p>
        </main>
        
        <aside class="chatbot">
          <h3>Ask your AI Pal - Autobot</h3>
          <img src="../assets/chatbot.png" alt="">
          <div class="chat-box">
            <p><strong>What is a variable in Python?</strong></p>
            <p>In Python, a variable is used to store data that can be referenced and manipulated. It acts as a container for values and does not require explicit declaration of type.</p>
          </div>
          <input type="text" placeholder="Ask a question..." class="chat-input" />
        </aside>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "PythonCoursePage"
  };
  </script>
  
  <style scoped>
  .navbar {
    background: #2c3e50;
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .nav-container {
    display: flex;
    align-items: center;
    width: 100%;
    justify-content: space-between;
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
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    gap: 1rem;
    padding: 2rem;
  }
  
  .sidebar {
    background: #f4f4f4;
    padding: 1rem;
    border-radius: 8px;
  }
  
  .video-section {
    text-align: center;
  }
  
  .chatbot {
    background: #ffe4e1;
    padding: 1rem;
    border-radius: 8px;
  }
  
  .chat-box {
    background: white;
    padding: 0.8rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
  }
  
  .chat-input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  </style>
   -->


   <template>
    <div class="course-page">
      <header class="header">
        <h1 class="course-title">Python Course</h1>

       
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
  
              <router-link to="prassignment" class="assignment-link">📝 Graded Assignment</router-link>
              <router-link to="/programmingassignment" class="assignment-link">💻 Programming Assignment</router-link>
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
        </main>
      </div>
      <ChatBot_Student />
    </div>
  </template>
  
  <script>
import ChatBot_Student from '@/components/ChatBot_Student.vue';


  export default {
    components: {
      ChatBot_Student
    },
    data() {
      return {
        openWeeks: [],
        currentLecture: null,
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


,
          
        ]
      };
    },
    methods: {
      toggleWeek(weekNo) {
        if (this.openWeeks.includes(weekNo)) {
          this.openWeeks = this.openWeeks.filter((w) => w !== weekNo);
        } else {
          this.openWeeks.push(weekNo);
        }
      },
      toggleLecture(lectureId) {
        this.currentLecture = this.weeks.flatMap(week => week.lectures).find(lecture => lecture.lecture_id === lectureId);
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
  </style>
  