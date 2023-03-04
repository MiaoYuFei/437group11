<script lang="ts">
import $ from "jquery";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { disableForm, enableForm, handleApi } from "@/utilities";

export default {
  data() {
    return {
      formLoading: false,
      formAlertMessage: "unknown error",
      submitButtonTimer: 0,
      submitButtonSeconds: 0,
    };
  },
  watch: {
    formLoading(newValue: Boolean) {
      const formAlert = $(this.$refs.formAlert as Element);
      if (newValue) {
        formAlert.fadeOut();
      } else {
        formAlert.css("display", "flex").hide().fadeIn();
      }
    },
  },
  methods: {
    onFormSubmit() {
      this.formLoading = true;
      disableForm(this.$refs.form);
      const apiData = {
        requestType: "registration",
      };
      handleApi("post", "/api/user/verifyemail", apiData).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            (this.$refs.form as any).reset();
            this.formLoading = false;
            this.formAlertMessage =
              "Email sent! Please check your email account.";
            this.submitButtonSeconds = 30;
            this.submitButtonTimer = window.setInterval(this.onTimerTick, 1000);
          } else {
            this.formAlertMessage = response.data.data.reason;
            this.formLoading = false;
            enableForm(this.$refs.form);
          }
        },
        (error) => {
          this.formAlertMessage = error.message;
          this.formLoading = false;
          enableForm(this.$refs.form);
        }
      );
      return true;
    },
    onFormAlertClose() {
      $(this.$refs.formAlert as Element).fadeOut();
    },
    onTimerTick() {
      if (this.submitButtonSeconds > 0) {
        this.submitButtonSeconds -= 1;
      } else {
        window.clearInterval(this.submitButtonTimer);
        enableForm(this.$refs.form);
      }
    },
  },
  created() {
    document.title = "Email verification - " + (this as any).$projectName;
  },
  mounted() {
    (this.$refs.form as any).reset();
    $(this.$refs.formAlert as Element).hide();
    this.formLoading = false;
    this.onFormSubmit();
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
            <FontAwesomeIcon icon="fa-envelope" class="me-3" />Email
            verification
          </h3>
          <div class="mb-3">
            <span
              >For security reasons, please follow instructions to verify your
              email address to finish registration.</span
            >
          </div>
          <form @submit.prevent="onFormSubmit" ref="form">
            <div class="mb-3">
              <button
                type="submit"
                class="btn btn-dark text-light btn-lg btn-block d-flex align-items-center me-3"
              >
                <span v-if="!formLoading">
                  Send verification email<span v-if="submitButtonSeconds > 0">
                    ({{ submitButtonSeconds }}s)</span
                  ></span
                >
                <div v-if="formLoading" class="spinner-border" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </button>
            </div>
            <div class="mb-3">
              <div
                class="alert alert-warning align-items-center mb-0"
                role="alert"
                aria-hidden="true"
                ref="formAlert"
              >
                <FontAwesomeIcon icon="fa-circle-exclamation" />
                <span class="mx-2">
                  {{ formAlertMessage }}
                </span>
                <button
                  type="button"
                  class="btn-close ms-auto"
                  aria-label="Close"
                  @click="onFormAlertClose"
                ></button>
              </div>
            </div>
          </form>
          <div class="mb-3">
            <span
              >After email verification, you can proceed to your feeds
              page.</span
            >
          </div>
          <div>
            <RouterLink to="/myfeeds">
              <span>Go to My Feeds page</span>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
