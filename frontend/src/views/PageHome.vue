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
                  <MessageBubble v-for="message in messages" :key="message.id" :isOwnMessage="message.role === 'user'"
                    :text="message.content" timestamp="" />
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
    ...mapState('admin', ['selectedTopic', 'messages']),
  },

  data() {
    return {
      recommendedQuestions: [],
    };
  },

  watch: {
    selectedTopic(newTopicId, oldTopicId) {
      if (newTopicId !== oldTopicId) {
        this.fetchMessages(newTopicId);
        this.fetchRecommendedQuestions();
      }
    },
    messages: {
      handler() {
        this.$forceUpdate();
      },
      deep: true
    }
  },

  methods: {
    ...mapActions('admin', ['fetchMessages']),

    async handleSend() {
      const messageContent = this.$el.querySelector(".emojiarea-editor").textContent;

      if (!messageContent.trim()) {
        return;
      }

      try {
        this.$el.querySelector(".emojiarea-editor").textContent = '';
        await AdminService.createMessageForConversation(this.selectedTopic, this.selectedTopic, messageContent);
        await this.fetchMessages(this.selectedTopic);
        await this.fetchRecommendedQuestions();
      } catch (error) {
        console.error('Error sending message:', error);
      }
    },

    async fetchRecommendedQuestions() {
      try {
        this.recommendedQuestions = await AdminService.getRecommendedQuestionsForConversation(this.selectedTopic);
      } catch (error) {
        console.error('Error fetching recommended questions:', error);
      }
    },

    handleRecommendationClick(question) {
      this.$el.querySelector(".emojiarea-editor").textContent = question;
    },
  },

  async created() {
    if (this.selectedTopic) {
      await this.fetchMessages(this.selectedTopic);
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
</style>
