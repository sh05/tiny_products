// TOP main.js
import Vue from 'vue';
import Top from './Top.vue';

Vue.config.productionTip = false;

new Vue({
  render: h => h(Top),
}).$mount('#app');
