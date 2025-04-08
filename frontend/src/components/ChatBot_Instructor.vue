<template>
  <div>
    <!-- Chat Bubble Icon -->
    <div
      class="chatbot-icon"
      @click="toggleChat"
      :class="{ bounce: animateBubble }"
    >
      <div class="chat-icon-text">💬</div>
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
            <div class="bot-avatar">INS</div>
            <div class="header-info">
              <h2>Instructor Assistant</h2>
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
            <div class="bot-avatar">INS</div>
            <div class="bot-message">
              <p>
                Welcome to the Instructor Assistant! I can help you with grading
                policies, student inquiries, academic integrity, deadlines, and
                more.
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
              <div class="bot-avatar">TA</div>
              <div class="bot-message">
                <!-- Use v-html for messages that might contain code blocks -->
                <div v-html="formatMessage(message.text)"></div>
                <span class="message-time">{{ message.time }}</span>
              </div>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="bot-message-container">
            <div class="bot-avatar">TA</div>
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
            placeholder="Type your message here..."
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
      animateBubble: false,
      suggestedQuestions: [
        "How do I grade programming assignments?",
        "What's the policy for late submissions?",
        "How to handle academic misconduct?",
      ],
    };
  },
  methods: {
    formatMessage(text) {
      // Configure marked with proper options
      marked.setOptions({
        highlight: function (code, lang) {
          if (lang && hljs.getLanguage(lang)) {
            try {
              return hljs.highlight(code, { language: lang }).value;
            } catch (e) {
              console.error(e);
            }
          }
          return hljs.highlightAuto(code).value;
        },
        breaks: true,
        gfm: true,
        headerIds: false,
        mangle: false,
      });

      // Process directly with marked
      return marked(text);
    },
    escapeHtml(text) {
      const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
      };
      return text.replace(/[&<>"']/g, function (m) {
        return map[m];
      });
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
        const response = await fetch("http://127.0.0.1:5000/api/chatbot/ta", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message }),
        });
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
  left: 20px;
  width: 60px;
  height: 60px;
  cursor: pointer;
  background: linear-gradient(135deg, #4568dc, #b06ab3);
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
  left: 20px;
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
  background: linear-gradient(135deg, #4568dc, #b06ab3);
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
  background-color: #4568dc;
  color: white;
  margin-left: 10px;
}

.bot-avatar {
  background-color: #b06ab3;
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
  background: linear-gradient(135deg, #4568dc, #67a3dc);
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
  border-color: #4568dc;
}

.send-button {
  width: 40px;
  height: 40px;
  border: none;
  background: linear-gradient(135deg, #4568dc, #b06ab3);
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
  color: #4568dc;
  cursor: pointer;
  transition: all 0.2s;
}

.suggestion-button:hover {
  background-color: #f0f4ff;
  border-color: #4568dc;
}

/* Mobile responsiveness */
@media (max-width: 480px) {
  .chatbot-container {
    left: 10px;
    right: 10px;
    width: calc(100% - 20px);
    bottom: 80px;
  }
}

:deep(.code-block),
:deep(pre code) {
  background-color: #282c34;
  border-radius: 8px;
  padding: 12px;
  margin: 8px 0;
  overflow-x: auto;
  font-family: "Consolas", "Monaco", "Courier New", monospace;
  font-size: 14px;
  line-height: 1.5;
  display: block;
  color: #abb2bf;
}

:deep(pre) {
  background-color: #282c34;
  border-radius: 8px;
  margin: 8px 0;
  padding: 0;
}

:deep(code) {
  font-family: "Consolas", "Monaco", "Courier New", monospace;
}

:deep(a) {
  color: #4568dc;
  text-decoration: underline;
}

:deep(ul),
:deep(ol) {
  padding-left: 20px;
  margin: 8px 0;
}

:deep(li) {
  margin: 4px 0;
}

:deep(strong) {
  font-weight: bold;
}

:deep(em) {
  font-style: italic;
}

:deep(h1),
:deep(h2),
:deep(h3),
:deep(h4),
:deep(h5),
:deep(h6) {
  margin: 10px 0;
  font-weight: bold;
}

:deep(p) {
  margin: 8px 0;
}

:deep(blockquote) {
  border-left: 4px solid #ccc;
  margin: 8px 0;
  padding-left: 16px;
  color: #666;
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
</style>
