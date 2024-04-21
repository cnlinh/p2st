<template>
  <div class="d-flex p-3" :class="{ 'justify-content-end': role === 'user' }">
    <!-- Avatar -->
    <div class="avatar avatar-l me-2">
      <img class="rounded-circle" :src="avatarSrc" alt="" />
    </div>

    <div class="flex-1">
      <div class="w-xxl-75">
        <div class="hover-actions-trigger d-flex align-items-center">
          <pre v-html="formattedContent" class="formatted-text chat-message bg-200 p-2 rounded-2"
            v-if="role === 'assistant'"></pre>
          <pre v-html="formattedContent" class="formatted-text chat-message bg-success text-white p-2 rounded-2 light"
            v-else></pre>
          <ul class="hover-actions position-relative list-inline mb-0 text-400 ms-2">
            <li class="list-inline-item">
              <a class="chat-option" :class="{ 'highlighted': voteStatus === 'upvote' }" href="#"
                @click.prevent="handleUpvote" data-bs-toggle="tooltip" data-bs-placement="top" title="Upvote">
                <span class="fas fa-thumbs-up"></span>
              </a>
            </li>
            <li class="list-inline-item">
              <a class="chat-option" :class="{ 'highlighted': voteStatus === 'downvote' }" href="#"
                @click.prevent="handleDownvote" data-bs-toggle="tooltip" data-bs-placement="top" title="Downvote">
                <span class="fas fa-thumbs-down"></span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminService from "@/services/admin.service";

export default {
  name: "MessageBubble",
  props: {
    id: {
      type: Number,
      required: true
    },
    role: {
      type: String,
      required: true
    },
    content: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      voteStatus: 'neutral',
    };
  },

  computed: {
    avatarSrc() {
      return this.role === 'user' ? require('../assets/img/team/3.jpg') : require('../assets/img/team/2.jpg');
    },
    formattedContent() {
      return this.content
        .replace(/```([^`]+)```/g, '<pre>$1</pre>') 
        .replace(/`([^`]+)`/g, '<strong>$1</strong>'); 
    },
  },

  methods: {
    async handleUpvote() {
      try {
        await AdminService.rateMessage(this.id, 5);
        this.voteStatus = 'upvote';
      } catch (error) {
        console.error('Error upvoting message:', error);
      }
    },
    async handleDownvote() {
      try {
        await AdminService.rateMessage(this.id, 1);
        this.voteStatus = 'downvote';
      } catch (error) {
        console.error('Error downvoting message:', error);
      }
    },
  },
};
</script>

<style scoped>
.highlighted {
  color: #ff5722;
}

.formatted-text {
  white-space: pre-line;
  font-family: "Open Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
}
</style>