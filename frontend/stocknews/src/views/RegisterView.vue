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
  <div>Register page for stock news
    <form action="http://localhost:9001/api/register" method="post">
            <h3>Sign Up</h3>

            <div>
                <label>User Name</label>
                <input name="username" type="text">
            </div>
            <div>
                <label>Password</label>
                <input name="password" type="password">
            </div>
             <div>
                <label>Email</label>
                <input name="email" type="email">
            </div>           
            <button type="submit" class="btn btn-dark btn-lg btn-block">Sign Up</button>

    </form>  
  </div>
  
</template>
<style scoped></style>
