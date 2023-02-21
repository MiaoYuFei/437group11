<script setup lang="ts">
import { RouterView } from "vue-router";
import BsNavbarVue from "@/components/BsNavbar.vue";
</script>

<template>
  <BsNavbarVue />
  <div class="d-flex flex-row flex-fill" style="min-height: 0">
    <RouterView
      class="flex-fill"
      style="min-height: 0; padding: 1rem; overflow: auto"
    />
  </div>
</template>

<style scoped></style>
