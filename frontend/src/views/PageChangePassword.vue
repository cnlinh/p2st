<template>
  <div class="row flex-center min-vh-100 py-6">
    <div class="col-sm-10 col-md-8 col-lg-6 col-xl-5 col-xxl-4">
      <div class="d-flex flex-center mb-4">
        <a class="navbar-brand" href="/home">
          <div class="d-flex align-items-center py-3">
            <span class="font-sans-serif fw-bolder fs-5 d-inline-block text-black">CS3243</span>
          </div>
        </a>
      </div>
      <div class="card">
        <div class="card-body p-4 p-sm-5">
          <div class="row flex-between-center mb-2">
            <div class="col-auto">
              <h5>Change Password</h5>
            </div>
          </div>
          <form>
            <div class="mb-3">
              <label class="form-label required" for="email">Email</label>
              <input v-model="email" class="form-control" type="email" id="email" placeholder="Enter email"
                @input="clearError('email')" />
              <span class="text-danger">{{ validationErrors.email }}</span>
            </div>
            <div class="mb-3">
              <label class="form-label required" for="currentPassword">Current Password</label>
              <input v-model="currentPassword" class="form-control" type="password" id="currentPassword" 
                placeholder="Enter current password" @input="clearError('currentPassword')" />
              <span class="text-danger">{{ validationErrors.currentPassword }}</span>
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
            <div class="mb-3">
              <button type="button" class="btn btn-primary d-block w-100 mt-3" @click="submitChangePassword">
                Change Password
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
  name: "PageChangePassword",

  data() {
    return {
      validationErrors: {},
      email: "",
      currentPassword: "",
      newPassword: "",
      confirmNewPassword: "",
    };
  },

  methods: {
    clearError(fieldName) {
      if (this.validationErrors[fieldName]) {
        this.validationErrors[fieldName] = "";
      }
    },

    validateForm() {
      this.validationErrors = {};

      if (!this.email) {
        this.validationErrors.email = "Email address is required";
      }

      if (!this.currentPassword) {
        this.validationErrors.currentPassword = "Current password is required";
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

    async submitChangePassword() {
      if (!this.validateForm()) {
        return;
      }
      const passwordDetails = {
        email: this.email,
        currentPassword: this.currentPassword,
        newPassword: this.newPassword
      };

      try {
        await AuthService.changePassword(passwordDetails);
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
