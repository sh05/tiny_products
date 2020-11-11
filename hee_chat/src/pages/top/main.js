// TOP main.js
import Vue from 'vue';
import Top from './Top.vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify);
Vue.config.productionTip = false;

new Vue({
  render: h => h(Top),
}).$mount('#app');
