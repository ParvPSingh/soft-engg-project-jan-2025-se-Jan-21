<template>
  <div>
    <h1>Manage Students</h1>
    <table v-if="students.length">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.user_id">
          <td>{{ student.name }}</td>
          <td>{{ student.email }}</td>
          <td>{{ student.active ? "Active" : "Blocked" }}</td>
          <td>
            <button
              :class="student.active ? 'block-button' : 'unblock-button'"
              @click="toggleBlock(student)"
            >
              {{ student.active ? "Block" : "Unblock" }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No students enrolled.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      students: [],
    };
  },
  created() {
    this.fetchStudents();
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/enrolled-students");
        if (response.ok) {
          const data = await response.json();
          if (data && Array.isArray(data.students)) {
            const uniqueStudents = Array.from(
              new Map(data.students.map((student) => [student.user_id, student])).values()
            ); // Remove duplicates
            this.students = uniqueStudents.filter(
              (student) =>
                !["instructor@ds.study.iitm.ac.in", "ta@ds.study.iitm.ac.in"].includes(student.email)
            );
          } else {
            console.error("Unexpected response format:", data);
          }
        } else {
          console.error("Failed to fetch students:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching students:", error);
      }
    },
    async toggleBlock(student) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/user/${student.user_id}/block`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ active: !student.active }),
        });
        if (response.ok) {
          const data = await response.json(); // Parse the response JSON
          if (data && data.message) {
            const index = this.students.findIndex((s) => s.user_id === student.user_id);
            if (index !== -1) {
              this.students[index].active = !this.students[index].active; // Update the student in the array directly
            }
            alert(data.message); // Show the success message from the API
          } else {
            console.error("Unexpected API response:", data);
            alert("An unexpected error occurred. Please try again.");
          }
        } else {
          console.error("Failed to toggle block status:", response.statusText);
          alert(`Failed to toggle block status: ${response.statusText}`);
        }
      } catch (error) {
        console.error("Error toggling block status:", error);
        alert("An error occurred while toggling the block status. Please check your network connection and try again.");
      }
    },
  },
};
</script>

<style scoped>
h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}

p {
  text-align: center;
  color: #888;
  font-style: italic;
}

.block-button {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
}

.unblock-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
}

.block-button:hover {
  background-color: #e60000;
}

.unblock-button:hover {
  background-color: #45a049;
}
</style>