<script setup lang="ts">
import { RouterView } from "vue-router";
import BsNavbar from "@/components/BsNavbar.vue";
</script>

<template>
  <BsNavbar />
  <div class="d-flex flex-row flex-fill" style="min-height: 0">
    <RouterView class="flex-fill" style="min-height: 0" />
  </div>
  <div style="border-top: 1px solid var(--bs-border-color)">
    <div class="p-1" style="font-size: 0.8em">
      <span class="text-muted mx-3">Copyright CSE437S group 11</span>
    </div>
  </div>
</template>
