<script lang="ts">
import { handleApi } from "@/utilities";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

export default {
  data() {
    return {
      email: "",
      signedIn: false,
      emailVerified: false,
    };
  },
  methods: {
    onUserStatus: function () {
      handleApi("post", "/api/user/status", []).then(
        (response) => {
          if (parseInt(response.data.code) === 200) {
            console.log(this.email);
            this.email = response.data.data.email;
            this.signedIn = true;
            this.emailVerified =
              (response.data.data.emailVerified as string).toLowerCase() ===
              "true"
                ? true
                : false;
            if (!this.emailVerified) {
              this.$router.push("/verifyemail");
            }
          } else {
            this.signedIn = false;
            this.emailVerified = false;
            this.$router.push("/signin");
          }
        },
        () => {
          this.signedIn = false;
          this.emailVerified = false;
          this.$router.push("/signin");
        }
      );
    },
  },
  created() {
    document.title = "Profile - " + (this as any).$projectName;
  },
  mounted() {
    this.onUserStatus();
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
          <form ref="form">
            <h3 class="card-title mb-4">
              <FontAwesomeIcon icon="fa-user" class="me-3" />Profile
            </h3>
            <div class="input-group mb-3">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control-plaintext"
                  id="inputEmail"
                  name="email"
                  placeholder="Email"
                  :value="email"
                  readonly
                />
                <label for="inputEmail">Email</label>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
