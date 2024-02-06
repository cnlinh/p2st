<template>
  <!-- Change Student ID Modal -->
  <div class="modal fade" tabindex="-1" role="dialog" ref="modalStudentId">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Change Student ID</h5>
        </div>
        <div class="modal-body">
          <form class="needs-validation" novalidate="">
            <div class="form-group">
              <label for="student-id" class="required">New Student ID</label>
              <input v-model="studentId" type="text" class="form-control" id="student-id" placeholder="Enter new student ID" @input="clearError('studentId')">
              <span class="text-danger">{{ validationErrors.studentId }}</span>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="cancel">Cancel</button>
          <button type="button" class="btn btn-primary" @click="submitStudentId">Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
export default {
  name: "ModalChangeStudentId",

  data() {
    return {
      validationErrors: {},
      modalStudentId: null,
      studentId: "",
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

      if (!this.studentId) {
        this.validationErrors.studentId = "Student ID is required";
      }

      return Object.keys(this.validationErrors).length === 0;
    },

    clear() {
      this.studentId = "";
    },

    show() {
      this.modalStudentId.show();
    },

    cancel() {
      this.modalStudentId.hide();
      this.clear();
      this.validationErrors = {};
      this.$emit('cancel');
    },

    confirm() {
      this.modalStudentId.hide();
      this.clear();
      this.validationErrors = {};
      this.$emit('confirm', this.studentId);
    },

    async submitStudentId() {
      if (!this.validateForm()) {
        return;
      }
      try {
        //await AdminService.changeStudentId(this.studentId);
        this.confirm();
      } catch (error) {
        console.log(error);
        // Handle errors, e.g., show error message
      }
    },
  },

  mounted() {
    this.modalStudentId = new Modal(this.$refs.modalStudentId);
  },
}
</script>

<style scoped>
.required::after {
  content: " *";
  color: red;
}
</style>