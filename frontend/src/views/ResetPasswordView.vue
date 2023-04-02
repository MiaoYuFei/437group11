<script lang="ts">
import $ from "jquery";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  disableForm,
  enableForm,
  focusForm,
  getFormData,
  handleApi,
} from "@/utilities";

export default {
  props: {
    userStatus: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      formSendEmailLoading: false,
      formSendEmailAlertMessage: "unknown error",
    };
  },
  watch: {
    formSendEmailLoading(newValue) {
      const formAlert = $(this.$refs.formSendEmailAlert as Element);
      if (newValue) {
        formAlert.fadeOut();
        disableForm(this.$refs.formSendEmail);
      } else {
        formAlert.css("display", "flex").hide().fadeIn();
        enableForm(this.$refs.formSendEmail);
      }
    },
  },
  methods: {
    onFormSendEmailSubmit() {
      this.formSendEmailLoading = true;
      const apiData = getFormData(this.$refs.formSendEmail, ["email"]);
      apiData["requestType"] = "reset_password";
      handleApi("post", "/api/user/verifyemail", apiData).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            (this.$refs.formSendEmail as any).reset();
            this.formSendEmailLoading = false;
            this.formSendEmailAlertMessage =
              "If there is an account associated with this email address, it will receive a password reset email.";
          } else {
            this.formSendEmailAlertMessage = response.data.data.reason;
            this.formSendEmailLoading = false;
          }
        },
        (error) => {
          this.formSendEmailAlertMessage = error.message;
          this.formSendEmailLoading = false;
        }
      );
      return true;
    },
    onFormSendEmailAlertClose() {
      $(this.$refs.formSendEmailAlert as Element).fadeOut();
      focusForm(this.$refs.formSendEmail);
    },
  },
  created() {
    document.title = "Reset password - " + (this as any).$projectName;
  },
  mounted() {
    (this.$refs.formSendEmail as any).reset();
    $(this.$refs.formSendEmailAlert as Element).hide();
    this.formSendEmailLoading = false;
    focusForm(this.$refs.formSendEmail);
  },
  components: {
    FontAwesomeIcon,
  },
};
</script>
<template>
  <div>
    <div
      class="container d-flex flex-column align-items-center justify-content-center"
      style="min-height: 100%"
    >
      <div
        class="card col-12 col-md-10 col-lg-8 col-xl-6 col-xxl-5"
        style="box-shadow: 0.2rem 0.2rem 0.1rem #eee"
      >
        <div class="card-body p-4">
          <h3 class="card-title mb-4">
            <FontAwesomeIcon icon="fa-lock" class="me-3" />Reset Password
          </h3>
          <div class="mb-3">
            <span
              >To reset your password, we will send a link to your email
              address.</span
            >
          </div>
          <form @submit.prevent="onFormSendEmailSubmit" ref="formSendEmail">
            <div class="input-group mb-3">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  id="inputEmail"
                  name="email"
                  placeholder="Email"
                  required
                  autofocus
                />
                <label for="inputEmail">Email</label>
              </div>
            </div>
            <div class="mb-3">
              <button
                type="submit"
                class="btn btn-dark text-light btn-lg btn-block d-flex align-items-center me-3"
              >
                <span v-if="!formSendEmailLoading">Send Email</span>
                <div
                  v-if="formSendEmailLoading"
                  class="spinner-border"
                  role="status"
                >
                  <span class="visually-hidden">Loading...</span>
                </div>
              </button>
            </div>
            <div class="mb-3">
              <div
                class="alert alert-warning align-items-center mb-0"
                role="alert"
                aria-hidden="true"
                ref="formSendEmailAlert"
              >
                <FontAwesomeIcon icon="fa-circle-exclamation" />
                <span class="mx-2">
                  {{ formSendEmailAlertMessage }}
                </span>
                <button
                  type="button"
                  class="btn-close ms-auto"
                  aria-label="Close"
                  @click="onFormSendEmailAlertClose"
                ></button>
              </div>
            </div>
            <div>
              <RouterLink to="/signin">
                <span>Go back to sign in.</span>
              </RouterLink>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
