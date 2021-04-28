<template lang="pug">
  div
    ReviewInput(@sendReview="getReviews")
    v-card(elevation="5" outlined shaped v-for="(review, i) in reviewsList" :key="i" transition="scroll-y-reverse-transition" :class="{'un-moderated': review.status == 'moderated'}").transparent.ma-2
      v-row(justify="end" no-gutters)
        v-btn(v-if="review.status == 'moderated'" @click="moderating(review.id,'ok')").green.ma-2 OK 
        v-btn(v-if="auth" @click="moderating(review.id,'delete')").red.ma-2 Delete
      v-row(align="center" no-gutters).px-4
        v-col(cols="1")
          v-avatar
            v-icon(:class="{'admin': review.autor}") mdi-account
        v-col(cols="8").px-2
          v-card-title {{ review.autor ? review.autor.nickname : review.nickname }}
        v-col(cols="3")
          v-card-subtitle.text-right {{ review.time_post }}
        v-card-text.text-left.px-6 {{ review.description }}
</template>

<script>
import ReviewInput from '@/components/ReviewInput.vue'

import { mapActions, mapGetters } from 'vuex'

export default {
  components: {
    ReviewInput,
  },

  data: () => ({
    reviewsList: [],
  }),

  computed: {
    ...mapGetters(['url', 'made', 'auth', 'csrf']),
  },

  methods: {
    ...mapActions(['getCsrfToken']),
    async getReviews() {
      const res2 = await fetch(`${this.url}/api/get-reviews`, {
        credentials: 'include',
        mode: this.mode,
      })
      this.reviewsList = await res2.json()
    },
    async moderating(id, command) {
      console.log(id, command)
      await this.getCsrfToken()
      const res = await fetch(this.url + '/api/moderating', {
        method: 'POST',
        credentials: 'include',
        mode: this.mode,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          csrf: this.csrf,
          id,
          command,
        }),
      })
      const response = await res.json()
      // console.log(response)
      if (response.status == 'OK') {
        this.getReviews()
      }
    },
  },

  watch: {
    async auth() {
      this.getReviews()
    },
  },

  async mounted() {
    this.getReviews()
  },
}
</script>

<style lang="sass" scoped>
.un-moderated
  background: #e847 !important
.admin
  color: #49f
  box-shadow: inset 0 0 10px #888
button
  width: 8em
</style>
