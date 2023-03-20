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
    };
  },
  watch: {
    loading(newValue) {
      const formAlert = this.$refs.formAlert as typeof BsAlert;
      if (newValue) {
        formAlert.hide();
        disableForm(this.$refs.form);
      } else {
        formAlert.show();
        enableForm(this.$refs.form);
      }
    },
  },
  methods: {
    onFormSubmit: function () {
      this.loading = true;
      const apiData: { [key: string]: string } = {};
      apiData["type"] = "email";
      handleApi("post", "/api/user/getonetimecode", apiData).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            (this.$refs.form as any).reset();
            this.loading = false;
            this.formAlertMessage =
              "Email sent! Please check your email account.";
          } else {
            this.formAlertMessage = response.data.data.reason;
            this.loading = false;
          }
        },
        (error) => {
          this.formAlertMessage = error.message;
          this.loading = false;
        }
      );
      return true;
    },
    onProceed: function () {
      this.$router.push("/myfeeds");
    },
  },
  created() {
    document.title = "Reset password - " + (this as any).$projectName;
  },
  mounted() {
    (this.$refs.form as any).reset();
    this.loading = false;
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
            <FontAwesomeIcon icon="fa-lock" class="me-3" />Reset Password
          </h3>
          <div class="mb-3">
            <span
              >For your security, we will send an one time code to your email
              address.</span
            >
          </div>
          <form @submit.prevent="onFormSubmit" ref="form">
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
              <BsButton
                type="submit"
                class="btn-block me-3"
                :loading="loading"
                bgColor="secondary"
                textColor="light"
                ref="formSubmit"
              >
                Send verification email
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
          <form>
            <div class="form-floating mb-3">
              <input
                type="text"
                class="form-control"
                id="inputOneTimeCode"
                name="onetimecode"
                placeholder="One Time Code"
                required
              />
              <label for="inputPassword">One Time Code</label>
            </div>
            <div>
              <BsButton
                type="button"
                class="btn-block me-3"
                bgColor="secondary"
                textColor="light"
                @click="onProceed"
              >
                Confirm
              </BsButton>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
