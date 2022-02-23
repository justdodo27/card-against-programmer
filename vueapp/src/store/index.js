import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  state: {
    nickname: null,
    id: null,
  },
  mutations: {
    login (state, payload){
      state.nickname = payload.nickname
      state.id = payload.id
    },
    logout(state){
      state.nickname = null
      state.id = null
    }
  },
  getters: {
    getNickname: (state) => {
      return state.nickname
    },
    getId: (state) => {
      return state.id
    },
  },
  actions: {},
  modules: {},
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
});
