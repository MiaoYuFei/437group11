<script lang="ts">
import { RouterLink } from "vue-router";
import { getFormData, handleApi } from "@/utilities";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

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
      const q = getFormData(this.$refs.searchForm as HTMLFormElement, ["q"])[
        "q"
      ];
      if (q === "") {
        return false;
      }
      this.searchText = q;
      window.open("/search?q=" + encodeURIComponent(this.searchText), "_blank");
    },
  },
  watch: {
    $route(to: any, from: any) {
      if (to?.path === "/search") {
        this.searchText = to.query.q as string;
      }
      if (to?.path !== from?.path) {
        this.onUserStatus();
      }
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
        :class="{ 'd-none': !($route.path === '/myaccount') }"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvas"
        aria-controls="offcanvas"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <FontAwesomeIcon icon="fa-table-list" />
      </button>
      <RouterLink class="navbar-brand d-flex align-items-center gap-1" to="/">
        <img
          src="/src/assets/icon/logo.svg"
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
        <FontAwesomeIcon icon="fa-bars" />
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/">
              <span>Home</span>
            </RouterLink>
          </li>
          <li v-if="signedIn" class="nav-item">
            <RouterLink class="nav-link" to="/myreadinglist">
              <span>My Reading List</span>
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
                <RouterLink class="dropdown-item" to="/category?q=agriculture">
                  <span>Agriculture</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/category?q=mining">
                  <span>Mining</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/category?q=construction">
                  <span>Construction</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  class="dropdown-item"
                  to="/category?q=manufacturing"
                >
                  <span>Manufacturing</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  class="dropdown-item"
                  to="/category?q=transportation"
                >
                  <span>Transportation</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/category?q=wholesale">
                  <span>Wholesale Trade</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/category?q=retail">
                  <span>Retail Trade</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/category?q=finance">
                  <span>Finance, Insurance, Real, Estate</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/category?q=services">
                  <span>Services</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  class="dropdown-item"
                  to="/category?q=public_administration"
                >
                  <span>Public Administration</span>
                </RouterLink>
              </li>
            </ul>
          </li>
        </ul>
        <form
          class="d-flex me-2"
          role="search"
          @submit.prevent="search_click"
          ref="searchForm"
        >
          <input
            class="form-control me-2"
            type="search"
            name="q"
            placeholder="Search"
            aria-label="Search"
            required
            :value="searchText"
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

.nav-link.router-link-active {
  color: #fff;
}
</style>
