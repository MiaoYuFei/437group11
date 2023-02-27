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
  <div>Ticker information:</div>
</template>
<style scoped></style>
