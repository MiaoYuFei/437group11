<script lang="ts">
import { RouterLink } from "vue-router";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { handleApi } from "@/utilities";

export default {
  data: () => {
    return {
      useremail: "",
      username: "",
      signedIn: false,
      emailVerified: false,
      searchText: "",
    };
  },
  methods: {
    onUserStatus: function () {
      handleApi("post", "/api/user/status", []).then(
        (response) => {
          const code = parseInt(response.data.code);
          const data = response.data.data;
          if (code === 200) {
            this.useremail = data.email;
            this.username = data.name;
            this.signedIn = true;
            this.emailVerified =
              (response.data.data.emailVerified as string).toLowerCase() ===
              "true"
                ? true
                : false;
          } else {
            this.signedIn = false;
            this.emailVerified = false;
          }
        },
        () => {
          this.signedIn = false;
          this.emailVerified = false;
        }
      );
    },
    onUserSignout: function () {
      handleApi("post", "/api/user/signout", []).then(() => {
        this.useremail = "";
        this.signedIn = false;
        this.$router.push("/");
      });
    },
    search_click: function () {
      if (this.searchText === "") {
        return false;
      }
      window.open("/search?q=" + encodeURIComponent(this.searchText), "_blank");
    },
  },
  mounted() {
    this.onUserStatus();
  },
  watch: {
    $route() {
      this.onUserStatus();
    },
  },
  components: { RouterLink, FontAwesomeIcon },
};
</script>
<template>
  <nav
    class="navbar navbar-expand-lg navbar-dark bg-dark"
    aria-label="Navigation"
  >
    <div class="container-fluid">
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvas"
        aria-controls="offcanvas"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <RouterLink class="navbar-brand d-flex align-items-center gap-1" to="/">
        <img
          src="/src/assets/vue.svg"
          alt="Logo"
          width="30"
          height="24"
          class="d-inline-block align-text-top"
        />
        Stock News
      </RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/">
              <span>Home</span>
            </RouterLink>
          </li>
          <li v-if="signedIn" class="nav-item">
            <RouterLink class="nav-link" to="/myfeeds">
              <span>My Feeds</span>
            </RouterLink>
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Industries
            </a>
            <ul class="dropdown-menu dropdown-menu-dark" style="margin: 0">
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Agriculture</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Mining</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Construction</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Manufacturing</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Transportation</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Wholesale Trade</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Retail Trade</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Finance, Insurance, Real, Estate</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Services</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Public Administration</span>
                </RouterLink>
              </li>
            </ul>
          </li>
        </ul>
        <form class="d-flex me-2" role="search" @submit.prevent="search_click">
          <input
            class="form-control me-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
            required
            v-model="searchText"
          />
          <button class="btn btn-outline-success" type="submit">
            <FontAwesomeIcon icon="fa-magnifying-glass" class="fs-5" />
          </button>
        </form>
        <div>
          <ul v-if="!signedIn" class="navbar-nav mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/signin">
                <span>Sign in</span>
              </RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/register">
                <span>Register</span>
              </RouterLink>
            </li>
          </ul>
          <ul v-if="signedIn" class="navbar-nav mb-2 mb-lg-0">
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                {{ username }}
              </a>
              <ul
                class="dropdown-menu dropdown-menu-end dropdown-menu-dark m-0"
              >
                <li>
                  <RouterLink class="dropdown-item" to="/myaccount">
                    <span>My Account</span>
                  </RouterLink>
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li>
                  <button class="dropdown-item" @click="onUserSignout">
                    Sign out
                  </button>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>
<style scoped>
.dropdown-menu-dark .dropdown-divider {
  border-top: 1px solid rgba(var(--bs-secondary-rgb), 0.675);
}
</style>
