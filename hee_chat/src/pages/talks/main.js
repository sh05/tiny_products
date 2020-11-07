// Talks .js
import Vue from 'vue';
import Talks from './Talks.vue';

Vue.config.productionTip = false;

new Vue({
  render: h => h(Talks),
}).$mount('#app');
