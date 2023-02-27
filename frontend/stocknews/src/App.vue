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
  <div style="border-top: 1px solid var(--bs-border-color)">
    <div class="p-1" style="font-size: 0.8em">
      <span class="text-muted">Copyright CSE437S group 11</span>
    </div>
  </div>
</template>

<style scoped></style>
