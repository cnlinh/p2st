export default function authHeader() {
  const token = JSON.parse(sessionStorage.getItem('token'));

  if (token) {
    return { 
      Authorization: 'Bearer ' + token,
      'Content-Type': 'application/json'
    }; 
  } else {
    return {
      'Content-Type': 'application/json'
    };
  }
}