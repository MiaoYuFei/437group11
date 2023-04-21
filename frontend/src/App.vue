<script lang="ts">
import { RouterView } from "vue-router";
import BsNavbar from "@/components/BsNavbar.vue";
import { handleApi } from "./utilities";
export default {
  data: () => ({
    userStatus: {
      signedIn: false,
      id: "",
      email: "",
      emailVerified: false,
      name: "",
    },
  }),
  methods: {
    onUserStatus(callback: Function | undefined = undefined) {
      handleApi("post", "/api/user/status", []).then(
        (response) => {
          const code = parseInt(response.data.code);
          const data = response.data.data;
          if (code === 200) {
            this.userStatus.signedIn = true;
            this.userStatus.id = data.id;
            this.userStatus.email = data.email;
            this.userStatus.name = data.name;
            this.userStatus.emailVerified =
              (response.data.data.emailVerified as string).toLowerCase() ===
              "true"
                ? true
                : false;
          } else {
            this.userStatus.signedIn = false;
            this.userStatus.id = "";
            this.userStatus.email = "";
            this.userStatus.name = "";
            this.userStatus.emailVerified = false;
          }
          if (callback) {
            callback();
          }
        },
        () => {
          this.userStatus.signedIn = false;
          this.userStatus.id = "";
          this.userStatus.email = "";
          this.userStatus.name = "";
          this.userStatus.emailVerified = false;
          if (callback) {
            callback();
          }
        }
      );
    },
  },
  mounted() {
    this.onUserStatus();
  },
  watch: {
    $route(to: any, from: any) {
      if (to?.path !== from?.path) {
        this.onUserStatus(() => {
          const protectedPages = ["/myreadinglist", "/myaccount"];
          if (protectedPages.includes(to?.path)) {
            if (!this.userStatus.signedIn) {
              this.$router.push("/signin");
            } else {
              if (!this.userStatus.emailVerified) {
                this.$router.push("/verifyemail");
              }
            }
          }
        });
      }
    },
  },
  components: {
    BsNavbar,
    RouterView,
  },
};
</script>

<template>
  <BsNavbar :userStatus="userStatus" />
  <div class="d-flex flex-fill" style="min-height: 0">
    <RouterView
      class="flex-fill"
      style="min-height: 0"
      :userStatus="userStatus"
    />
  </div>
  <div style="border-top: 1px solid var(--bs-border-color)">
    <div class="p-1" style="font-size: 0.8em">
      <span class="text-muted mx-3"
        >Copyright CSE437S group 11. API sponsored by
        <a href="https://polygon.io/" target="_blank">polygon.io</a>.</span
      >
    </div>
  </div>
</template>
