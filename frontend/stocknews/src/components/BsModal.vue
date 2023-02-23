<script setup lang="ts">
import { Modal } from "bootstrap";
</script>
<script lang="ts">
let domObj: Element | null = null;
let bsObj: Modal | null = null;

export default {
  props: {
    title: String,
    options: Object as () => Modal.Options,
  },
  data: () => {
    return {};
  },
  methods: {
    show: () => {
      bsObj?.show();
    },
    hide: () => {
      bsObj?.hide();
    },
  },
  mounted: function () {
    domObj = this.$refs.modalContainer as Element;
    bsObj = new Modal(domObj, this.options);
    const modalEventHandler = (event: Modal.Event) => {
      this.$emit(event.type.substring(0, event.type.indexOf(".")));
    };
    domObj.addEventListener("hide.bs.modal", modalEventHandler);
    domObj.addEventListener("hidden.bs.modal", modalEventHandler);
    domObj.addEventListener("hidePrevented.bs.modal", modalEventHandler);
    domObj.addEventListener("show.bs.modal", modalEventHandler);
    domObj.addEventListener("shown.bs.modal", modalEventHandler);
    new ResizeObserver(() => bsObj?.handleUpdate()).observe(
      this.$refs.modalBody as Element
    );
  },
  expose: ["show", "hide"],
};
</script>
<template>
  <div
    class="modal fade"
    tabindex="-1"
    aria-hidden="true"
    :aria-label="title"
    ref="modalContainer"
  >
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <font-awesome-icon icon="fa-circle-exclamation" class="fs-5" />
            {{ title }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <slot ref="modalBody"></slot>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="$emit('confirm')"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
