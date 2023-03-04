<script lang="ts">
import $ from "jquery";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { VueRecaptcha } from "vue-recaptcha";
import {
  disableForm,
  enableForm,
  focusForm,
  getFormData,
  handleApi,
} from "@/utilities";

export default {
  data() {
    return {
      passwordMatch: true,
      passwordWeak: false,
      recaptchaChecked: true,
      recaptchaResponse: "",
      termsChecked: true,
      formLoading: false,
      formAlertMessage: "unknown error",
    };
  },
  watch: {
    loading(newValue) {
      const formAlert = $(this.$refs.formAlert as Element);
      if (newValue) {
        formAlert.fadeOut();
        disableForm(this.$refs.form);
        $(this.$refs.recaptchaContainer as Element).hide();
      } else {
        formAlert.css("display", "flex").hide().fadeIn();
        enableForm(this.$refs.form);
        $(this.$refs.recaptchaContainer as Element).show();
        (this.$refs.recaptcha as VueRecaptcha).reset();
      }
    },
  },
  methods: {
    onFormSubmit() {
      if (!this.passwordMatch) {
        return false;
      }
      if (
        (
          $(this.$refs.form as Element)
            .find("input[name='password']")
            .val() as any
        ).length < 6
      ) {
        this.passwordWeak = true;
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
      this.formLoading = true;
      const apiData = getFormData(this.$refs.form, ["email", "password"]);
      apiData["recaptcha_response"] = lastRecaptchaResponse;
      handleApi("post", "/api/user/register", apiData).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            (this.$refs.form as any).reset();
            this.formLoading = false;
            this.$router.push("/verifyEmail");
          } else {
            this.formAlertMessage = response.data.data.reason;
            this.formLoading = false;
          }
        },
        (error) => {
          this.formAlertMessage = error.message;
          this.formLoading = false;
        }
      );
      return true;
    },
    onFormChange() {
      const form = $(this.$refs.form as Element);
      this.passwordMatch =
        form.find("input[name='password']").val() ===
          form.find("input[name='passwordConfirmation']").val() ||
        form.find("input[name='passwordConfirmation']").val() === "";
      this.passwordWeak =
        (form.find("input[name='password']").val() as any).length < 6 &&
        (form.find("input[name='passwordConfirmation']").val() as any).length !=
          0;
    },
    onFormAlertClose() {
      $(this.$refs.formAlert as Element).fadeOut();
      focusForm(this.$refs.form);
    },
    onRecaptchaExpired() {
      this.recaptchaResponse = "";
      this.recaptchaChecked = false;
    },
    onRecaptchaChecked(response: string) {
      this.recaptchaResponse = response;
      this.recaptchaChecked = true;
    },
    onTermsChecked() {
      const checked = $(this.$refs.terms as Element).is(":checked");
      if (checked) {
        this.termsChecked = true;
      }
    },
  },
  created() {
    document.title = "Register - " + (this as any).$projectName;
  },
  mounted() {
    (this.$refs.form as any).reset();
    $(this.$refs.formAlert as Element).hide();
    this.formLoading = false;
    $(this.$refs.form as Element)
      .find("input")
      .on("change keydown keyup keypress paste", this.onFormChange);
    focusForm(this.$refs.form);
  },
  components: {
    FontAwesomeIcon,
    VueRecaptcha,
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
          <form @submit.prevent="onFormSubmit" ref="form">
            <h3 class="card-title mb-4">
              <FontAwesomeIcon icon="fa-user-plus" class="me-3" />Register
            </h3>
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
              <span v-if="passwordWeak" class="text-danger d-block"
                >Password minimum length is 6.</span
              >
              <span v-if="!passwordMatch" class="text-danger d-block"
                >Password and confirmation don&apos;t match.</span
              >
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
                    >Terms &amp; Conditions</RouterLink
                  >.
                </label>
              </div>
              <span v-if="!termsChecked" class="text-danger"
                >You have to agree with the terms and conditions.</span
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
              <button
                type="submit"
                class="btn btn-dark text-light btn-lg btn-block d-flex align-items-center me-3"
              >
                <span v-if="!formLoading">Register</span>
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
