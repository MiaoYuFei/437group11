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
  <div
    class="alert align-items-center mb-0"
    role="alert"
    aria-hidden="true"
    ref="root"
  >
    <svg
      style="height: 1em; width: auto"
      xmlns="http://www.w3.org/2000/svg"
      class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2"
      viewBox="0 0 16 16"
      role="img"
      aria-label="Warning:"
    >
      <path
        d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"
      />
    </svg>

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
