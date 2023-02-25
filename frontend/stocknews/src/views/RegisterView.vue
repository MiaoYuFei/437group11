<script lang="ts">
import $ from "jquery";
import BsAlert from "@/components/BsAlert.vue";
import BsButton from "@/components/BsButton.vue";
import axios from "axios";

export default {
  data() {
    return {
      registerAlertMessage: "unknown error",
    };
  },
  methods: {
    onRegister: function (event: Event) {
      if (event.target != null) {
        const jqObj = $(event.target as Element);
        const apiData = {
          username: jqObj.find("input[name='username']").val(),
          password: jqObj.find("input[name='password']").val(),
          email: jqObj.find("input[name='email']").val(),
        };
        console.log(apiData);
      }
    },
    onRegisterAlertClosed: function (target: Element) {
      $(target)
        .parentsUntil("form")
        .parent()
        .find("input:first")
        .trigger("focus");
    },
  },
  mounted() {
    $(this.$refs.root as Element)
      .find("form:first")
      .find("input:first")
      .trigger("focus");
  },
  components: {
    BsAlert,
    BsButton,
  },
};
</script>
<template>
  <div ref="root">
    <div
      class="container d-flex flex-column justify-content-center align-items-center h-100"
    >
      <div
        class="card col-12 col-md-10 col-lg-8 col-xl-6 col-xxl-4"
        style="box-shadow: 0.2rem 0.2rem 0.1rem #eee"
      >
        <div class="card-body p-4">
          <form
            action="/api/register"
            method="post"
            @submit.prevent="onRegister"
          >
            <h3 class="card-title mb-3">Register</h3>
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
              <BsButton
                type="submit"
                class="btn-lg btn-block me-3"
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
                :message="registerAlertMessage"
                bgColor="warning"
                @closed="onRegisterAlertClosed"
                ref="registerAlert"
              ></BsAlert>
            </div>
            <div>
              Already have an account?
              <RouterLink to="/login">
                <span>Log in here.</span>
              </RouterLink>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
