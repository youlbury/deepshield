<template>
  <div class="navbar">
    <div class="page-title">
      <h2>{{ currentPageTitle }}</h2>
    </div>
    <div class="navbar-actions">
      <el-tag type="success" effect="plain" class="server-badge">
        <el-icon class="pulse-dot"><Loading /></el-icon>
        <span>系统运行中</span>
      </el-tag>
      
      <el-dropdown @command="handleCommand" trigger="click">
        <el-button type="primary" link class="user-btn">
          <el-avatar :size="32" class="user-avatar">A</el-avatar>
          <span class="username">{{ username }}</span>
          <el-icon><ArrowDown /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="logout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Loading, ArrowDown, SwitchButton } from '@element-plus/icons-vue'
import { logout } from '../../../store/auth'

const route = useRoute()
const router = useRouter()

const username = computed(() => localStorage.getItem('username') || 'admin')

const currentPageTitle = computed(() => {
  const titles = {
    '/': '首页概览',
    '/image': '图片检测',
    '/video': '视频检测',
    '/audio': '音频检测',
    '/forensics': '数字取证',
    '/models': '模型实验',
    '/benchmark': '性能评估',
    '/about': '关于系统'
  }
  return titles[route.path] || 'DeepShield'
})

const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      logout()
      router.push('/')
      ElMessage.success('已退出登录')
    }).catch(() => {})
  }
}
</script>

<style scoped>
.navbar {
  background: rgba(17, 24, 39, 0.95);
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 60px;
}

.page-title h2 {
  font-size: 18px;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.navbar-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}

.server-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
}

.pulse-dot {
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.user-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e2e8f0 !important;
}

.user-btn:hover {
  color: #00d4ff !important;
}

.user-avatar {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  color: white;
  font-weight: bold;
}

.username {
  font-size: 14px;
  font-weight: 500;
}
</style>