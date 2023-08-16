import { createWebHistory, createRouter } from "vue-router";
import store from '../store';

import PageHome from "../views/PageHome.vue"
import PageLogin from "../views/PageLogin.vue"
import PageLogout from "../views/PageLogout.vue"
import PageRegister from "../views/PageRegister.vue"
import PageChangePassword from "../views/PageChangePassword.vue"

const routes = [
  {
    path: "/",
    name: "PageHome",
    component: PageHome,
    meta: { requiresAuth: true },
  },
  {
    path: "/home",
    component: PageHome,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "PageLogin",
    component: PageLogin,
  },
  {
    path: "/logout",
    component: PageLogout,
  },
  {
    path: "/register",
    component: PageRegister,
  },
  {
    path: "/change-password",
    component: PageChangePassword,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  // Check if the route requires authentication
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // Check if the user is logged in
    if (store.state.auth.status.loggedIn) {
      next(); // Proceed to the route
    } else {
      next({ path: "/login" }); // Redirect to the login page
    }
  } else {
    next(); // Proceed to the route
  }
});

export default router;