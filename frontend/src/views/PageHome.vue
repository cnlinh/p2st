<template>
  <BaseLayout>
    <template v-slot:main-content>
      <!-- Main content -->
      <div class="card card-chat overflow-hidden">
        <div class="card-body d-flex p-0 h-100">
          <div class="tab-content card-chat-content">
            <div class="tab-pane card-chat-pane active" id="chat-0" role="tabpanel" aria-labelledby="chat-link-0">
              <div class="chat-content-body" style="display: inherit;">
                <div class="chat-content-scroll-area scrollbar">
                  <MessageBubble v-for="message in messages" :key="message.id" :id="message.id" :role="message.role"
                    :content="message.content" />
                </div>
              </div>
            </div>
            <div class="card-body">
              <a v-for="question in recommendedQuestions" :key="question"
                class="badge border link-secondary me-1 text-decoration-none" @click="handleRecommendationClick(question)"
                href="#!">{{ question }}</a>
            </div>
            <form class="chat-editor-area" @submit.prevent="handleSend">
              <div class="emojiarea-editor outline-none scrollbar" contenteditable="true"></div>
              <input class="d-none" type="file" id="chat-file-upload" />
              <button class="btn btn-sm btn-send shadow-none" type="submit">Send</button>
            </form>
          </div>
        </div>
        <!-- Overlay message when no topic is selected -->
        <div v-if="!selectedTopic" class="overlay-no-topic">
          Select a module and a topic to continue
        </div>
      </div>
    </template>
  </BaseLayout>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import AdminService from "@/services/admin.service";
import BaseLayout from "@/components/BaseLayout.vue";
import MessageBubble from "@/components/MessageBubble.vue";

export default {
  name: "PageHome",

  components: {
    BaseLayout,
    MessageBubble,
  },

  computed: {
    ...mapState('admin', ['selectedTopic', 'messages', 'selectedConversation']),
  },

  data() {
    return {
      recommendedQuestions: [],
    };
  },

  watch: {
    selectedTopic(newTopicId, oldTopicId) {
      if (newTopicId !== oldTopicId) {
        this.recommendedQuestions = [];
        this.fetchConversation(newTopicId);
      }
    },
    selectedConversation(newConversationId, oldConversationId) {
      if (newConversationId !== oldConversationId) {
        this.recommendedQuestions = [];
        this.fetchMessages(newConversationId);
        this.fetchRecommendedQuestions();
      }
    },
    messages: {
      handler() {
        this.$forceUpdate();
      },
      deep: true
    },
  },

  methods: {
    ...mapActions('admin', ['fetchMessages', 'fetchConversation']),

    async handleSend() {
      const editor = this.$el.querySelector(".emojiarea-editor");
      if (!editor || !editor.textContent.trim()) {
        return;
      }

      try {
        await AdminService.createMessageForConversation(this.selectedConversation, this.selectedTopic, editor.textContent);
        editor.textContent = '';
        await this.fetchMessages(this.selectedConversation);
        await this.fetchRecommendedQuestions();
      } catch (error) {
        console.error('Error sending message:', error);
      }
    },

    async fetchRecommendedQuestions() {
      if (!this.messages || !this.messages.length) {
        return;
      }

      try {
        const lastMessageId = this.messages[this.messages.length - 1].id;
        this.recommendedQuestions = await AdminService.getRecommendedQuestionsForConversation(lastMessageId);
      } catch (error) {
        console.error('Error fetching recommended questions:', error);
      }
    },

    handleRecommendationClick(question) {
      const editor = this.$el.querySelector(".emojiarea-editor");
      if (editor) {
        editor.textContent = question;
      }
    },
  },

  async created() {
    if (this.selectedConversation) {
      await this.fetchMessages(this.selectedConversation);
      await this.fetchRecommendedQuestions();
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "../vendors/simplebar/simplebar.min.css";
@import "../assets/css/user.css";
@import "../assets/css/theme.css";

@import "https://fonts.googleapis.com/css?family=Open+Sans:300,400,500,600,700%7cPoppins:300,400,500,600,700,800,900&amp;display=swap";

.overlay-no-topic {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8); /* semi-transparent white */
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
  color: #555;
  z-index: 10; /* Ensure the overlay appears above the chat content */
}
</style>
