import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://localhost:8000/api/';

class AdminService {
  listTopics() {
    return axios
      .get(`${API_URL}topics`, { headers: authHeader() })
      .then((response) => {
        return response.data
      })
      .catch(error => {
        console.error("Error fetching topics:", error);
        return null;
      });
  }

  getMessagesFromConversation(id) {
    return axios
      .get(`${API_URL}conversations/${id}`, { headers: authHeader() })
      .then(response => {
        return response.data.messages;
      })
      .catch(error => {
        console.error("Error fetching messages:", error);
        return null;
      });
  }

  createMessageForConversation(id, topicId, text) {
    return axios.post(
      `${API_URL}conversations/${id}`,
      { topic: topicId, text },
      { headers: authHeader() }
    )
      .catch(error => {
        console.error("Error creating message:", error);
        throw error;
      });
  }

  initConversation(topicId) {
    return axios
      .post(
        `${API_URL}conversations`,
        { topic: topicId },
        { headers: authHeader() }
      )
      .then((response) => {
        return response.data;
      })
      .catch(error => {
        console.error("Error initializing conversation:", error);
        return null;
      });
  }

  getConversationByTopic(topicId) {
    return axios
      .get(`${API_URL}conversations?topic=${topicId}`, {
        headers: authHeader(),
      })
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        console.error("Error fetching conversation by topic:", error);
        return null;
      });
  }

  getRecommendedQuestionsForConversation(id) {
    return axios
      .get(`${API_URL}recommendations/${id}`, { headers: authHeader() })
      .then((response) => {
        return response.data.data;
      })
      .catch(error => {
        console.error("Error fetching recommended questions:", error);
        return null;
      });
  }

  rateMessage(id, score) {
    return axios
      .post(`${API_URL}ratings/${id}`, { score }, { headers: authHeader() })
      .catch(error => {
        console.error("Error rating message:", error);
        throw error;
      });
  }
}

export default new AdminService()
