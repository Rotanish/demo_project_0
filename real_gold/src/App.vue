<template lang="pug">
  v-app(app)
    .gradient.h-100
      v-app-bar(app justify="center" no-gutters @click="$vuetify.goTo(0)").primary.cursor-pointer.cyan--text.pa-0.ma-0
        v-col.pa-0.ma-0.h-100
          .d-flex.justify-center.pa-0.ma-0.align-center.h-100(@click="$router.push('/')")
            img(src="@/assets/owl.png").owl.h-100
            svg(version="1.0" xmlns="http://www.w3.org/2000/svg" width="1049.000000pt" height="1280.000000pt" viewBox="0 0 1049.000000 1280.000000" preserveAspectRatio="xMidYMid meet").crescent.mr-4
              metadata Created by potrace 1.15, written by Peter Selinger 2001-2017
              g(transform="translate(900.00000,-100.000000) scale(0.050000,-0.050000) rotate(200)" fill="cyan" stroke="none")
                path(d="M6015 12789 c-740 -46 -1469 -219 -2145 -509 -284 -121 -817 -407 -985 -528 -22 -15 -108 -77 -191 -136 -179 -126 -366 -275 -521 -412 -163 -144 -375 -344 -398 -375 -11 -15 -63 -74 -115 -131 -1223 -1342 -1815 -3153 -1624 -4968 153 -1459 796 -2809 1835 -3849 665 -665 1429 -1156 2315 -1486 406 -151 865 -268 1304 -330 341 -48 510 -59 900 -59 374 -1 519 8 810 45 85 11 182 23 215 25 33 3 121 19 195 35 707 160 1097 293 1625 554 386 191 672 366 1000 612 261 196 285 223 237 271 -17 17 -43 20 -233 25 -1742 51 -3386 839 -4545 2177 -1184 1368 -1717 3206 -1453 5010 218 1494 969 2854 2124 3849 116 100 115 98 115 132 0 52 -22 59 -186 58 -82 -1 -207 -6 -279 -10z")
            h1(@click="$router.push('/')").d-md-none.text-center Golden Owl
            h1(@click="$router.push('/')").d-none.d-md-block.text-center Golden Owl - Buy gold in World of Warcraft
        v-btn(v-if="auth" @click="logout" color="success").black--text Logout
      v-main(app)
        router-view.h-100.star
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'App',

  data: () => ({
    //
  }),

  computed: {
    ...mapGetters(['auth']),
  },

  methods: {
    ...mapActions(['logout', 'whoami']),
  },

  created() {
    document.title = 'Golden Owl'
    this.whoami()
  },
}
</script>

<style lang="sass">
*::-webkit-scrollbar-track
  -webkit-box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.0)
  background-color: #136

*::-webkit-scrollbar
  width: 10px
  background-color: #136

*::-webkit-scrollbar-thumb
  -webkit-box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.0)
  background-color: cyan

.block
  background-color: #ddd5

.star
  background: url("./assets/star.svg") repeat

.gradient
  background-color: #116699
  $color1: #7357d2
  $color2: #116699
  $color3: #075470
  $color4: #1560a9
  background: fixed linear-gradient(-45deg,$color1, $color2, $color3, $color4)

  background-size: 100% 100%

@keyframes gradient
  0%
    background-position: 0% 0%
  100%
    background-position: 100% 100%

.mh-100
  min-height: 100%

.h-100
  height: 100%

.cursor-pointer
  cursor: pointer


.v-toolbar__content.v-toolbar__content
  padding: 0
</style>

<style lang="sass" scoped>
.crescent
  height: 50px
  width: 50px
.owl
  margin-right: -30px
</style>
