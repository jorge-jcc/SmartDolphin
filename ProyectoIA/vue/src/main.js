import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import Vuelidate from 'vuelidate'
import VueApexCharts from 'vue-apexcharts'


Vue.config.productionTip = false
Vue.config.devtools = true
eel._host="http://localhost:8000";

Vue.use(Vuelidate);

Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
