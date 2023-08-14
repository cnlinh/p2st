import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';

axios.interceptors.response.use(
  response => response,
  error => {
    const originalRequest = error.config;
    
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = JSON.parse(sessionStorage.getItem('refresh'));
      
      if (!refreshToken) throw error;
      
      return axios.post(`${API_URL}token/refresh`, { refresh: refreshToken })
        .then(res => {
          sessionStorage.setItem('token', JSON.stringify(res.data.access));
          
          axios.defaults.headers['Authorization'] = 'Bearer ' + res.data.access;
          originalRequest.headers['Authorization'] = 'Bearer ' + res.data.access;
          
          return axios(originalRequest);
        })
        .catch(err => {
          console.error("Error fetching refresh token:", err);
          AuthService.logout();
          window.location.href = '/login';
        });
    }
    
    return Promise.reject(error);
  }
);

class AuthService {
  login(user) {
    return axios
      .post(`${API_URL}login`, {
        email: user.username,
        password: user.password
      })
      .then(response => {
        if (response.data) {
          sessionStorage.setItem('refresh', JSON.stringify(response.data.refresh));
          sessionStorage.setItem('token', JSON.stringify(response.data.access));
          sessionStorage.setItem('email', user.username);
        }

        return response.data;
      });
  }

  refreshToken() {
    const refreshToken = JSON.parse(sessionStorage.getItem('refresh'));

    return axios
      .post(`${API_URL}token/refresh`, { refresh: refreshToken })
      .then(response => {
        if (response.data) {
          sessionStorage.setItem('token', JSON.stringify(response.data.access));
        }

        return response.data;
      })
      .catch(error => {
        console.error("Error during token refresh:", error);
        throw error;
      });
  }

  logout() {
    sessionStorage.removeItem('refresh');
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('email');
  }

  register(user) {
    return axios.post(`${API_URL}register`, {
      name: user.name,
      email: user.email,
      student_id: user.studentId,
      password: user.password
    }).then(response => {
      return response.data;
    });
  }

  changePassword(passwordDetails) {
    return axios.post(`${API_URL}change-password`, {
      email: passwordDetails.email,
      current_password: passwordDetails.currentPassword,
      new_password: passwordDetails.newPassword
    }).then(response => {
      return response.data;
    });
}
}

export default new AuthService();
