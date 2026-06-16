<template>
  <div class="sidebar-container" :class="{ 'is-collapsed': isCollapse }" :style="{ width: sidebarWidth + 'px' }">
    <!-- Logo -->
    <div class="sidebar-header">
      <!-- 使用登录界面的发光盾牌 SVG -->
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="logo-icon">
        <path d="M12 2L3 7V12C3 17.55 6.84 22.74 12 24C17.16 22.74 21 17.55 21 12V7L12 2Z" stroke="url(#logo-gradient)" stroke-width="2"/>
        <path d="M9 12L11 14L15 10" stroke="url(#logo-gradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <defs>
          <linearGradient id="logo-gradient" x1="3" y1="2" x2="21" y2="24" gradientUnits="userSpaceOnUse">
            <stop stop-color="#00D4FF"/>
            <stop offset="1" stop-color="#00FF88"/>
          </linearGradient>
        </defs>
      </svg>
      <transition name="fade-text">
        <div v-if="!isCollapse" class="logo-text">
          <h1 class="logo">DeepShield</h1>
          <span class="version">v2.0</span>
        </div>
      </transition>
    </div>

    <!-- 菜单 -->
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        router
        :default-active="activeMenu"
        :collapse="isCollapse"
        background-color="#111827"
        text-color="#94a3b8"
        active-text-color="#00d4ff"
        :unique-opened="true"
        :collapse-transition="false"
      >
        <!-- 概览 -->
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <template #title>首页概览</template>
        </el-menu-item>

        <!-- 检测模块 -->
        <el-sub-menu index="detect">
          <template #title>
            <el-icon><Monitor /></el-icon>
            <span>检测模块</span>
          </template>
          <el-menu-item index="/image">
            <el-icon><Picture /></el-icon>
            <template #title>图片检测</template>
          </el-menu-item>
          <el-menu-item index="/video">
            <el-icon><VideoCamera /></el-icon>
            <template #title>视频检测</template>
          </el-menu-item>
          <el-menu-item index="/audio">
            <el-icon><Headset /></el-icon>
            <template #title>音频检测</template>
          </el-menu-item>
          <el-menu-item index="/forensics">
            <el-icon><Search /></el-icon>
            <template #title>数字取证</template>
          </el-menu-item>
          <el-menu-item index="/verify">
            <el-icon><CircleCheckFilled /></el-icon>
            <template #title>证据验真</template>
          </el-menu-item>
        </el-sub-menu>

        <!-- 实验模块 -->
        <el-sub-menu index="experiment">
          <template #title>
            <el-icon><Grid /></el-icon>
            <span>实验模块</span>
          </template>
          <el-menu-item index="/models">
            <el-icon><Cpu /></el-icon>
            <template #title>模型实验</template>
          </el-menu-item>
          <el-menu-item index="/benchmark">
            <el-icon><TrendCharts /></el-icon>
            <template #title>性能评估</template>
          </el-menu-item>
        </el-sub-menu>

        <!-- 系统 -->
        <el-menu-item index="/about">
          <el-icon><InfoFilled /></el-icon>
          <template #title>关于系统</template>
        </el-menu-item>
      </el-menu>
    </el-scrollbar>

    <!-- 底部状态 -->
    <div class="sidebar-footer">
      <el-tag type="success" size="small" effect="dark" class="status-tag">
        <el-icon class="status-dot"><CircleCheckFilled /></el-icon>
        <span v-if="!isCollapse">系统在线</span>
      </el-tag>
    </div>

    <!-- 折叠按钮 -->
    <div class="sidebar-collapse" @click="toggleCollapse">
      <el-icon>
        <component :is="isCollapse ? 'Expand' : 'Fold'" />
      </el-icon>
    </div>

    <!-- 可拖动调整器 -->
    <div 
      v-if="!isCollapse"
      class="sidebar-resizer"
      @mousedown="startResize"
    >
      <div class="resizer-line"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  HomeFilled,
  Monitor,
  Picture,
  VideoCamera,
  Headset,
  Search,
  Grid,
  Cpu,
  TrendCharts,
  InfoFilled,
  CircleCheckFilled,
  Expand,
  Fold
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const isCollapse = ref(false)
const sidebarWidth = ref(220)  // 侧边栏宽度，默认220px
const minWidth = 180           // 最小宽度
const maxWidth = 400           // 最大宽度
let isResizing = false         // 是否正在调整大小

onMounted(() => {
  // 从 localStorage 读取折叠状态
  const savedState = localStorage.getItem('sidebarCollapse')
  if (savedState !== null) {
    isCollapse.value = savedState === 'true'
  }
  
  // 从 localStorage 读取侧边栏宽度
  const savedWidth = localStorage.getItem('sidebarWidth')
  if (savedWidth !== null) {
    const width = parseInt(savedWidth)
    if (width >= minWidth && width <= maxWidth) {
      sidebarWidth.value = width
    }
  }
})

const activeMenu = computed(() => route.path)

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
  localStorage.setItem('sidebarCollapse', isCollapse.value)
  window.dispatchEvent(new Event('resize'))
}

// 开始调整大小
const startResize = (e) => {
  e.preventDefault()
  isResizing = true
  
  // 记录初始位置
  const startX = e.clientX
  const startWidth = sidebarWidth.value
  
  // 鼠标移动事件
  const onMouseMove = (moveEvent) => {
    if (!isResizing) return
    
    // 计算新的宽度
    const deltaX = moveEvent.clientX - startX
    let newWidth = startWidth + deltaX
    
    // 限制在最小和最大宽度之间
    newWidth = Math.max(minWidth, Math.min(maxWidth, newWidth))
    
    // 更新宽度
    sidebarWidth.value = newWidth
  }
  
  // 鼠标释放事件
  const onMouseUp = () => {
    isResizing = false
    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)
    
    // 保存宽度到 localStorage
    localStorage.setItem('sidebarWidth', sidebarWidth.value)
    
    // 触发窗口重绘
    window.dispatchEvent(new Event('resize'))
  }
  
  // 监听鼠标移动和释放
  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
}
</script>

<style scoped>
.sidebar-container {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 220px;  /* 默认宽度，会被动态样式覆盖 */
  background: #111827;
  border-right: 1px solid rgba(148, 163, 184, 0.2);
  transition: none;  /* 移除过渡动画，让拖动更流畅 */
  display: flex;
  flex-direction: column;
  z-index: 1001;
}

.sidebar-container.is-collapsed {
  width: 64px;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid rgba(0, 212, 255, 0.15);
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 64px;
  background: linear-gradient(90deg, rgba(0, 212, 255, 0.08), transparent);
}

.logo-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  filter: drop-shadow(0 0 8px rgba(0, 212, 255, 0.5));
}

.logo-text {
  display: flex;
  flex-direction: column;
  white-space: nowrap;
}

.logo {
  font-size: 16px;
  font-weight: bold;
  background: linear-gradient(90deg, #00d4ff, #10b981);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
}

.version {
  font-size: 10px;
  color: #64748b;
  margin-top: 2px;
}

:deep(.el-menu) {
  border-right: none !important;
  flex: 1;
  overflow-y: auto;
}

:deep(.el-menu--collapse) {
  width: 64px;
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  height: 48px !important;
  line-height: 48px !important;
  transition: all 0.3s ease;
}

:deep(.el-menu-item:hover),
:deep(.el-sub-menu__title:hover) {
  background: rgba(0, 212, 255, 0.08) !important;
  color: #00d4ff !important;
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, rgba(0, 212, 255, 0.15), transparent) !important;
  color: #00d4ff !important;
  position: relative;
}

:deep(.el-menu-item.is-active)::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #00d4ff;
}

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
  display: flex;
  justify-content: center;
}

.status-tag {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.sidebar-collapse {
  position: absolute;
  right: -12px;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  background: #111827;
  border: 1px solid rgba(0, 212, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 1002;
}

.sidebar-collapse:hover {
  background: rgba(0, 212, 255, 0.2);
  border-color: #00d4ff;
  box-shadow: 0 0 12px rgba(0, 212, 255, 0.4);
}

/* 可拖动调整器 */
.sidebar-resizer {
  position: absolute;
  right: -3px;
  top: 0;
  bottom: 0;
  width: 6px;
  cursor: col-resize;
  z-index: 1003;
  display: flex;
  align-items: center;
  justify-content: center;
}

.resizer-line {
  width: 2px;
  height: 100%;
  background: transparent;
  transition: background 0.3s;
}

.sidebar-resizer:hover .resizer-line {
  background: rgba(0, 212, 255, 0.5);
}

.sidebar-resizer:active .resizer-line {
  background: #00d4ff;
}

.fade-text-enter-active,
.fade-text-leave-active {
  transition: opacity 0.2s ease;
}

.fade-text-enter-from,
.fade-text-leave-to {
  opacity: 0;
}
</style>