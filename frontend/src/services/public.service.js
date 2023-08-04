import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://localhost:8090/app/';

class PublicService {
  registerUser(userDetails) {
    const url = API_URL + 'user/openApi/publ/register';
    const body = JSON.stringify(userDetails);
    const config = {
      headers: authHeader()
    };

    return axios.post(url, body, config)
      .then(response => {
        console.log(response.data);
      })
  }
}

export default new PublicService();