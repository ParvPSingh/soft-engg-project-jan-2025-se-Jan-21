<!-- filepath: d:\Desktop\soft-engg-project-jan-2025-se-Jan-21-main\soft-engg-project-jan-2025-se-Jan-21-main\frontend\src\components\ChatBot_Student.vue -->
<template>
  <div>
    <!-- Chat Bubble Icon -->
    <div
      class="chatbot-icon"
      @click="toggleChat"
      :class="{ bounce: animateBubble }"
    >
      <div class="chat-icon-text">💻</div>
      <div v-if="unreadMessages > 0" class="notification-badge">
        {{ unreadMessages }}
      </div>
    </div>

    <!-- Chat Window Container -->
    <transition name="slide-fade">
      <div v-if="isChatOpen" class="chatbot-container">
        <!-- Chat Header -->
        <div class="chatbot-header">
          <div class="header-left">
            <div class="bot-avatar">AB</div>
            <div class="header-info">
              <h2>Autobot</h2>
              <div class="status-indicator online"></div>
            </div>
          </div>
          <div class="header-actions">
            <button @click="clearChat" class="action-button" title="Clear chat">
              <span class="material-icons">delete_outline</span>
            </button>
            <button
              @click="toggleChat"
              class="action-button"
              title="Close chat"
            >
              <span class="material-icons">close</span>
            </button>
          </div>
        </div>

        <!-- Chat Messages Area -->
        <div class="chatbot-messages" ref="messagesContainer">
          <!-- Welcome Message -->
          <div class="message-date-divider">
            <span>Today</span>
          </div>

          <div class="bot-message-container">
            <div class="bot-avatar">AB</div>
            <div class="bot-message">
              <p>
                Welcome to Autobot! I can help you understand course concepts
                and find information in your course materials. Feel free to ask
                me questions about your Data Science program.
              </p>
              <span class="message-time">{{ getCurrentTime() }}</span>
            </div>
          </div>

          <!-- Message Bubbles -->
          <div v-for="(message, index) in messages" :key="index">
            <div v-if="message.user" class="user-message-container">
              <div class="user-message">
                <p>{{ message.text }}</p>
                <span class="message-time">{{ message.time }}</span>
              </div>
              <div class="user-avatar">YOU</div>
            </div>
            <div v-else class="bot-message-container">
              <div class="bot-avatar">AB</div>
              <div class="bot-message">
                <!-- Use v-html for messages that might contain code blocks -->
                <div v-html="formatMessage(message.text)"></div>
                <span class="message-time">{{ message.time }}</span>
              </div>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="bot-message-container">
            <div class="bot-avatar">AB</div>
            <div class="bot-message typing-indicator">
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
            </div>
          </div>
        </div>

        <!-- Chat Input Area -->
        <div class="chatbot-input">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="Ask about your courses..."
            :disabled="isTyping"
          />
          <button
            @click="sendMessage"
            :disabled="!userInput.trim() || isTyping"
            class="send-button"
          >
            <span class="material-icons">send</span>
          </button>
        </div>

        <!-- Suggested Questions -->
        <div class="suggested-questions" v-if="suggestedQuestions.length > 0">
          <p class="suggestions-title">You might want to ask:</p>
          <div class="suggestions-container">
            <button
              v-for="(question, index) in suggestedQuestions"
              :key="index"
              @click="askSuggestion(question)"
              class="suggestion-button"
            >
              {{ question }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";
import { marked } from "marked";
export default {
  data() {
    return {
      isChatOpen: false,
      userInput: "",
      messages: [],
      isTyping: false,
      unreadMessages: 0,
      session_id: "user_" + Math.random().toString(36).substring(2, 15),
      animateBubble: false,
      suggestedQuestions: [
        "How do Python lists work?",
        "Explain object-oriented programming",
        "What are the course grading components?",
      ],
    };
  },
  methods: {
    formatMessage(text) {
      // Check if the message contains code blocks (```code```)
      marked.setOptions({
        highlight: function (code, lang) {
          if (lang && hljs.getLanguage(lang)) {
            try {
              return hljs.highlight(code, { language: lang }).value;
            } catch (e) {}
          }
          return hljs.highlightAuto(code).value;
        },
        breaks: true, // Enable line breaks in markdown
        gfm: true, // Enable GitHub Flavored Markdown
        sanitize: false, // Allow HTML in the markdown
      });

      if (text.includes("```")) {
        // Split by code block delimiters
        const segments = text.split(/(```[\s\S]*?```)/g);

        return segments
          .map((segment) => {
            // If this is a code block
            if (segment.startsWith("```") && segment.endsWith("```")) {
              // Extract the code and potential language identifier
              let code = segment.slice(3, -3);
              let language = "";

              // Check if the first line specifies a language
              const firstLineEnd = code.indexOf("\n");
              if (firstLineEnd > 0) {
                const potentialLang = code.substring(0, firstLineEnd).trim();
                if (/^[a-zA-Z0-9_]+$/.test(potentialLang)) {
                  language = potentialLang;
                  code = code.substring(firstLineEnd + 1);
                }
              }

              try {
                // Apply syntax highlighting
                const highlighted = language
                  ? hljs.highlight(code, { language }).value
                  : hljs.highlightAuto(code).value;

                return `<pre class="code-block"><code>${highlighted}</code></pre>`;
              } catch (e) {
                // Fallback if highlighting fails
                return `<pre class="code-block"><code>${this.escapeHtml(
                  code
                )}</code></pre>`;
              }
            }

            // Regular text - escape HTML and convert newlines to <br>
            return marked.parse(segment);
          })
          .join("");
      }

      // If no code blocks, just escape HTML and convert newlines
      return this.escapeHtml(text).replace(/\n/g, "<br>");
    },

    // Helper method to escape HTML
    escapeHtml(text) {
      const div = document.createElement("div");
      div.textContent = text;
      return div.innerHTML;
    },

    toggleChat() {
      this.isChatOpen = !this.isChatOpen;
      if (this.isChatOpen) {
        this.unreadMessages = 0;
        // Focus on input field when chat opens
        this.$nextTick(() => {
          const input = this.$el.querySelector(".chatbot-input input");
          if (input) input.focus();
        });
      }
    },
    async sendMessage() {
      if (this.userInput.trim() === "" || this.isTyping) return;

      const currentTime = this.getCurrentTime();

      // Add user message to messages array
      this.messages.push({
        text: this.userInput,
        user: true,
        time: currentTime,
      });

      // Clear user input
      const userQuery = this.userInput;
      this.userInput = "";

      // Scroll to bottom
      this.$nextTick(() => {
        this.scrollToBottom();
      });

      // Show typing indicator
      this.isTyping = true;

      // Send user message to backend and get response
      try {
        const response = await this.getBotResponse(userQuery);

        // Short timeout to simulate typing
        setTimeout(() => {
          // Hide typing indicator
          this.isTyping = false;

          // Add bot response to messages array
          this.messages.push({
            text: response,
            user: false,
            time: this.getCurrentTime(),
          });

          // If chat is closed, show notification
          if (!this.isChatOpen) {
            this.unreadMessages++;
            this.animateBubble = true;
            setTimeout(() => {
              this.animateBubble = false;
            }, 1000);
          }

          // Scroll to bottom
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        }, 1000 + Math.random() * 1000); // Random typing time for realism
      } catch (error) {
        // Handle error
        this.isTyping = false;
        this.messages.push({
          text: "Sorry, I couldn't connect to the server. Please try again later.",
          user: false,
          time: this.getCurrentTime(),
        });

        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    async getBotResponse(message) {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/chatbot/student",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ message, session_id: this.session_id }),
          }
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        return data.response;
      } catch (error) {
        console.error("Error communicating with chatbot API:", error);
        return "Sorry, there was an error connecting to the chatbot server.";
      }
    },
    scrollToBottom() {
      if (this.$refs.messagesContainer) {
        this.$refs.messagesContainer.scrollTop =
          this.$refs.messagesContainer.scrollHeight;
      }
    },
    getCurrentTime() {
      const now = new Date();
      return (
        now.getHours().toString().padStart(2, "0") +
        ":" +
        now.getMinutes().toString().padStart(2, "0")
      );
    },
    clearChat() {
      this.messages = [];
    },
    askSuggestion(question) {
      this.userInput = question;
      this.sendMessage();
    },
  },
  mounted() {
    // Add Material Icons
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://fonts.googleapis.com/icon?family=Material+Icons";
    document.head.appendChild(link);
    // Add highlight.js CSS
    const highlightCss = document.createElement("link");
    highlightCss.rel = "stylesheet";
    highlightCss.href =
      "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/atom-one-dark.min.css";
    document.head.appendChild(highlightCss);
  },
};
</script>

<style scoped>
/* Base styling */
* {
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

/* Animations */
@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.bounce {
  animation: bounce 0.5s ease 2;
}

.slide-fade-enter-active {
  transition: all 0.3s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(20px);
  opacity: 0;
}

@keyframes typing {
  0% {
    transform: translateY(0px);
  }
  28% {
    transform: translateY(-5px);
  }
  44% {
    transform: translateY(0px);
  }
}

.typing-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #aaa;
  margin: 0 2px;
}

.typing-dot:nth-child(1) {
  animation: typing 1.2s infinite;
  animation-delay: 0.2s;
}
.typing-dot:nth-child(2) {
  animation: typing 1.2s infinite;
  animation-delay: 0.4s;
}
.typing-dot:nth-child(3) {
  animation: typing 1.2s infinite;
  animation-delay: 0.6s;
}

/* Chat icon */
.chatbot-icon {
  position: fixed;
  bottom: 20px;
  right: 20px; /* Positioned on the right side instead of left */
  width: 60px;
  height: 60px;
  cursor: pointer;
  background: linear-gradient(
    135deg,
    #2193b0,
    #6dd5ed
  ); /* Different color scheme */
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  z-index: 1000;
}

.chatbot-icon:hover {
  transform: scale(1.1);
}

.chat-icon-text {
  font-size: 28px;
  color: white;
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background-color: #ff4c4c;
  color: white;
  font-size: 12px;
  font-weight: bold;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Chat container */
.chatbot-container {
  position: fixed;
  bottom: 90px;
  right: 20px; /* Positioned on the right side instead of left */
  width: 450px;
  height: 600px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  background: white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
}

/* Chat header */
.chatbot-header {
  padding: 15px;
  background: linear-gradient(135deg, #2193b0, #6dd5ed);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-info {
  margin-left: 10px;
  display: flex;
  flex-direction: column;
}

.header-info h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 4px;
}

.status-indicator.online {
  background-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.3);
}

.header-actions {
  display: flex;
}

.action-button {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  margin-left: 5px;
  padding: 5px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-color 0.2s;
}

.action-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

/* Messages area */
.chatbot-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f5f7fb;
}

.message-date-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10px 0;
  color: #8a8a8a;
  font-size: 12px;
}

.message-date-divider::before,
.message-date-divider::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid #e0e0e0;
  margin: 0 10px;
}

.user-message-container,
.bot-message-container {
  display: flex;
  margin-bottom: 15px;
  align-items: flex-end;
}

.user-message-container {
  justify-content: flex-end;
}

.user-avatar,
.bot-avatar {
  min-width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 12px;
}

.user-avatar {
  background-color: #2193b0; /* Different color */
  color: white;
  margin-left: 10px;
}

.bot-avatar {
  background-color: #6dd5ed; /* Different color */
  color: white;
  margin-right: 10px;
}

.user-message,
.bot-message {
  padding: 14px 18px; /* Increased padding */
  border-radius: 18px;
  max-width: 80%; /* Increased from 70% */
  position: relative;
  font-size: 15px; /* Added font size */
  line-height: 1.5; /* Improved line height */
}

.user-message {
  background: linear-gradient(135deg, #2193b0, #6dd5ed); /* Different color */
  color: white;
  border-bottom-right-radius: 5px;
}

.bot-message {
  background-color: white;
  color: #333;
  border-bottom-left-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.user-message p,
.bot-message p {
  margin: 0;
  line-height: 1.5;
  word-wrap: break-word;
}

.message-time {
  font-size: 10px;
  opacity: 0.7;
  position: absolute;
  bottom: 4px;
  right: 10px;
  margin-top: 6px;
}

.user-message .message-time {
  color: rgba(255, 255, 255, 0.8);
}

.bot-message .message-time {
  color: rgba(0, 0, 0, 0.5);
}

.typing-indicator {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  min-height: 44px;
}

/* Chat input */
.chatbot-input {
  display: flex;
  padding: 10px;
  background-color: white;
  border-top: 1px solid #e9e9e9;
}

.chatbot-input input {
  flex: 1;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.chatbot-input input:focus {
  border-color: #2193b0;
}

.send-button {
  width: 40px;
  height: 40px;
  border: none;
  background: linear-gradient(135deg, #2193b0, #6dd5ed);
  color: white;
  border-radius: 50%;
  margin-left: 10px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.2s;
}

.send-button:hover {
  transform: scale(1.05);
}

.send-button:disabled {
  background: #e0e0e0;
  cursor: not-allowed;
}

/* Suggested questions */
.suggested-questions {
  padding: 12px;
  background-color: #f9f9f9;
  border-top: 1px solid #e9e9e9;
}

.suggestions-title {
  font-size: 13px;
  color: #666;
  margin: 0 0 8px 0;
}

.suggestions-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.suggestion-button {
  padding: 8px 12px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  font-size: 12px;
  color: #2193b0; /* Different color */
  cursor: pointer;
  transition: all 0.2s;
}

.suggestion-button:hover {
  background-color: #e6f7fc; /* Different color */
  border-color: #2193b0; /* Different color */
}
:deep(.code-block) {
  background-color: #282c34;
  border-radius: 8px;
  padding: 12px;
  margin: 8px 0;
  overflow-x: auto;
  font-family: "Consolas", "Monaco", "Courier New", monospace;
  font-size: 14px;
  line-height: 1.5;
}

:deep(code) {
  font-family: "Consolas", "Monaco", "Courier New", monospace;
}

/* Make sure the message time doesn't overlap with code blocks */
.bot-message .message-time {
  position: relative;
  display: block;
  text-align: right;
  margin-top: 8px;
  bottom: auto;
  right: auto;
}

/* Mobile responsiveness */
@media (max-width: 480px) {
  .chatbot-container {
    right: 10px;
    width: calc(100% - 20px);
    bottom: 80px;
  }
}
</style>
