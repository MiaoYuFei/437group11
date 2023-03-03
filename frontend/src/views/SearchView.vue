<script lang="ts">
export default {
  data() {
    return {};
  },
  created() {
    document.title = "Search - " + (this as any).$projectName;
  },
  mounted() {},
};
</script>
<template>
  <div>Search results:</div>
</template>
<style scoped></style>
