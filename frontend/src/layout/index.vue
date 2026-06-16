<template>
  <div class="app-wrapper" :class="classes">
    <!-- 移动端遮罩 -->
    <div
      v-show="device === 'mobile' && sidebar.opened"
      class="app-mask"
      @click="toggleSideBar"
    />
    
    <!-- 侧边栏 -->
    <NavVertical v-show="!hiddenSideBar" />
    
    <!-- 主容器 -->
    <div :class="['main-container', hiddenSideBar ? 'main-hidden' : '']">
      <!-- 顶部导航 -->
      <LayNavbar v-if="!hiddenSideBar" />
      
      <!-- 主体内容 -->
      <el-scrollbar>
        <el-backtop target=".main-container .el-scrollbar__wrap" title="回到顶部">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M12 8l-6 6h12z"/>
          </svg>
        </el-backtop>
        <LayContent />
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import NavVertical from './components/lay-sidebar/NavVertical.vue'
import LayNavbar from './components/lay-navbar/LayNavbar.vue'
import LayContent from './components/lay-content/LayContent.vue'

const route = useRoute()
const sidebar = ref({
  opened: true,
  withoutAnimation: false
})
const device = ref('desktop')
const hiddenSideBar = ref(false)
const sidebarWidth = ref(220)  // 跟踪侧边栏宽度

const classes = computed(() => ({
  hideSidebar: !sidebar.value.opened,
  openSidebar: sidebar.value.opened,
  withoutAnimation: sidebar.value.withoutAnimation,
  mobile: device.value === 'mobile'
}))

const toggleSideBar = () => {
  sidebar.value.opened = !sidebar.value.opened
  sidebar.value.withoutAnimation = false
}

// 响应式处理
const handleResize = () => {
  if (window.innerWidth <= 768) {
    device.value = 'mobile'
    sidebar.value.opened = false
  } else {
    device.value = 'desktop'
    sidebar.value.opened = true
  }
}

// 监听侧边栏宽度变化
const updateSidebarWidth = () => {
  const savedWidth = localStorage.getItem('sidebarWidth')
  if (savedWidth !== null) {
    const width = parseInt(savedWidth)
    if (width >= 180 && width <= 400) {
      sidebarWidth.value = width
    }
  }
}

onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
  
  // 初始读取侧边栏宽度
  updateSidebarWidth()
  
  // 监听localStorage变化（当其他组件修改时）
  window.addEventListener('storage', updateSidebarWidth)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('storage', updateSidebarWidth)
})
</script>

<style scoped>
.app-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.app-wrapper::after {
  clear: both;
  display: table;
  content: "";
}

.app-wrapper.mobile.openSidebar {
  position: fixed;
  top: 0;
}

.app-mask {
  position: absolute;
  top: 0;
  z-index: 2001;
  width: 100%;
  height: 100%;
  background: #000;
  opacity: 0.3;
}

.main-container {
  height: 100%;
  transition: margin-left 0.28s;
  margin-left: v-bind(sidebarWidth + 'px');  /* 动态绑定侧边栏宽度 */
  padding-right: 1rem; /* 右侧留出约一厘米空间 */
  position: relative;
  background: transparent;
}

.main-hidden {
  margin-left: 0px;
}

.hideSidebar .main-container {
  margin-left: 64px;
}

.mobile .main-container {
  margin-left: 0px;
}
</style>