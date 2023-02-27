<script setup lang="ts"></script>
<script lang="ts">
export default {
  data() {
    return {};
  },
  created() {
    document.title = "Profile - " + (this as any).$projectName;
  },
  mounted() {},
};
</script>
<template>
  <div>Profile page for stock news</div>
</template>
<style scoped></style>
