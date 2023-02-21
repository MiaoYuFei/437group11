<script setup lang="ts">
import axios from "axios";
</script>
<script lang="ts">
export default {
  data() {
    return {};
  },
  mounted() {
    axios
      .get("http://localhost:9000/test")
      .then((response: { data: any }) => {
        console.log(response.data);
      })
      .catch((reason) => {
        console.log(reason);
      });
  },
};
</script>
<template>
  <div>Home page for stock news</div>
</template>
<style scoped></style>
