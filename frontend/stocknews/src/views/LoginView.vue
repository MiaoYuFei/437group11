<script lang="ts">
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import BsAlert from "@/components/BsAlert.vue";
import BsButton from "@/components/BsButton.vue";
import { disableForm, enableForm, focusForm, handleApi } from "@/utilities";

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
      handleApi(this.$refs.form, ["username", "password"]).then(
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
    onFormAlertClosed: function () {
      focusForm(this.$refs.form);
    },
  },
  mounted() {
    focusForm(this.$refs.form);
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
      class="container d-flex flex-column justify-content-center align-items-center h-100"
    >
      <div
        class="card col-12 col-md-10 col-lg-8 col-xl-6 col-xxl-4"
        style="box-shadow: 0.2rem 0.2rem 0.1rem #eee"
      >
        <div class="card-body p-4">
          <form
            action="/api/login"
            method="post"
            @submit.prevent="onFormSubmit"
            ref="form"
          >
            <h3 class="card-title mb-4">
              <FontAwesomeIcon icon="fa-user" class="me-3" />Log In
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
            <div class="mb-3">
              <BsButton
                type="submit"
                class="btn-lg btn-block me-3"
                :loading="loading"
                bgColor="dark"
                textColor="light"
                ref="formSubmit"
              >
                Log In
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
              <a href="#">Forgot password?</a>
            </div>
            <div>
              Don&apos;t have an account?
              <RouterLink to="/register">
                <span>Register here.</span>
              </RouterLink>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
