export default {
  state: {
    userLogin: "",
    userName: "",
    avatar: "",
    auth: false,
    csrf: "",
  },
  getters: {
    userLogin(state) {
      return state.userLogin;
    },
    userName(state) {
      return state.userName;
    },
    auth(state) {
      return state.auth;
    },
    avatar(state) {
      return state.avatar;
    },
    csrf(state) {
      return state.csrf;
    },
  },
  mutations: {
    updateUserLogin(state, { login, nickname, auth, avatar}) {
      state.userLogin = login;
      state.userName = nickname;
      state.auth = auth;
      state.avatar = avatar;
    },
    updateCsrf(state, csrf) {
      state.csrf = csrf;
    },
  },
  actions: {
    async getCsrfToken({ commit, state, getters }) {
      if (state.csrf === "") {
        const csrfRes = await fetch(getters.url + "/api/csrf", {
          method: "GET",
          credentials: "include",
          mode: getters.mode,
        });
        const csrf = await csrfRes.text();
        commit("updateCsrf", csrf);
      }
    },
    async whoami({ commit, getters }) {
      const res = await fetch(getters.url + "/api/whoami", {
        method: "GET",
        credentials: "include",
        mode: getters.mode,
      });
      const response = await res.json();
      if (response.status === "auth") {
        commit("updateUserLogin", { ...response, auth: true });
      }
      if (response.status === "not auth") {
        commit("updateUserLogin", { ...response, auth: false });
      }
      // console.log(response.status);
      return response.status;
    },
    async loginUser({ state, getters, dispatch }, { login, password }) {
      await dispatch("getCsrfToken");
      const csrf = state.csrf;
      const res = await fetch(getters.url + "/api/login", {
        method: "POST",
        credentials: "include",
        mode: getters.mode,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          login,
          password,
          csrf,
        }),
      });
      const response = await res.text();
      dispatch("whoami");
      return response;
    },
    async logout({ state, getters, dispatch }) {
      await dispatch("getCsrfToken");
      const csrf = state.csrf;
      const res = await fetch(getters.url + "/api/logout", {
        method: "POST",
        credentials: "include",
        mode: getters.mode,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          csrf,
        }),
      });
      const response = await res.text();
      dispatch("whoami");
      // console.log(response);
      return response;
    },
    async logoutAll({ state, getters, dispatch }) {
      await dispatch("getCsrfToken");
      const csrf = state.csrf;
      const res = await fetch(getters.url + "/api/logoutall", {
        method: "POST",
        credentials: "include",
        mode: getters.mode,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          csrf,
        }),
      });
      const response = await res.text();
      dispatch("whoami");
      // console.log(response);
      return response;
    },
    async registrate(
      { state, getters, dispatch },
      { login, nickname, password, checkbox }
    ) {
      await dispatch("getCsrfToken");
      const csrf = state.csrf;
      const res = await fetch(getters.url + "/api/registrate", {
        method: "POST",
        credentials: "include",
        mode: getters.mode,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          login,
          nickname,
          password,
          checkbox,
          csrf,
        }),
      });
      const response = await res.text();
      await dispatch("whoami");
      return response;
    },
  },
};
