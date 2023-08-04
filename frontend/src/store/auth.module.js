import AuthService from '../services/auth.service';
import AdminService from '../services/admin.service';

const user = JSON.parse(sessionStorage.getItem('user'));

const initialState = {
  status: {
    loggedIn: user ? true : false,
  },
  user: null,
  userDetail: null,
  sessionId: null,
};

export const auth = {
  namespaced: true,
  state: initialState,
  actions: {
    async initUser({ commit }) {
      const user = JSON.parse(sessionStorage.getItem('user'));
      const userDetail = JSON.parse(sessionStorage.getItem('userDetail'));
      const charts = await AdminService.getCharts();
      const sessionId = charts.sessionId;

      commit('updateUser', user);
      commit('updateUserDetail', userDetail);
      commit('updateSessionId', sessionId);
    },

    async login({ commit, dispatch }, user) {
      return AuthService.login(user).then(
        user => {
          commit('loginSuccess', user);
          dispatch('initUser');
          dispatch('admin/initData', null, { root: true });
          return Promise.resolve(user);
        },
        error => {
          commit('loginFailure');
          return Promise.reject(error);
        }
      );
    },

    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
  },
  mutations: {
    updateUser(state, user) {
      state.user = user;
    },
    updateUserDetail(state, userDetail) {
      state.userDetail = userDetail;
    },
    updateSessionId(state, sessionId) {
      state.sessionId = sessionId;
    },
    loginSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
  }
};
