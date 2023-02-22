<script setup lang="ts"></script>
<script lang="ts">
export default {
  data() {
    return {};
  },
  mounted() {},
};
</script>
<template>
  <div>Log in page for stock news
    <form action="http://localhost:9001/api/login" method="post">
            <h3>Sign In</h3>

            <div>
                <label>user name</label>
                <input name="username" type="text">
            </div>
            <div>
                <label>Password</label>
                <input name="password" type="password">
            </div>
            <button type="submit" class="btn btn-dark btn-lg btn-block">Sign In</button>

    </form>  
  </div>
  
</template>
<style scoped></style>
