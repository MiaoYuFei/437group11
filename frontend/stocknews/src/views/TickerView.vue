<script lang="ts">
export default {
  data() {
    return {};
  },
  created() {
    document.title = "Ticker - " + (this as any).$projectName;
  },
  mounted() {},
};
</script>
<template>
  <div>Ticker information for {{ $route.query.q }}:</div>
</template>
<style scoped></style>
