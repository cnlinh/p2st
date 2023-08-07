<template>
  <div class="container-fluid">
    <div class="row min-vh-100 bg-100">
      <div class="col-6 d-none d-lg-block" style="--falcon-gutter-x: 0">
        <div class="card mb-3 h-100 d-flex justify-content-center bg-primary">
          <div class="tab-content">
            <div class="tab-pane preview-tab-pane active" role="tabpanel"
              aria-labelledby="tab-dom-60d68d55-fe26-474c-98d8-62d1587bc3f8"
              id="dom-60d68d55-fe26-474c-98d8-62d1587bc3f8">
              <div class="carousel slide overflow-clip" id="carouselExampleCaptions" data-ride="carousel">
                <div class="carousel-indicators">
                  <button class="active" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0"
                    aria-current="true" aria-label="Slide 1"></button>
                  <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1"
                    aria-label="Slide 2"></button>
                  <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2"
                    aria-label="Slide 3"></button>
                </div>
                <div class="carousel-inner light">
                  <div class="carousel-item active">
                    <img class="d-block w-100" src="../assets/img/generic/8.jpg" alt="First slide" />
                    <div class="carousel-caption d-none d-md-block">
                      <h5 class="text-white">First Slide Heading</h5>
                      <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      </p>
                    </div>
                  </div>
                  <div class="carousel-item h-100">
                    <img class="d-block w-100" src="../assets/img/generic/8.jpg" alt="Second slide" />
                    <div class="carousel-caption d-none d-md-block">
                      <h5 class="text-white">Second Slide Heading</h5>
                      <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      </p>
                    </div>
                  </div>
                  <div class="carousel-item h-100">
                    <img class="d-block w-100" src="../assets/img/generic/8.jpg" alt="Third slide" />
                    <div class="carousel-caption d-none d-md-block">
                      <h5 class="text-white">Third Slide Heading</h5>
                      <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit
                      </p>
                    </div>
                  </div>
                </div>

                <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions"
                  data-bs-slide="prev">
                  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                  <span class="sr-only">Previous</span>
                </button>

                <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions"
                  data-bs-slide="next">
                  <span class="carousel-control-next-icon" aria-hidden="true"></span>
                  <span class="sr-only">Next</span>
                </button>
              </div>
            </div>
          </div>
        </div>
        <!--/.bg-holder-->
      </div>
      <div class="col-sm-10 col-md-6 px-sm-0 align-self-center mx-auto py-5">
        <div class="row justify-content-center g-0">
          <div class="col-lg-9 col-xl-8 col-xxl-6">
            <div class="row flex-between-center">
              <div class="col-auto">
                <h3>Welcome Back!</h3>
                <h6 class="text-500 fs--2">
                  Please login to your account to continue.
                </h6>
              </div>
            </div>

            <!-- Login -->
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
                    <input class="form-check-input" type="checkbox" id="split-checkbox" />
                    <label class="form-check-label mb-0" for="split-checkbox">Remember for 30 days</label>
                  </div>
                </div>
                <div class="col-auto">
                  <a class="fs--1" href="/reset-password">Forgot Password?</a>
                </div>
              </div>
              <div class="mb-3">
                <button class="btn btn-primary d-block w-100 mt-3" type="submit">
                  Log in
                </button>
              </div>
            </Form>

            <div class="col-auto fs--1 text-600 text-center">
              <span class="mb-0 fw-semi-bold">Don't have an account? </span>
              <span>
                <a class="fw-bold" href="/register">Sign up</a>
              </span>
            </div>

            <!-- Bottom aligned 
              <footer class="footer">
                <div class="col-auto fs--1 text-600">
                  <a class="fw-bold" href="../../../pages/authentication/split/register.html">Help Center</a>
                </div>
              </footer>
              -->
          </div>
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
          this.message = "Wrong password/username!";
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
