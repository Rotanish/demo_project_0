<template lang="pug">
  v-container.pb-0
    v-row
      v-col.py-0
        v-text-field(
          color="accent"
          v-model="review"
          label="Enter your feedback"
          outlined
          required
          append-outer-icon="mdi-send"
          clear-icon="mdi-close-circle"
          clearable
          @click:append-outer="sendReview"
          :loading="loading"
          :disabled="loading"
        )
        v-dialog(
          v-model="dialog"
          width="500"
        )
          v-card.secondary
            v-card-title(class="headline lighten-2") {{ dialogText }}
            v-divider
            v-card-actions
              v-spacer
              v-btn(
                color="accent"
                text
                @click="dialog = false"
              ) Ok
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  data: () => ({
    review: '',
    loading: false,
    dialog: false,
    dialogText: '',
  }),

  computed: {
    ...mapGetters(['url', 'made', 'csrf', 'auth']),
  },

  methods: {
    ...mapActions(['getCsrfToken']),

    async sendReview() {
      this.review = this.review.trim()
      if (this.review) {
        this.loading = true
        await this.getCsrfToken()
        const res = await fetch(this.url + '/api/send-reviews', {
          method: 'POST',
          credentials: 'include',
          mode: this.mode,
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            review: this.review,
            csrf: this.csrf,
          }),
        })
        const response = await res.json()
        if (response.status == 'OK') {
          if (!this.auth) {
            this.dialogText = 'Thanks, your review on moderated'
            this.dialog = true
            this.review = ''
          }
        } else {
          this.dialogText =
            "Oh, i'm sorry. Error on the server. Please retry later."
          this.dialog = true
        }
        this.$emit('sendReview')
        this.loading = false
      }
    },
  },
}
</script>

<style lang="scss" scoped></style>
