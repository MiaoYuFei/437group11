<script lang="ts">
export default {
  props: {
    loading: Boolean,
    message: String,
  },
};
</script>
<template>
  <div
    class="flex-fill justify-content-center align-items-center h-100"
    :class="{ 'd-flex': loading, 'd-none': !loading }"
  >
    <div
      class="spinner-border text-primary me-2"
      role="status"
      style="width: 3em; height: 3em"
    ></div>
    {{ message }}
  </div>
</template>
