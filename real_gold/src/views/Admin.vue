<template lang="pug">
  div
    v-container
      v-row
        v-col
          .rounded-xl.pa-6.text-center.mx-auto.my-6.block
            v-form(ref="form" v-model="valid" lazy-validation @submit.prevent="submit")
              v-text-field(
                color="accent"
                v-model="login"
                :counter="20"
                label="Логин"
                required
              )
              v-text-field(
                color="accent"
                v-model="password"
                :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPass ? 'text' : 'password'"
                label="Пароль"
                counter
                @click:append="showPass = !showPass"
                required
              )
              v-col(style="color: #e66")
                strong {{ msgDialog }}
              v-btn(color="success" class="mr-4" type="submit") Войти
</template>

<script>
import { mapActions } from "vuex"
export default {
  data: () => ({
    msgDialog: "",
    valid: true,
    login: "",
    password: "",
    showPass: false,
  }),

  methods: {
    ...mapActions(["loginUser"]),
    validate() {
      this.$refs.form.validate()
    },
    reset() {
      this.$refs.form.reset()
    },
    async submit() {
      const res = await this.loginUser({
        login: this.login,
        password: this.password,
      })
      console.log(res)
      if (res === "Already logined") this.msgDialog = "Вы уже залогинены"
      if (res === "Logined") this.$router.push("/")
      if (res === "Wrong login or password")
        this.msgDialog = "Неправильный логин или пароль."
      if (res === "Oops") this.msgDialog = "Неизвестная ошибка."
    },
  },
}
</script>

<style lang="sass"></style>
