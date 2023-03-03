<script lang="ts">
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import BsAlert from "@/components/BsAlert.vue";
import BsButton from "@/components/BsButton.vue";
import { disableForm, enableForm, handleApi } from "@/utilities";

export default {
  data() {
    return {
      loading: false,
      formAlertMessage: "unknown error",
      submitButtonTimer: 0,
      submitButtonSeconds: 0,
    };
  },
  watch: {
    loading(newValue: Boolean) {
      const formAlert = this.$refs.formAlert as typeof BsAlert;
      if (newValue) {
        formAlert.hide();
      } else {
        formAlert.show();
      }
    },
  },
  methods: {
    onFormSubmit: function () {
      this.loading = true;
      disableForm(this.$refs.form);
      const apiData = {
        requestType: "registration",
      };
      handleApi("post", "/api/user/verifyemail", apiData).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            (this.$refs.form as any).reset();
            this.loading = false;
            this.formAlertMessage =
              "Email sent! Please check your email account.";
            this.submitButtonSeconds = 30;
            this.submitButtonTimer = window.setInterval(this.onTimerTick, 1000);
          } else {
            this.formAlertMessage = response.data.data.reason;
            this.loading = false;
            enableForm(this.$refs.form);
          }
        },
        (error) => {
          this.formAlertMessage = error.message;
          this.loading = false;
          enableForm(this.$refs.form);
        }
      );
      return true;
    },
    onProceed: function () {
      this.$router.push("/myfeeds");
    },
    onTimerTick: function () {
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
    this.loading = false;
    this.onFormSubmit();
  },
  components: {
    FontAwesomeIcon,
    BsAlert,
    BsButton,
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
              <BsButton
                type="submit"
                class="btn-block me-3"
                :loading="loading"
                bgColor="primary"
                textColor="light"
                ref="formSubmit"
              >
                Send verification email<span v-if="submitButtonSeconds > 0">
                  ({{ submitButtonSeconds }}s)</span
                >
              </BsButton>
            </div>
            <div class="mb-3">
              <BsAlert
                class="mb-3"
                :message="formAlertMessage"
                bgColor="warning"
                ref="formAlert"
              ></BsAlert>
            </div>
          </form>
          <div class="mb-3">
            <span
              >After email verification, you can proceed to your feeds
              page.</span
            >
          </div>
          <div>
            <BsButton
              type="button"
              class="btn-block me-3"
              bgColor="secondary"
              textColor="light"
              @click="onProceed"
            >
              Go to My Feeds page
            </BsButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
