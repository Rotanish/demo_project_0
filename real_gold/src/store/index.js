import Vue from 'vue'
import Vuex from 'vuex'
import login from "./modules/login";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // url: "http://localhost:5000", //    ВЫКЛЮЧИТЬ НА ПРОДЕ
    url: "", //    ВКЛЮЧИТЬ НА ПРОДЕ
    // mode: "cors", //    ВЫКЛЮЧИТЬ НА ПРОДЕ
    mode: "same-origin", //    ВКЛЮЧИТЬ НА ПРОДЕ

  },
  getters: {
    url(state) {
      return state.url;
    },
    mode(state) {
      return state.mode;
    },
  },

  modules: {
    login,
  }
})
