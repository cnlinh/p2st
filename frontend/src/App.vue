<template>
  <div id="app">
    <div class="main">
      <router-view />
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import "./assets/js/config.js";
import "./vendors/simplebar/simplebar.min.js";
import "./vendors/popper/popper.min.js";
import "./vendors/is/is.min.js";
import "./vendors/echarts/echarts.min.js";
import "./vendors/fontawesome/all.min.js";
import "./vendors/lodash/lodash.min.js";
import "./vendors/list.js/list.min.js";
import "./vendors/polyfill/polyfill.min.js";
import "./vendors/jquery/jquery.min.js";
import "./vendors/choices/choices.min.js";
import "./assets/js/theme.js";

import { mapActions, mapState } from "vuex";

export default {
  name: "App",

  computed: {
    ...mapState("auth", ["status"]),
  },

  methods: {
    ...mapActions('admin', ['initData']),
    ...mapActions('auth', ['initUser']),
  },

  async created() {
    if (this.status.loggedIn) {
      //await this.initData();
    }
  },
};
</script>
