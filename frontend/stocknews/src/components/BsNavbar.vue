<script lang="ts">
import { RouterLink } from "vue-router";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

export default {
  data: () => {
    return {
      searchText: "",
    };
  },
  methods: {
    search_click: function () {
      if (this.searchText === "") {
        return false;
      }
      window.open("/search?q=" + encodeURIComponent(this.searchText), "_blank");
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
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Category 1
            </a>
            <ul class="dropdown-menu dropdown-menu-dark">
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Type 1</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Type 2</span>
                </RouterLink>
              </li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Category 1
            </a>
            <ul class="dropdown-menu dropdown-menu-dark">
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Type 1</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/">
                  <span>Type 2</span>
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
        <ul class="navbar-nav mb-2 mb-lg-0">
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
      </div>
    </div>
  </nav>
</template>
<style scoped></style>
