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
                  <MessageBubble v-for="(message, index) in messages" :key="index" :isOwnMessage="message.isOwnMessage"
                    :text="message.text" :timestamp="message.timestamp" />
                </div>
              </div>
            </div>
            <form class="chat-editor-area">
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
import BaseLayout from "@/components/BaseLayout.vue";
import MessageBubble from "@/components/MessageBubble.vue";

export default {
  name: "PageHome",

  components: {
    BaseLayout,
    MessageBubble,
  },

  data() {
    return {
      messages: [
        {
          isOwnMessage: true,
          text: 'Yes, in an organization stature, this is a must. Besides, we need to quickly establish all other professional appearances, e.g., having a website where members’ profile will be displayed along with additional organizational information. Providing services to existing members is more important than attracting new members at this moment, in my opinion..',
          timestamp: '11:50 am'
        },
        {
          isOwnMessage: false,
          text: 'I\'m doing well, thanks! How about you?',
          timestamp: '11:51 am'
        },
        {
          isOwnMessage: true,
          text: 'I\'m great! I\'ve been working on this cool project.',
          timestamp: '11:52 am'
        },
        {
          isOwnMessage: false,
          text: 'That sounds interesting! Can you tell me more about it?',
          timestamp: '11:54 am'
        }
      ]
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
