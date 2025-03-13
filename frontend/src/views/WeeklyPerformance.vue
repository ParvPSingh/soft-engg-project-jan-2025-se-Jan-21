<template>
    <div class="performance-report">
      <nav class="navbar">
        <div class="nav-container">
          <h2 class="nav-title">PYTHON - Weekly Performance Reports</h2>
        </div>
      </nav>
      
      <div class="content">
        <aside class="sidebar">
          <h3>Course Introduction</h3>
          <ul>
            <li>Week 1</li>
            <ul>
              <li>1.1 Introduction</li>
              <li>1.2 Variables</li>
              <li>Practice Assignment 1</li>
              <li>Graded Assignment 1</li>
              <li>PPA 1</li>
              <li>GrPA 1</li>
              <li><strong>Week 1 Summary & Performance</strong></li>
            </ul>
          </ul>
        </aside>
        
        <main class="report-content">
          <h3>Your Week 1 Performance Report!</h3>
          <section class="report-details">
            <h4>Week 1 Report:</h4>
            <ul>
              <li>Variables & Literals</li>
              <li>Data Types</li>
              <li>Operators & Expressions</li>
              <li>Strings</li>
            </ul>
            <p><strong>Graded Assignment Score:</strong> 85%</p>
            <h4>Areas for Improvement:</h4>
            <ul>
              <li>Misunderstood string slicing concepts</li>
              <li>Errors in operator precedence questions</li>
            </ul>
            <h4>Recommended Study Materials:</h4>
            <ul>
              <li>W3Schools - Python Strings</li>
              <li>GeeksforGeeks - Python Operators</li>
            </ul>
          </section>
        </main>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "WeeklyPerformanceReport"
  };
  </script>
  
  <style scoped>
  .navbar {
    background: #2c3e50;
    color: white;
    padding: 1rem;
    text-align: center;
  }
  
  .content {
    display: flex;
    margin: 1rem;
  }
  
  .sidebar {
    width: 250px;
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
  }
  
  .report-content {
    flex-grow: 1;
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  </style>
  