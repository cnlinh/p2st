import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://localhost:8000/api/';

class AdminService {
  listTopics() {
    return axios
      .get(`${API_URL}topics/all`, { headers: authHeader() })
      .then(response => {
        return response.data;
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
      });
  }

  createMessageForConversation(id, topic_id, text) {
    return axios.post(`${API_URL}conversations/${id}`, { topic_id, text }, { headers: authHeader() });
  }

  initConversation(topic_id, text) {
    return axios.post(`${API_URL}conversations`, { topic_id, text }, { headers: authHeader() });
  }

  getRecommendedQuestionsForConversation(id) {
    return axios
      .get(`${API_URL}recommendations/${id}`, { headers: authHeader() })
      .then(response => {
        return response.data.data;
      });
  }

  rateMessage(id, score) {
    return axios
      .post(`${API_URL}ratings/${id}`, { score }, { headers: authHeader() })
      .then(response => {
        console.log(response);
      });
  }
}

export default new AdminService();
