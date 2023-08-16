<template>
  <div class="row flex-center min-vh-100 py-6">
    <div class="col-sm-10 col-md-8 col-lg-6 col-xl-5 col-xxl-4">
      <div class="d-flex flex-center mb-4"><a class="navbar-brand" href="/home">
          <div class="d-flex align-items-center py-3"><span
              class="font-sans-serif fw-bolder fs-5 d-inline-block text-black">CS3243</span>
          </div>
        </a></div>
      <div class="card">
        <div class="card-body p-4 p-sm-5">
          <div class="row flex-between-center mb-2">
            <div class="col-auto">
              <h5>Register</h5>
            </div>
            <div class="col-auto fs--1 text-600"><span class="mb-0 undefined">Have an account?</span> <span><a
                  href="/login">Login</a></span></div>
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
                <input v-model="password" class="form-control" type="password" id="password" placeholder="Enter password"
                  @input="clearError('password')" />
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
          </form>
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