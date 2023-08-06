import AuthService from '../services/auth.service';

const token = JSON.parse(sessionStorage.getItem('token'));

const initialState = {
  status: {
    loggedIn: token ? true : false,
  },
  token: null,
};

export const auth = {
  namespaced: true,
  state: initialState,
  actions: {
    async login({ commit }, user) {
      try {
        const response = await AuthService.login(user);
        commit('loginSuccess', response.token);
        return Promise.resolve(response.data);
      }
      catch (error) {
        commit('loginFailure');
        return Promise.reject(error);
      }
    },

    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
  },
  mutations: {
    loginSuccess(state, token) {
      state.status.loggedIn = true;
      state.token = token;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.token = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.token = null;
    },
  }
};
