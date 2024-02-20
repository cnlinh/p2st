<template>
  <div class="row flex-center min-vh-100 py-6">
    <div class="col-sm-10 col-md-8 col-lg-6 col-xl-5 col-xxl-4">
      <div class="d-flex flex-center mb-4"><a class="navbar-brand" href="/home">
          <div class="d-flex align-items-center py-3"><span
              class="font-sans-serif fw-bolder fs-5 d-inline-block text-black">P2ST</span>
          </div>
        </a></div>
      <div class="card">
        <div class="card-body p-4 p-sm-5">
          <div class="row flex-between-center mb-2">
            <div class="col-auto">
              <h5>Log in</h5>
            </div>
            <div class="col-auto fs--1 text-600"><span class="mb-0 undefined">or</span> <span><a href="/register">Sign
                  up</a></span></div>
          </div>
          <Form @submit="handleLogin" :validation-schema="schema">
            <div class="mb-3">
              <label class="form-label" for="card-email">Email address</label>
              <Field name="username" type="email" class="form-control" id="username" placeholder="Enter email" />
              <ErrorMessage name="username" class="error-feedback text-danger" />
            </div>
            <div class="mb-3">
              <label class="form-label" for="card-password">Password</label>
              <Field name="password" type="password" class="form-control" id="password" placeholder="Enter password" />
              <ErrorMessage name="password" class="error-feedback text-danger" />
            </div>
            <h6 class="text-center text-danger">
              {{ this.message }}
            </h6>
            <div class="row flex-between-center">
              <div class="col-auto">
                <div class="form-check mb-0">
                  <input class="form-check-input" type="checkbox" id="basic-checkbox" checked="checked" />
                  <label class="form-check-label mb-0" for="basic-checkbox">Remember me</label>
                </div>
              </div>
              <div class="col-auto"><a class="fs--1" href="/change-password">Change Password</a></div>
            </div>
            <div class="mb-1">
              <button class="btn btn-primary d-block w-100 mt-3" type="submit" name="submit">Log in</button>
              <div class="col-auto fs--1 text-600 mt-3"><span class="mb-0 fw-semi-bold">Forget your password? </span>
                <span><a href="/reset-password">Reset Password</a></span>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Form, Field, ErrorMessage } from "vee-validate";
import * as yup from "yup";

export default {
  name: "PageLogin",

  components: {
    Form,
    Field,
    ErrorMessage,
  },

  data() {
    const schema = yup.object().shape({
      username: yup.string().required("Username is required!"),
      password: yup.string().required("Password is required!"),
    });

    return {
      loading: false,
      message: "",
      schema,
    };
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },

  created() {
    if (this.loggedIn) {
      this.$router.push("/home");
    }
  },

  methods: {
    async handleLogin(user) {
      try {
        this.loading = true;
        await this.$store.dispatch("auth/login", user);
        this.$router.push("/home");
      } catch (error) {
        this.loading = false;
        this.message =
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString();

        if (this.message === "Request failed with status code 500") {
          this.message = "Wrong email/password!";
        } else if (this.message === "Request failed with status code 401") {
          this.message = "Wrong email/password!";
        }
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "../vendors/simplebar/simplebar.min.css";
@import "../assets/css/user.css";
@import "../assets/css/theme.css";
@import "https://fonts.googleapis.com/css?family=Open+Sans:300,400,500,600,700%7cPoppins:300,400,500,600,700,800,900&amp;display=swap";
</style>
