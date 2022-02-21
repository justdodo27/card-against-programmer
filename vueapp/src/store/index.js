import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  state: {
    nickname: null
  },
  mutations: {
    setnickname (state, payload){
      state.nickname = payload.nickname
    },
    logout(state){
      state.nickname = null
    }
  },
  getters: {
    getNickname: (state) => {
      return state.nickname
    }
  },
  actions: {},
  modules: {},
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
});
