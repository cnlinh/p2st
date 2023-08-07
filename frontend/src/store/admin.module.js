import AdminService from '../services/admin.service';

const initialState = {
  topics: [],
  selectedTopic: null,
  messages: [],
}

export const admin = {
  namespaced: true,
  state: initialState,
  actions: {    
    async initData({ dispatch }) {
      await dispatch('fetchTopics');
    },

    async fetchTopics({ commit }) {
      try {
        const topics = await AdminService.listTopics();
        commit('SET_TOPICS', topics);
      } catch (error) {
        console.error('Error fetching topics:', error);
      }
    },

    async fetchMessages({ commit }, topicId) {
      try {
        const messages = await AdminService.getMessagesFromConversation(topicId);
        commit('SET_MESSAGES', messages);
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    },

    selectTopic({ commit, dispatch }, topicId) {
      commit('SET_SELECTED_TOPIC', topicId);
      dispatch('fetchMessages', topicId);
    },
  },
  mutations: {
    SET_TOPICS(state, topics) {
      state.topics = topics;
    },
    SET_SELECTED_TOPIC(state, topicId) {
      state.selectedTopic = topicId;
    },
    SET_MESSAGES(state, messages) {
      state.messages = messages;
    }
  },
};