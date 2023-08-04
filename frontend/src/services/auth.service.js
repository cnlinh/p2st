import axios from 'axios';

const API_URL = 'http://localhost:8090/app/';

class AuthService {
  login(user) {
    return axios
      .post(API_URL + 'authenticate', {
        username: user.username,
        password: user.password
      })
      .then(response => {
        if (response.data.token) {
          sessionStorage.setItem('token', JSON.stringify(response.data.token));
        }

        return response.data;
      });
  }

  logout() {
    sessionStorage.removeItem('token');
  }

  register(user) {
    return axios.post(API_URL + 'signup', {
      username: user.username,
      email: user.email,
      password: user.password
    }).then(response => {
      return response.data;
    });
  }
}

export default new AuthService();
