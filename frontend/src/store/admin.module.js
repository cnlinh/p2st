import AdminService from '../services/admin.service';

const initialState = {
  topics: [],
  selectedTopic: null,
  selectedConversation: null,
  messages: [],
  email: null,
  enrolledModules: [],
  selectedModule: null,
}

export const admin = {
  namespaced: true,
  state: initialState,
  actions: {
    async initData({ dispatch }) {
      await dispatch('fetchStudentDetails');
    },

    async fetchStudentDetails({ commit }) {
      try {
        const response = await AdminService.getStudentDetails();
        commit('SET_MODULES', response.enrolled_modules);
        commit('SET_EMAIL', response.email);
      } catch (error) {
        console.error('Error fetching details:', error);
      }
    },

    async fetchTopics({ commit }, moduleId) {
      try {
        const topics = await AdminService.listTopics(moduleId);
        commit('SET_TOPICS', topics);
      } catch (error) {
        console.error('Error fetching topics:', error);
      }
    },

    async fetchMessages({ commit }, conversationId) {
      try {
        const messages = await AdminService.getMessagesFromConversation(
          conversationId
        )
        commit('SET_MESSAGES', messages);
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    },

    async fetchConversation({ commit }, topic) {
      try {
        const conversation = await AdminService.getConversationByTopic(topic.id);
        commit('SET_SELECTED_CONVERSATION', conversation.id);
      } catch (error) {
        console.log(topic);
        const conversation = await AdminService.initConversation(topic?.id);
        await AdminService.createMessageForConversation(conversation?.id, topic?.id, `What are good questions to ask when learning about ${topic?.name}?`);
        commit('SET_SELECTED_CONVERSATION', conversation.id);

        console.error('Error fetching conversation:', error);
      }
    },

    selectTopic({ commit }, topic) {
      commit('SET_SELECTED_TOPIC', topic);
    },

    selectModule({ commit }, moduleId) {
      commit('SET_SELECTED_MODULE', moduleId);
    },
  },
  mutations: {
    SET_TOPICS(state, topics) {
      state.topics = topics;
    },
    SET_SELECTED_TOPIC(state, topic) {
      state.selectedTopic = topic;
    },
    SET_MESSAGES(state, messages) {
      state.messages = messages;
    },
    SET_SELECTED_CONVERSATION(state, conversationId) {
      state.selectedConversation = conversationId;
    },
    SET_EMAIL(state, email) {
      state.email = email;
    },
    SET_MODULES(state, modules) {
      state.enrolledModules = modules;
    },
    SET_SELECTED_MODULE(state, moduleId) {
      state.selectedModule = moduleId;
    },
  },
};