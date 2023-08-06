import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';

class AuthService {
  login(user) {
    return axios
      .post(API_URL + 'login', {
        email: user.username,
        password: user.password
      })
      .then(response => {
        if (response.data.access) {
          sessionStorage.setItem('token', JSON.stringify(response.data.access));
          sessionStorage.setItem('email', user.username);
        }

        return response.data;
      });
  }

  logout() {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('email');
  }

  register(user) {
    return axios.post(API_URL + 'register', {
      name: user.name,
      email: user.email,
      student_id: user.studentId,
      password: user.password
    }).then(response => {
      return response.data;
    });
  }
}

export default new AuthService();
