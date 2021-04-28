<template lang="pug">
  div
    h3 Say thanks
    v-btn.mx-2(fab text :color="disThanks" :loading="thLoading" @click="sendThanks")
      v-icon mdi-thumb-up
    span {{ thanks }}
</template>

<script>
import { mapActions, mapGetters } from "vuex"

export default {
  data: () => ({
    thanks: null,
    thLoading: false,
    disThanks: "black",
  }),

  computed: {
    ...mapGetters(["url", "made", "csrf"]),
  },

  methods: {
    ...mapActions(["getCsrfToken"]),
    async sendThanks() {
      this.thLoading = true
      await this.getCsrfToken()
      const res = await fetch(this.url + "/api/send-thanks", {
        method: "POST",
        credentials: "include",
        mode: this.mode,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          csrf: this.csrf,
        }),
      })
      const response = await res.json()
      this.thLoading = false
      this.disThanks = response.thanks ? "accent" : "black"
      this.getThanks()
    },
    async getThanks() {
      await this.getCsrfToken()
      const res = await fetch(this.url + "/api/get-thanks", {
        credentials: "include",
        mode: this.mode,
      })
      const response = await res.json()
      this.thanks = response.count
      this.disThanks = response.thanks ? "accent" : "black"
      
    }
  },

  created() {
    this.getThanks()
  },

}
</script>

<style lang="scss" scoped></style>
