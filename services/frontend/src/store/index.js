import { createStore } from 'vuex';

export default createStore({
  state: {
    user: localStorage.getItem('user') || '',
    token: localStorage.getItem('token') || '',
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
      localStorage.setItem('user', user);
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    clearUser(state) {
      state.user = '';
      state.token = '';
      localStorage.removeItem('user');
      localStorage.removeItem('token');
    },
  },
  actions: {
    setUser({ commit }, user) {
      commit('setUser', user);
    },
    setToken({ commit }, token) {
      commit('setToken', token);
    },
    clearUser({ commit }) {
      commit('clearUser');
    }
  },
  getters: {
    getUser: (state) => state.user,
    getToken: (state) => state.token,
  },
});