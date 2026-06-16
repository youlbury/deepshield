<template>
  <div>
    <router-view v-if="!authState.isLoggedIn" />
    <Layout v-else />
    <ToastNotification ref="toastRef" />
  </div>
</template>

<script>
import Layout from './layout/index.vue'
import ToastNotification from './components/ToastNotification.vue'
import { authState } from './store/auth'

export default {
  name: 'App',
  components: {
    Layout,
    ToastNotification
  },
  setup() {
    return { authState }
  },
  mounted() {
    // 全局挂载 toast 方法
    window.$toast = this.$refs.toastRef
  }
}
</script>

<style>
/* 全局样式（非 scoped）*/
body {
  margin: 0;
  padding: 0;
  /* 允许 body 滚动，由 el-scrollbar 内部管理 */
  background: linear-gradient(135deg, #0a0e1a 0%, #1a1f3a 50%, #111827 100%);
}

#app {
  height: 100vh;
  /* 移除 overflow: hidden，让 el-scrollbar 正常工作 */
}
</style>