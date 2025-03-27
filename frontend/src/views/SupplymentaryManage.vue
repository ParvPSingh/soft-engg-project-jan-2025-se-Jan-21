<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\views\SupplymentaryManage.vue -->
<template>
  <div class="container mt-4" v-if="isInstructor">
    <h1 class="text-center">Supplementary Content</h1>

    <!-- File Upload Section -->
    <div class="upload-section">
      <h3>Upload PDF</h3>
      <form @submit.prevent="uploadFile">
        <div class="form-group">
          <label for="upload-week">Select Week:</label>
          <select id="upload-week" v-model="selectedUploadWeek" class="form-control">
            <option v-for="week in weeks" :key="week" :value="week">Week {{ week }}</option>
          </select>
        </div>

        <div class="form-group">
          <label for="file">Choose PDF:</label>
          <input type="file" id="file" ref="fileInput" @change="handleFileUpload" class="form-control-file" accept="application/pdf">
        </div>

        <button type="submit" class="btn btn-primary mt-2">Upload</button>
      </form>
    </div>

    <!-- Uploaded Files Section -->
    <div class="files-section mt-4">
      <h3>Uploaded PDFs</h3>

      <!-- Week Selector for Viewing Uploaded PDFs -->
      <div class="form-group">
        <label for="view-week">Select Week to View:</label>
        <select id="view-week" v-model="selectedViewWeek" class="form-control" @change="fetchUploadedFiles">
          <option v-for="week in weeks" :key="week" :value="week">Week {{ week }}</option>
        </select>
      </div>

      <!-- Display Files or Message If No Files Exist -->
      <ul v-if="uploadedFiles.length" class="list-group">
        <li v-for="pdf in uploadedFiles" :key="pdf.id" class="list-group-item d-flex justify-content-between align-items-center">
          <span>{{ pdf.file_name }} (Week {{ pdf.week_no }})</span>
          <div>
            <button @click="viewFile(pdf.file_url)" class="btn btn-success btn-sm mr-2">View</button> | 
            <button @click="deleteFile(pdf.id)" class="btn btn-danger btn-sm">Delete</button>
          </div>
        </li>
      </ul>
      <p v-else class="text-muted">No files uploaded yet for Week {{ selectedViewWeek }}.</p>
    </div>
    
    <!-- Add TA ChatBot -->
    <ChatBot_TA />
  </div>

  <!-- Access Denied Message -->
  <div v-else class="access-denied">
    <h2>⛔ Access Denied</h2>
    <p>You do not have permission to view this page.</p>
  </div>
</template>

<script>
import axios from "axios";
import ChatBot_TA from '@/components/ChatBot_TA.vue';

export default {
  name: "SupplementaryContent",
  components: {
    ChatBot_TA
  },
  data() {
    return {
      isInstructor: false, // RBAC Check
      selectedUploadWeek: "",
      selectedViewWeek: 1,
      file: null,
      uploadedFiles: [],
      weeks: Array.from({ length: 12 }, (_, i) => i + 1),
    };
  },
  methods: {
    // Handle file selection
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },

    // Upload File
    async uploadFile() {
      if (!this.selectedUploadWeek) {
        alert("⚠️ Please select a week before uploading.");
        return;
      }
      if (!this.file) {
        alert("⚠️ Please select a file before uploading.");
        return;
      }

      const user = JSON.parse(localStorage.getItem("user"));
      if (!user || !user.token) {
        alert("⚠️ User is not authenticated.");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.file);
      formData.append("course_id", 1);
      formData.append("week_no", this.selectedUploadWeek);

      try {
        const response = await axios.post("http://127.0.0.1:5000/api/supplementary", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            "Authorization": `Bearer ${user.token}`,
          },
        });

        console.log("✅ File uploaded successfully:", response.data);
        alert("✅ File uploaded successfully!");

        this.file = null;
        this.$refs.fileInput.value = "";
        this.fetchUploadedFiles();
      } catch (error) {
        console.error("❌ Error uploading file:", error.response ? error.response.data : error.message);
        alert("❌ Error uploading file. Please try again.");
      }
    },

    // Fetch Uploaded Files for the Selected Week
    async fetchUploadedFiles() {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        if (!user || !user.token) {
          console.error("User is not authenticated.");
          return;
        }

        const response = await axios.get(`http://127.0.0.1:5000/api/supplementary/1/${this.selectedViewWeek}`, {
          headers: {
            "Authorization": `Bearer ${user.token}`,
          },
        });

        this.uploadedFiles = response.data;
        console.log(`📂 Fetched files for Week ${this.selectedViewWeek}:`, response.data);
      } catch (error) {
        console.error("❌ Error fetching uploaded files:", error.response ? error.response.data : error.message);
        this.uploadedFiles = [];
      }
    },

    // View a PDF File
    viewFile(fileUrl) {
      if (fileUrl) {
        const absoluteUrl = `http://127.0.0.1:5000${fileUrl}`;
        window.open(absoluteUrl, "_blank");
      } else {
        console.error("❌ Invalid file URL.");
      }
    },

    // Delete a File
    async deleteFile(fileId) {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        if (!user || !user.token) {
          console.error("User is not authenticated.");
          return;
        }

        await axios.delete(`http://127.0.0.1:5000/api/supplementary/${fileId}`, {
          headers: {
            "Authorization": `Bearer ${user.token}`,
          },
        });

        console.log("🗑️ File deleted successfully");
        alert("🗑️ File deleted successfully!");
        this.fetchUploadedFiles();
      } catch (error) {
        console.error("❌ Error deleting file:", error.response ? error.response.data : error.message);
        alert("❌ Error deleting file. Please try again.");
      }
    },

    // Check User Role for RBAC
    checkUserRole() {
      const user = JSON.parse(localStorage.getItem("user"));
      if (user && user.role === "Instructor") {
        this.isInstructor = true;
      } else {
        this.isInstructor = false;
        alert("⛔ You do not have access to this page.");
        this.$router.push("/"); // Redirect to home page if unauthorized
      }
    },
  },

  mounted() {
    this.checkUserRole();
    if (this.isInstructor) {
      this.fetchUploadedFiles();
    }
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}
.upload-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.files-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
h1, h3 {
  color: #2c3e50;
}
.access-denied {
  text-align: center;
  margin-top: 50px;
  color: red;
}
</style>
