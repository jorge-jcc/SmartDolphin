import Vue from 'vue'
import Vuetify from 'vuetify/lib'

import colors from 'vuetify/lib/util/colors'
Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: colors.purple.darken2, // #E53935
        secondary: colors.purple.lighten1, // #FFCDD2
        accent: colors.purple.base, // #3F51B5
      },
    },
  },
})