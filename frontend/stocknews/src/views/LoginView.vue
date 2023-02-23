<script setup lang="ts"></script>
<script lang="ts">
export default {
  data() {
    return {};
  },
  methods: {},
  mounted() {},
  components: {},
};
</script>
<template>
  <div>
    <div
      class="container d-flex flex-column justify-content-center align-items-center h-100"
    >
      <div class="card col-12 col-md-10 col-lg-8 col-xl-6 col-xxl-4">
        <div class="card-body">
          <form action="http://localhost:9001/api/login" method="post">
            <h3 class="card-title">Log In</h3>
            <div class="form-floating mb-3">
              <input
                type="text"
                class="form-control"
                id="inputUsername"
                name="username"
                placeholder="Username"
              />
              <label for="inputUsername">Username</label>
            </div>
            <div class="form-floating mb-3">
              <input
                type="password"
                class="form-control"
                id="inputPassword"
                name="password"
                placeholder="Password"
              />
              <label for="inputPassword">Password</label>
            </div>
            <div>
              <button type="submit" class="btn btn-dark btn-lg btn-block">
                Log In
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped></style>
