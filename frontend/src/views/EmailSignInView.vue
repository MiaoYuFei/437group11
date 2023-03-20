<script lang="ts">
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { handleApi } from "@/utilities";

export default {
  data() {
    return {
      errorMessage: "unknown errror",
    };
  },
  methods: {},
  created() {
    document.title = "Sign in with email - " + (this as any).$projectName;
  },
  mounted() {
    this.errorMessage = "Loading...";
    if (
      this.$route.query.oobCode === undefined ||
      this.$route.query.email === undefined
    ) {
      this.errorMessage = "Invalid request.";
      return;
    }
    const apiData = {
      requestType: "email_link",
      email: this.$route.query.email,
      oobCode: this.$route.query.oobCode,
    };
    handleApi("post", "/api/user/signin", apiData).then(
      (response) => {
        if (parseInt(response.data.code) === 200) {
          this.errorMessage = "Sign in successful! Redirecting...";
          this.$router.replace("/myreadinglist");
        } else {
          this.errorMessage = response.data.data.reason;
        }
      },
      (error) => {
        this.errorMessage = error.message;
      }
    );
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
          <p>{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped></style>
