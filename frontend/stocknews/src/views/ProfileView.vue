import { UserOutlined, VideoCameraOutlined, UploadOutlined } from '@ant-design/icons-vue';
import { defineComponent, ref } from 'vue';

<script setup lang="ts"></script>
<script lang="ts">
export default {
  data() {
    return {};
  },
  mounted() {},
};
</script>
<template>
  <a-layout>
    <a-layout-sider
      breakpoint="lg"
      collapsed-width="0"
      @collapse="onCollapse"
      @breakpoint="onBreakpoint"
    >
      <div class="logo" />
      <a-menu  theme="dark" mode="inline">
        <a-menu-item key="My Data">
          <video-camera-outlined />
          <span class="nav-text">My Data</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header :style="{ background: '#fff', padding: 0 }" />
      <a-layout-content style="text-align: center">
        <div :style="{ padding: '10px', background: '#fff', minHeight: '360px' }">User Information</div>
      </a-layout-content>
      <a-layout-footer style="text-align: center">
        Created by Group 11 for 437
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script>


</script>
<style>
#components-layout-demo-top-side .logo {
  float: left;
  width: 120px;
  height: 60px;
  margin: 16px 24px 16px 0;
  background: rgba(255, 255, 255, 0.3);
}

.ant-row-rtl #components-layout-demo-top-side .logo {
  float: right;
  margin: 16px 0 16px 24px;
}

.site-layout-background {
  background: #fff;
}
</style>
