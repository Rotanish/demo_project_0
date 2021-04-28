import '@mdi/font/css/materialdesignicons.css'
import Vue from "vue"
import Vuetify from "vuetify/lib"

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    options: {
      customProperties: true,
    },
    themes: {
      light: {
        primary: "#036",
        secondary: "#09a",
        accent: "#136",
        success: "#2b9",
        info: "#393",
        error: "#711",
      },
    },
  },
})
