<template>
  <div class="row flex-center min-vh-100 py-6">
    <div class="col-sm-10 col-md-8 col-lg-6 col-xl-5 col-xxl-4">
      <div class="d-flex flex-center mb-4">
        <a class="navbar-brand" href="/home">
          <div class="d-flex align-items-center py-3">
            <span class="font-sans-serif fw-bolder fs-5 d-inline-block text-black">P2ST</span>
          </div>
        </a>
      </div>
      <div class="card">
        <div class="card-body p-4 p-sm-5">
          <div class="row flex-between-center mb-2">
            <div class="col-auto">
              <h5>Reset Password</h5>
            </div>
            <div class="col-auto fs--1 text-600"><span class="mb-0 undefined">or</span> <span><a href="/login">Log
                  in</a></span></div>
          </div>
          <form>
            <div class="mb-3">
              <label class="form-label required" for="name">Name</label>
              <input v-model="name" class="form-control" type="text" id="name" placeholder="Enter name"
                @input="clearError('name')" />
              <span class="text-danger">{{ validationErrors.name }}</span>
            </div>
            <div class="mb-3">
              <label class="form-label required" for="name">Student ID</label>
              <input v-model="studentId" class="form-control" type="text" id="student-id" placeholder="Enter student id"
                @input="clearError('studentId')" />
              <span class="text-danger">{{ validationErrors.studentId }}</span>
            </div>
            <div class="mb-3">
              <label class="form-label required" for="email">Email</label>
              <input v-model="email" class="form-control" type="email" id="email" placeholder="Enter email"
                @input="clearError('email')" />
              <span class="text-danger">{{ validationErrors.email }}</span>
            </div>
            <div class="mb-3">
              <label class="form-label required" for="newPassword">New Password</label>
              <input v-model="newPassword" class="form-control" type="password" id="newPassword"
                placeholder="Enter new password" @input="clearError('newPassword')" />
              <span class="text-danger">{{ validationErrors.newPassword }}</span>
            </div>
            <div class="mb-3">
              <label class="form-label required" for="confirmNewPassword">Confirm New Password</label>
              <input v-model="confirmNewPassword" class="form-control" type="password" id="confirmNewPassword"
                placeholder="Confirm new password" @input="clearError('confirmNewPassword')" />
              <span class="text-danger">{{ validationErrors.confirmNewPassword }}</span>
            </div>
            <span class="text-danger">{{ apiError }}</span>
            <div class="mb-3">
              <button type="button" class="btn btn-primary d-block w-100 mt-3" @click="submitResetPassword">
                Reset Password
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
  name: "PageResetPassword",

  data() {
    return {
      validationErrors: {},
      apiError: "",
      name: "",
      studentId: "",
      email: "",
      newPassword: "",
      confirmNewPassword: "",
    };
  },

  methods: {
    clearError(fieldName) {
      if (this.validationErrors[fieldName]) {
        this.validationErrors[fieldName] = "";
      }
      this.apiError = "";
    },

    validateForm() {
      this.validationErrors = {};

      if (!this.name) {
        this.validationErrors.name = "Name is required";
      }

      if (!this.studentId) {
        this.validationErrors.studentId = "Student ID is required";
      }

      if (!this.email) {
        this.validationErrors.email = "Email address is required";
      }

      if (!this.newPassword) {
        this.validationErrors.newPassword = "New password is required";
      }

      if (!this.confirmNewPassword) {
        this.validationErrors.confirmNewPassword = "Confirm new password is required";
      } else if (this.newPassword !== this.confirmNewPassword) {
        this.validationErrors.confirmNewPassword = "New passwords do not match";
      }

      return Object.keys(this.validationErrors).length === 0;
    },

    async submitResetPassword() {
      if (!this.validateForm()) {
        return;
      }
      const passwordDetails = {
        name: this.name,
        studentId: this.studentId,
        email: this.email,
        newPassword: this.newPassword
      };

      try {
        await AuthService.resetPassword(passwordDetails);
        this.validationErrors = {};
        this.$router.push({
          name: 'PageLogin',
        });
      } catch (error) {
        console.log(error);

        if (error.response && error.response.data) {
          if (error.response.data.name) {
            this.validationErrors.name = error.response.data.name.join("\n");
          }
          if (error.response.data.email) {
            this.validationErrors.email = error.response.data.email.join("\n");
          } 
          if (error.response.data.student_id) {
            this.validationErrors.studentId = error.response.data.student_id.join("\n");
          }
          if (error.response.data.new_password) {
            this.validationErrors.newPassword = error.response.data.new_password.join("\n");
          }
          if (Array.isArray(error.response.data)) {
            this.apiError = error.response.data.join("\n");
          }
        }
      }
    }
  },
}
</script>
  
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
  