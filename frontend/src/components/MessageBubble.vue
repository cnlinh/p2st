<template>
  <div class="d-flex p-3" :class="{ 'justify-content-end': isOwnMessage }">
    <div v-if="!isOwnMessage" class="avatar avatar-l me-2">
      <img class="rounded-circle" src="../assets/img/team/2.jpg" alt="" />
    </div>
    <div class="flex-1">
      <div class="w-xxl-75">
        <div class="hover-actions-trigger d-flex align-items-center">
          <div class="chat-message bg-200 p-2 rounded-2" v-if="!isOwnMessage">{{ text }}</div>
          <div class="bg-primary text-white p-2 rounded-2 chat-message light" v-else>{{ text }}</div>
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
            <li class="list-inline-item"><a class="chat-option" href="#" data-bs-toggle="tooltip" data-bs-placement="top"
                title="Star"><span class="fas fa-star"></span></a></li>
            <li class="list-inline-item"><a class="chat-option" href="#" data-bs-toggle="tooltip" data-bs-placement="top"
                title="Copy"><span class="fas fa-copy"></span></a></li>
          </ul>
        </div>
        <div class="text-400 fs--2"><span>{{ timestamp }}</span></div>
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
    isOwnMessage: {
      type: Boolean,
      required: true
    },
    text: {
      type: String,
      required: true
    },
    timestamp: {
      type: String,
      default: "",
      required: false,
    }
  },

  data() {
    return {
      voteStatus: 'neutral',
    };
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
</style>