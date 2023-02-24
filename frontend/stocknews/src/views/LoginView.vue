<script lang="ts">
import $ from "jquery";
import BsAlert from "@/components/BsAlert.vue";
import BsButton from "@/components/BsButton.vue";
import axios from "axios";

export default {
  data() {
    return {
      loginAlertMessage: "unknown error",
    };
  },
  methods: {
    onLogin: function (event: Event) {
      const alertElement = this.$refs.loginAlert as typeof BsAlert;
      const loginButtonElement = this.$refs.loginButton as typeof BsButton;
      const form = $(event.target as Element);
      const formControls = form.find("input, button");
      const action = form.attr("action");
      if (action === undefined) {
        return false;
      }
      const method = form.attr("method")?.toLowerCase() || "get";
      if (method != "get" && method != "post") {
        return false;
      }
      alertElement.hide();
      formControls.addClass("disabled").attr("disabled", "disabled");
      loginButtonElement.setLoading(true);
      const api = method === "get" ? axios.get(action) : axios.post(action);
      api
        .then((response) => {
          const code = response.data.code;
          const data = response.data.data;
          formControls.removeClass("disabled").removeAttr("disabled");
          loginButtonElement.setLoading(false);
          if (parseInt(code) === 200) {
            window.location.href = "/";
          } else {
            this.loginAlertMessage =
              "(" + code.toString() + ") " + data.message;
            alertElement.show();
          }
        })
        .catch((error) => {
          console.log(error);
          this.loginAlertMessage = "(" + error.code + ") " + error.message;
          alertElement.show(() => {
            formControls.removeClass("disabled").removeAttr("disabled");
            loginButtonElement.setLoading(false);
          });
        });
    },
    onLoginAlertClosed: function (target: Element) {
      $((target as any).$el)
        .parentsUntil("form")
        .parent()
        .find("input:first")
        .trigger("focus");
    },
  },
  mounted() {},
  components: {
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
          <form action="/api/login" method="post" @submit.prevent="onLogin">
            <h3 class="card-title user-select-none mb-3">Log In</h3>
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
                bgColor="dark"
                textColor="light"
                ref="loginButton"
              >
                Log In
              </BsButton>
            </div>
            <div>
              <BsAlert
                class="mb-3"
                :message="loginAlertMessage"
                bgColor="warning"
                @closed="onLoginAlertClosed"
                ref="loginAlert"
              ></BsAlert>
            </div>
            <div>
              <a class="text-decoration-none user-select-none" href="#"
                >Forget password?</a
              >
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
