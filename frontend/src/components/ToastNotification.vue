<template>
  <div class="toast-container">
    <transition-group name="toast-slide">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast-notification"
        :class="toast.type"
        @click="removeToast(toast.id)"
      >
        <div class="toast-icon">
          <span v-if="toast.type === 'success'">✅</span>
          <span v-else-if="toast.type === 'error'">❌</span>
          <span v-else-if="toast.type === 'warning'">⚠️</span>
          <span v-else>ℹ️</span>
        </div>
        <div class="toast-content">
          <div class="toast-title">{{ toast.title }}</div>
          <div class="toast-message">{{ toast.message }}</div>
        </div>
        <button class="toast-close" @click.stop="removeToast(toast.id)">✕</button>
        <div class="toast-progress" :style="{ width: toast.progress + '%' }"></div>
      </div>
    </transition-group>
  </div>
</template>

<script>
export default {
  name: 'ToastNotification',
  data() {
    return {
      toasts: [],
      nextId: 1
    }
  },
  methods: {
    show(title, message, type = 'info', duration = 3000) {
      const id = this.nextId++
      const toast = {
        id,
        title,
        message,
        type,
        progress: 100,
        duration
      }
      
      this.toasts.push(toast)
      
      // 自动移除
      if (duration > 0) {
        const startTime = Date.now()
        const interval = setInterval(() => {
          const elapsed = Date.now() - startTime
          const remaining = Math.max(0, duration - elapsed)
          const toastIndex = this.toasts.findIndex(t => t.id === id)
          
          if (toastIndex !== -1) {
            this.toasts[toastIndex].progress = (remaining / duration) * 100
          }
          
          if (remaining <= 0) {
            clearInterval(interval)
            this.removeToast(id)
          }
        }, 50)
        
        setTimeout(() => {
          clearInterval(interval)
          this.removeToast(id)
        }, duration)
      }
      
      return id
    },
    
    success(title, message, duration = 3000) {
      return this.show(title, message, 'success', duration)
    },
    
    error(title, message, duration = 5000) {
      return this.show(title, message, 'error', duration)
    },
    
    warning(title, message, duration = 4000) {
      return this.show(title, message, 'warning', duration)
    },
    
    info(title, message, duration = 3000) {
      return this.show(title, message, 'info', duration)
    },
    
    removeToast(id) {
      const index = this.toasts.findIndex(t => t.id === id)
      if (index !== -1) {
        this.toasts.splice(index, 1)
      }
    }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 420px;
  pointer-events: none;
}

.toast-notification {
  pointer-events: auto;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(12px);
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 
              0 0 0 1px rgba(148, 163, 184, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  min-width: 320px;
}

.toast-notification:hover {
  transform: translateX(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), 
              0 0 0 1px rgba(148, 163, 184, 0.2);
}

.toast-notification.success {
  border-left: 4px solid #10b981;
}

.toast-notification.error {
  border-left: 4px solid #ef4444;
}

.toast-notification.warning {
  border-left: 4px solid #f59e0b;
}

.toast-notification.info {
  border-left: 4px solid #3b82f6;
}

.toast-icon {
  font-size: 20px;
  flex-shrink: 0;
  margin-top: 2px;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-size: 14px;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 4px;
  line-height: 1.4;
}

.toast-message {
  font-size: 13px;
  color: #94a3b8;
  line-height: 1.5;
  word-wrap: break-word;
}

.toast-close {
  background: transparent;
  border: none;
  color: #64748b;
  font-size: 16px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
  flex-shrink: 0;
}

.toast-close:hover {
  background: rgba(148, 163, 184, 0.1);
  color: #f1f5f9;
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: currentColor;
  opacity: 0.3;
  transition: width linear;
}

.toast-notification.success .toast-progress {
  background: #10b981;
}

.toast-notification.error .toast-progress {
  background: #ef4444;
}

.toast-notification.warning .toast-progress {
  background: #f59e0b;
}

.toast-notification.info .toast-progress {
  background: #3b82f6;
}

/* 动画 */
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-slide-enter-from {
  opacity: 0;
  transform: translateX(100px);
}

.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(100px);
}

.toast-slide-move {
  transition: transform 0.3s ease;
}

@media (max-width: 768px) {
  .toast-container {
    left: 20px;
    right: 20px;
    max-width: none;
  }
  
  .toast-notification {
    min-width: auto;
  }
}
</style>
