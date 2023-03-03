<script lang="ts">
import $ from "jquery";

let domObj: Element | null = null;

export default {
  props: {
    loading: { type: Boolean, default: false },
    bgColor: { type: String, default: "dark" },
    textColor: { type: String, default: "light" },
  },
  mounted: function () {
    domObj = this.$refs.root as Element;
    const jqObj = $(domObj);
    jqObj.addClass("btn-" + this.bgColor);
    jqObj.find(".spinner-border").addClass("text-" + this.textColor);
  },
};
</script>
<template>
  <button
    class="btn d-flex align-items-center"
    @click="$emit('click', $event)"
    ref="root"
  >
    <span v-if="!loading">
      <slot></slot>
    </span>
    <div v-if="loading" class="spinner-border" role="status" ref="spinner">
      <span class="visually-hidden">Loading...</span>
    </div>
  </button>
</template>
