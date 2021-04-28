<template lang="pug">
  .block.rounded-xl.pa-6.text-center.mx-auto.my-6
    v-form(ref="form" v-model="valid" lazy-validation @submit.prevent="submit").my-4
      v-select(
        color="accent"
        item-color="accent"
        v-model="selectServer"
        :items="Object.keys(priceList)"
        :rules="[(v) => !!v || 'Select server']"
        label="server"
        key="server"
        required
      ).mb-4
      v-text-field(
        color="accent"
        v-model="gold"
        :rules="goldRules"
        type="number"
        label="Gold"
        key="Gold"
        append-icon="G"
        @input="goldChange"
        required
      ).mb-4
      label.label {{ goldPerPrice }}
      v-text-field(
        color="accent"
        v-model="price"
        :rules="priceRules"
        type="number"
        label="Price"
        key="Price"
        append-icon="$"
        @input="priceChange"
        required
      ).mb-4
      v-text-field(
        color="accent"
        v-model="nickname"
        :rules="nicknameRules"
        label="Your nickname on the server"
        required
        type="nickname"
        key="nickname"
      ).mb-4
      v-radio-group(v-model="faction" row :rules='[v => !!v || "select you faction"]').mb-4
        v-radio(value="Alliance" label="Alliance" color="accent")
        v-radio(value="Horde" label="Horde" color="accent")
      v-text-field(
        color="accent"
        v-model="email"
        :rules="emailRules"
        label="Email"
        key="Email"
        required
        type="email"
      ).mb-4
      v-radio-group(v-model="payment" row :rules='[v => !!v || ""]').mb-4
        v-radio(value="PayPal" label="PayPal" color="accent")
        v-radio(value="WebMoney" label="WebMoney" color="accent")
      v-col(style="color: #e66")
        strong {{ msgDialog }}
      v-btn(color="success" class="py-10 px-14 text-h4" type="submit" :loading="loading") Buy
    .d-none(ref="subForm") asd

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
            @click="dialog = false"
          ) Ok
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  data: () => ({
    loading: false,
    dialog: false,
    dialogText: '',
    msgDialog: '',
    valid: true,
    gold: '',
    goldRules: [(v) => /\d+/.test(v) || '', (v) => v > 0 || ``],
    price: '',
    priceRules: [(v) => /\d+/.test(v) || '', (v) => v >= 2 || 'min 2$'],
    nicknameRules: [
      (v) => !!v || 'We need your nickname',
      (v) => (v && v.length <= 40) || 'Max 40 symbols',
    ],
    selectServer: null,
    nickname: '',
    faction: '',
    email: '',
    emailRules: [
      (v) => !!v || '',
      (v) => /.+@.+\..+/.test(v) || 'Email must be valid',
      (v) => v.length <= 50 || 'Max 50 symbols',
    ],
    priceList: {},
    payment: 'PayPal',
    goldPerPrice: 'Connecting...',
  }),

  computed: {
    ...mapGetters(['url', 'made', 'csrf']),
  },

  methods: {
    ...mapActions(['getCsrfToken']),
    round(value) {
      return Math.round(value * 100) / 100
    },

    goldChange() {
      if (this.selectServer) {
        this.price = String(
          this.round(this.gold / this.priceList[this.selectServer])
        )
        if (this.price == 0) {
          this.price = ''
        }
      } else {
        this.price = ''
      }
    },

    priceChange() {
      if (this.selectServer) {
        this.gold = String(
          this.round(this.price * this.priceList[this.selectServer])
        )
        if (this.gold == 0) {
          this.gold = ''
        }
      } else {
        this.gold = ''
      }
    },

    serverError(text = 'Server error. Please try again later') {
      this.loading = false
      this.dialogText = text
      this.dialog = true
    },

    validate() {
      this.$refs.form.validate()
    },
    submit() {
      if (this.$refs.form.validate()) {
        this.loading = true
        localStorage.setItem('selectServer', this.selectServer)
        localStorage.setItem('nickname', this.nickname)
        localStorage.setItem('faction', this.faction)
        localStorage.setItem('email', this.email)
        localStorage.setItem('payment', this.payment)
        this.getCsrfToken().then(
          () => {
            fetch(this.url + '/api/pay-start', {
              method: 'POST',
              credentials: 'include',
              mode: this.mode,
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                csrf: this.csrf,
                gold: this.gold,
                price: this.price,
                server: this.selectServer,
                nickname: this.nickname,
                faction: this.faction,
                email: this.email,
                pay: this.payment,
              }),
            }).then(
              (res) => {
                res.json().then(
                  (response) => {
                    if (response.status == 'Oops') {
                      this.loading = false
                      this.serverError()
                      return
                    }
                    if (response.payment == 'webmoney') {
                      const form = document.createElement('form')
                      form.method = 'POST'
                      form.action = response.action
                      form.acceptCharset = 'utf-8'
                      for (const param in response.params) {
                        const element = document.createElement('input')
                        element.name = param
                        element.value = response.params[param]
                        form.appendChild(element)
                      }
                      this.$refs.subForm.appendChild(form)
                      form.submit()
                      this.price = ''
                      this.gold = ''
                    }
                    if (response.payment == 'paypal') {
                      window.location.href = response.approveLink
                      this.price = ''
                      this.gold = ''
                    }
                  },
                  () => {
                    this.serverError()
                  }
                )
              },
              () => {
                this.serverError()
              }
            )
          },
          () => {
            this.serverError()
          }
        )
      }
    },
    goldPerPriceUpdate() {
      if (
        !Object.keys(this.priceList).length ||
        Object.keys(this.priceList).length < 1
      ) {
        this.goldPerPrice = 'Bad connection. Please try again later'
        return
      }
      let priceOnDollar
      if (this.selectServer) {
        priceOnDollar = this.priceList[this.selectServer]
      } else {
        priceOnDollar = Math.max(...Object.values(this.priceList))
      }
      let gold = 1000
      let priceGold = gold / priceOnDollar
      if (priceGold > 10) {
        gold = 1
        priceGold /= 1000
      }
      this.goldPerPrice = `${gold} gold per ${this.round(priceGold)} $`
    },
  },

  watch: {
    priceList() {
      this.goldPerPriceUpdate()
    },
    selectServer() {
      this.goldPerPriceUpdate()
      this.price = ''
      this.gold = ''
    },
  },

  mounted() {
    this.price = ''
    this.gold = ''
    if (localStorage.nickname) {
      this.nickname = localStorage.getItem('nickname')
    }
    if (localStorage.faction) {
      this.faction = localStorage.getItem('faction')
    }
    if (localStorage.email) {
      this.email = localStorage.getItem('email')
    }
    if (localStorage.payment) {
      this.payment = localStorage.getItem('payment')
    }

    fetch(this.url + '/api/get-price-list', {
      method: 'GET',
      credentials: 'include',
      mode: this.mode,
    }).then(
      (res) => {
        res.json().then((response) => {
          this.priceList = response
          if (localStorage.selectServer) {
            this.selectServer = localStorage.getItem('selectServer')
          }
          this.price = ''
          this.gold = ''
        })
      },
      () => {
        this.serverError('Bad connection. Please try again later')
        this.goldPerPriceUpdate()
      }
    )
  },
}
</script>

<style lang="sass">
input[type=number]::-webkit-inner-spin-button, input[type=number]::-webkit-outer-spin-button
    -webkit-appearance: none
    -moz-appearance: none
    appearance: none
    margin: 0
.v-input, .v-label, .label
  font-size: 1.2em
</style>
