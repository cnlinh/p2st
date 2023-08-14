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
                <h3>Sign up with your email</h3>
              </div>
            </div>
            <form>
              <div class="row gx-2">
                <div class="mb-3">
                  <label class="form-label required" for="name">Name</label>
                  <input v-model="name" class="form-control" type="text" id="name" placeholder="Enter name"
                    @input="clearError('name')" />
                  <span class="text-danger">{{ validationErrors.name }}</span>
                </div>
                <div class="mb-3">
                  <label class="form-label required" for="name">Student ID</label>
                  <input v-model="studentId" class="form-control" type="text" id="student-id" placeholder="Enter student id"
                    @input="clearError('name')" />
                  <span class="text-danger">{{ validationErrors.studentId }}</span>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label required" for="email">Email</label>
                <input v-model="email" class="form-control" type="email" id="email" placeholder="Enter email"
                  @input="clearError('email')" />
                <span class="text-danger">{{ validationErrors.email }}</span>
              </div>
              <div class="row gx-2">
                <div class="mb-3">
                  <label class="form-label required" for="password">Password</label>
                  <input v-model="password" class="form-control" type="password" id="password"
                    placeholder="Enter password" @input="clearError('password')" />
                  <span class="text-danger">{{ validationErrors.password }}</span>
                </div>
                <div class="mb-3">
                  <label class="form-label required" for="confirmPassword">Confirm Password</label>
                  <input v-model="confirmPassword" class="form-control" type="password" id="confirm-password"
                    placeholder="Confirm password" @input="clearError('confirmPassword')" />
                  <span class="text-danger">{{ validationErrors.confirmPassword }}</span>
                </div>
              </div>
              <div class="mb-3">
                <button type="button" class="btn btn-primary d-block w-100 mt-3" @click="submitUserDetails">
                  Create account
                </button>
              </div>
              <div class="col-auto fs--1 text-600 text-center">
                <span class="mb-0 fw-semi-bold">Already have an account? </span>
                <span>
                  <a class="fw-bold" href="/login">Login</a>
                </span>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AuthService from '../services/auth.service';

export default {
  name: "PageRegister",

  data() {
    return {
      validationErrors: {},
      name: "",
      studentId: "",
      email: "",
      password: "",
      confirmPassword: "",
    }
  },

  methods: {
    clearError(fieldName) {
      if (this.validationErrors[fieldName]) {
        this.validationErrors[fieldName] = "";
      }
    },

    validateForm() {
      this.validationErrors = {};

      if (!this.name) {
        this.validationErrors.name = "Name is required";
      }

      if (!this.studentId) {
        this.validationErrors.name = "Student ID is required";
      }

      if (!this.email) {
        this.validationErrors.email = "Email address is required";
      }

      if (!this.password) {
        this.validationErrors.password = "Password is required";
      }

      if (!this.confirmPassword) {
        this.validationErrors.confirmPassword = "Confirm Password is required";
      } else if (this.password !== this.confirmPassword) {
        this.validationErrors.confirmPassword = "Passwords do not match";
      }

      return Object.keys(this.validationErrors).length === 0;
    },

    async submitUserDetails() {
      if (!this.validateForm()) {
        return;
      }
      const userDetails = {};

      if (this.name) {
        userDetails.name = this.name;
      }
      if (this.studentId) {
        userDetails.studentId = this.studentId;
      }
      if (this.email) {
        userDetails.email = this.email;
      }
      if (this.password) {
        userDetails.password = this.password;
      }

      try {
        await AuthService.register(userDetails);
        this.validationErrors = {};
        this.$router.push({
          name: 'PageLogin',
        });
      } catch (error) {
        console.log(error);
      }
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "../vendors/simplebar/simplebar.min.css";
@import "../assets/css/user.min.css";
@import "../assets/css/theme.min.css";
@import "https://fonts.googleapis.com/css?family=Open+Sans:300,400,500,600,700%7cPoppins:300,400,500,600,700,800,900&amp;display=swap";

.required::after {
  content: " *";
  color: red;
}
</style>