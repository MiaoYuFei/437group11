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
  data() {
    return {
      formPasswordLoading: false,
      formPasswordAlertMessage: "unknown error",
      formLinkLoading: false,
      formLinkAlertMessage: "unknown error",
    };
  },
  watch: {
    formPasswordLoading(newValue) {
      const formAlert = $(this.$refs.formPasswordAlert as Element);
      if (newValue) {
        formAlert.fadeOut();
        disableForm(this.$refs.formPassword);
      } else {
        formAlert.css("display", "flex").hide().fadeIn();
        enableForm(this.$refs.formPassword);
      }
    },
    formLinkLoading(newValue) {
      const formAlert = $(this.$refs.formLinkAlert as Element);
      if (newValue) {
        formAlert.fadeOut();
        disableForm(this.$refs.formLink);
      } else {
        formAlert.css("display", "flex").hide().fadeIn();
        enableForm(this.$refs.formLink);
      }
    },
  },
  methods: {
    onFormPasswordSubmit() {
      this.formPasswordLoading = true;
      const apiData = getFormData(this.$refs.formPassword, [
        "email",
        "password",
      ]);
      apiData["requestType"] = "email_password";
      handleApi("post", "/api/user/signin", apiData).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            (this.$refs.formPassword as any).reset();
            this.formPasswordLoading = false;
            this.$router.push("/myreadinglist");
          } else {
            this.formPasswordAlertMessage = response.data.data.reason;
            this.formPasswordLoading = false;
          }
        },
        (error) => {
          this.formPasswordAlertMessage = error.message;
          this.formPasswordLoading = false;
        }
      );
      return true;
    },
    onFormPasswordAlertClose() {
      $(this.$refs.formPasswordAlert as Element).fadeOut();
      focusForm(this.$refs.formPassword);
    },
    onFormLinkSubmit() {
      this.formLinkLoading = true;
      const apiData = getFormData(this.$refs.formLink, ["email"]);
      apiData["requestType"] = "sign_in";
      handleApi("post", "/api/user/verifyemail", apiData).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            this.formLinkAlertMessage =
              "Sign in link sent. Please check your email account.";
            this.formLinkLoading = false;
          } else {
            this.formLinkAlertMessage = response.data.data.reason;
            this.formLinkLoading = false;
          }
        },
        (error) => {
          this.formLinkAlertMessage = error.message;
          this.formLinkLoading = false;
        }
      );
    },
    onFormLinkAlertClose() {
      $(this.$refs.formLinkAlert as Element).fadeOut();
      focusForm(this.$refs.formLink);
    },
  },
  created() {
    document.title = "Sign in - " + (this as any).$projectName;
  },
  mounted() {
    (this.$refs.formPassword as any).reset();
    (this.$refs.formLink as any).reset();
    $(this.$refs.formPasswordAlert as Element).hide();
    $(this.$refs.formLinkAlert as Element).hide();
    this.formPasswordLoading = false;
    this.formLinkLoading = false;
    focusForm(this.$refs.formPassword);
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
            <FontAwesomeIcon icon="fa-user" class="me-3" />Sign In
          </h3>
          <ul class="nav nav-tabs" id="myTab" role="tablist">
            <li class="nav-item" role="presentation">
              <button
                class="nav-link active"
                id="idTabEmailPassword"
                data-bs-toggle="tab"
                data-bs-target="#idPaneEmailPassword"
                type="button"
                role="tab"
                aria-controls="idPaneEmailPassword"
                aria-selected="true"
              >
                Password
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button
                class="nav-link"
                id="idTabEmailLink"
                data-bs-toggle="tab"
                data-bs-target="#idPaneEmailLink"
                type="button"
                role="tab"
                aria-controls="idPaneEmailLink"
                aria-selected="false"
              >
                Link
              </button>
            </li>
          </ul>
          <div class="tab-content" id="myTabContent">
            <div
              class="tab-pane fade show active"
              id="idPaneEmailPassword"
              role="tabpanel"
              aria-labelledby="idTabEmailPassword"
              tabindex="0"
            >
              <form @submit.prevent="onFormPasswordSubmit" ref="formPassword">
                <div class="input-group mt-3 mb-3">
                  <div class="form-floating">
                    <input
                      type="text"
                      class="form-control"
                      id="inputPasswordEmail"
                      name="email"
                      placeholder="Email"
                      required
                      autofocus
                    />
                    <label for="inputPasswordEmail">Email</label>
                  </div>
                </div>
                <div class="form-floating mb-3">
                  <input
                    type="password"
                    class="form-control"
                    id="inputPasswordPassword"
                    name="password"
                    placeholder="Password"
                    required
                  />
                  <label for="inputPasswordPassword">Password</label>
                </div>
                <div class="mb-3">
                  <button
                    type="submit"
                    class="btn btn-dark text-light btn-lg btn-block d-flex align-items-center me-3"
                  >
                    <span v-if="!formPasswordLoading">Sign in</span>
                    <div
                      v-if="formPasswordLoading"
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
                    ref="formPasswordAlert"
                  >
                    <FontAwesomeIcon icon="fa-circle-exclamation" />
                    <span class="mx-2">
                      {{ formPasswordAlertMessage }}
                    </span>
                    <button
                      type="button"
                      class="btn-close ms-auto"
                      aria-label="Close"
                      @click="onFormPasswordAlertClose"
                    ></button>
                  </div>
                </div>
                <div>
                  <RouterLink to="/resetpassword">Forgot password?</RouterLink>
                </div>
              </form>
            </div>
            <div
              class="tab-pane fade"
              id="idPaneEmailLink"
              role="tabpanel"
              aria-labelledby="idTabEmailLink"
              tabindex="0"
            >
              <form @submit.prevent="onFormLinkSubmit" ref="formLink">
                <div class="input-group mt-3 mb-3">
                  <div class="form-floating">
                    <input
                      type="text"
                      class="form-control"
                      id="inputLinkEmail"
                      name="email"
                      placeholder="Email"
                      required
                      autofocus
                    />
                    <label for="inputLinkEmail">Email</label>
                  </div>
                </div>
                <div class="mb-3">
                  <button
                    type="submit"
                    class="btn btn-dark text-light btn-lg btn-block d-flex align-items-center me-3"
                  >
                    <span v-if="!formLinkLoading">Send Link</span>
                    <div
                      v-if="formLinkLoading"
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
                    ref="formLinkAlert"
                  >
                    <FontAwesomeIcon icon="fa-circle-exclamation" />
                    <span class="mx-2">
                      {{ formLinkAlertMessage }}
                    </span>
                    <button
                      type="button"
                      class="btn-close ms-auto"
                      aria-label="Close"
                      @click="onFormLinkAlertClose"
                    ></button>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <div>
            Don&apos;t have a stocknews account?
            <RouterLink to="/register">
              <span>Get one now.</span>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
