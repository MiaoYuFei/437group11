<script lang="ts">
import $ from "jquery";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { VueRecaptcha } from "vue-recaptcha";
import BsAlert from "@/components/BsAlert.vue";
import BsButton from "@/components/BsButton.vue";
import { disableForm, enableForm, focusForm, handleApi } from "@/utilities";

export default {
  data() {
    return {
      loading: false,
      passwordMatch: true,
      recaptchaChecked: true,
      recaptchaResponse: "",
      termsChecked: true,
      formAlertMessage: "unknown error",
    };
  },
  watch: {
    loading(newValue) {
      const formAlert = this.$refs.formAlert as typeof BsAlert;
      if (newValue) {
        formAlert.hide();
        disableForm(this.$refs.form);
        $(this.$refs.recaptchaContainer as Element).hide();
      } else {
        formAlert.show();
        enableForm(this.$refs.form);
        $(this.$refs.recaptchaContainer as Element).show();
        (this.$refs.recaptcha as VueRecaptcha).reset();
      }
    },
  },
  methods: {
    onFormSubmit: function () {
      if (!this.passwordMatch) {
        return false;
      }
      if (!this.termsChecked) {
        return false;
      }
      if (!$(this.$refs.terms as Element).is(":checked")) {
        this.termsChecked = false;
        return false;
      }
      if (this.recaptchaResponse == "") {
        this.recaptchaChecked = false;
        return false;
      }
      const lastRecaptchaResponse = this.recaptchaResponse;
      this.recaptchaChecked = true;
      this.recaptchaResponse = "";
      this.loading = true;
      handleApi(this.$refs.form, ["username", "password", "email"], {
        recaptch: lastRecaptchaResponse,
      }).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            window.location.href = "/";
          } else {
            this.formAlertMessage = response.data.data.message;
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
    onFormChange: function () {
      const form = $(this.$refs.form as Element);
      this.passwordMatch =
        form.find("input[name='password']").val() ===
          form.find("input[name='passwordConfirmation']").val() ||
        form.find("input[name='passwordConfirmation']").val() === "";
    },
    onFormAlertClosed: function () {
      focusForm(this.$refs.form);
    },
    onRecaptchaExpired: function () {
      this.recaptchaResponse = "";
      this.recaptchaChecked = false;
    },
    onRecaptchaChecked: function (response: string) {
      this.recaptchaResponse = response;
      this.recaptchaChecked = true;
    },
    onTermsChecked: function () {
      const checked = $(this.$refs.terms as Element).is(":checked");
      if (checked) {
        this.termsChecked = true;
      }
    },
  },
  mounted() {
    const form = $(this.$refs.form as Element);
    form
      .find("input")
      .on("change keydown keyup keypress paste", this.onFormChange);
    focusForm(this.$refs.form);
  },
  components: {
    FontAwesomeIcon,
    VueRecaptcha,
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
        class="card col-12 col-md-10 col-lg-8 col-xl-6 col-xxl-4"
        style="box-shadow: 0.2rem 0.2rem 0.1rem #eee"
      >
        <div class="card-body p-4">
          <form
            action="/api/user/register"
            method="post"
            @submit.prevent="onFormSubmit"
            ref="form"
          >
            <h3 class="card-title mb-4">
              <FontAwesomeIcon icon="fa-user-plus" class="me-3" />Register
            </h3>
            <div class="input-group mb-3">
              <span class="input-group-text">@</span>
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  id="inputUsername"
                  name="username"
                  placeholder="Username"
                  required
                  autofocus
                />
                <label for="inputUsername">Username</label>
              </div>
            </div>
            <div class="form-floating mb-3">
              <input
                type="password"
                class="form-control"
                id="inputPassword"
                name="password"
                placeholder="Password"
                required
              />
              <label for="inputPassword">Password</label>
            </div>
            <div class="form-floating mb-3">
              <input
                type="password"
                class="form-control"
                id="inputPasswordConfirmation"
                name="passwordConfirmation"
                placeholder="Password Confirmation"
                required
              />
              <label for="inputPasswordConfirmation"
                >Password Confirmation</label
              >
              <span v-if="!passwordMatch" class="text-danger"
                >Password and confirmation don&apos;t match.</span
              >
            </div>
            <div class="form-floating mb-3">
              <input
                type="email"
                class="form-control"
                id="inputEmail"
                name="email"
                placeholder="Email"
                required
              />
              <label for="inputEmail">Email</label>
            </div>
            <div class="mb-3">
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  value=""
                  id="inputTerms"
                  @click="onTermsChecked"
                  ref="terms"
                />
                <label class="form-check-label" for="inputTerms">
                  I agree to
                  <RouterLink to="/" target="_blank"
                    >terms of service</RouterLink
                  >.
                </label>
              </div>
              <span v-if="!termsChecked" class="text-danger"
                >You have to agree with the terms of service.</span
              >
            </div>
            <div class="mb-3" ref="recaptchaContainer">
              <VueRecaptcha
                sitekey="6LeQ5LQkAAAAAJ4QjiBn6F9P9lyX76eVMSFGX72X"
                @verify="onRecaptchaChecked"
                @expired="onRecaptchaExpired"
                ref="recaptcha"
              >
              </VueRecaptcha>
              <span v-if="!recaptchaChecked" class="text-danger"
                >Please complete the reCAPTCHA verification.</span
              >
            </div>
            <div class="mb-3">
              <BsButton
                type="submit"
                class="btn-lg btn-block me-3"
                :loading="loading"
                bgColor="dark"
                textColor="light"
                ref="registerButton"
              >
                Register
              </BsButton>
            </div>
            <div>
              <BsAlert
                class="mb-3"
                :message="formAlertMessage"
                bgColor="warning"
                @closed="onFormAlertClosed"
                ref="formAlert"
              ></BsAlert>
            </div>
            <div>
              Already have a stocknews account?
              <RouterLink to="/signin">
                <span>Sign in here.</span>
              </RouterLink>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
