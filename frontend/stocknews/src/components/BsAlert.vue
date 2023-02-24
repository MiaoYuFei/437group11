<script lang="ts">
import $ from "jquery";

let domObj: Element | null = null;

export default {
  props: {
    message: String,
    bgColor: { type: String, default: "primary" },
  },
  methods: {
    show: function (callback: Function | undefined = undefined) {
      this.$emit("show", this);
      if (domObj != null) {
        const jqObj = $(domObj);
        jqObj
          .css("display", "flex")
          .hide()
          .fadeIn(() => {
            jqObj.addClass("show").removeAttr("aria-hidden");
            if (callback != undefined) {
              callback();
            }
            this.$emit("shown", this);
          });
      }
    },
    hide: function (callback: Function | undefined = undefined) {
      this.$emit("close", this);
      if (domObj != null) {
        const jqObj = $(domObj);
        jqObj.fadeOut(() => {
          jqObj.removeClass("show").attr("aria-hidden", "true").hide();
          if (callback != undefined) {
            callback();
          }
          this.$emit("closed", this);
        });
      }
    },
  },
  mounted: function () {
    domObj = this.$refs.root as Element;
    $(this.$refs.root as Element).hide();
    const eventHandler = (event: Event) => {
      this.$emit(event.type.substring(0, event.type.indexOf(".")), this);
    };
    domObj.addEventListener("close.bs.alert", eventHandler);
    domObj.addEventListener("closed.bs.alert", eventHandler);
    const jqObj = $(domObj);
    jqObj.addClass("alert-" + this.bgColor);
  },
  expose: ["show", "hide"],
};
</script>
<template>
  <div class="alert mb-0" role="alert" aria-hidden="true" ref="root">
    <span class="me-2">
      {{ message }}
    </span>
    <button
      type="button"
      class="btn-close ms-auto"
      aria-label="Close"
      @click="hide()"
    ></button>
  </div>
</template>
