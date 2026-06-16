<template>
  <div class="home-page">
    <!-- 主标题区域 -->
    <div class="hero-section">
      <div class="hero-bg"></div>
      <div class="hero-content">
        <div class="logo-section">
          <img src="../assets/影盾DeepShield.png" alt="DeepShield" class="hero-logo" />
          <h1 class="hero-title">DeepShield</h1>
          <p class="hero-subtitle">多模态深度伪造检测与数字取证平台</p>
        </div>
        
        <div class="features-grid">
          <div class="feature-item" @click="goFeature('/image')">🖼️ 图片检测</div>
          <div class="feature-item" @click="goFeature('/video')">🎬 视频检测</div>
          <div class="feature-item" @click="goFeature('/audio')">🎵 音频检测</div>
          <div class="feature-item" @click="goFeature('/forensics')">🔍 数字取证</div>
          <div class="feature-item" @click="goFeature('/verify')">🔗 证据验真</div>
          <div class="feature-item" @click="goFeature('/models')">🧪 模型实验</div>
        </div>
      </div>
    </div>

    <!-- 统计数据 -->
    <div class="stats-row">
      <div class="stat-card">
        <span class="stat-number">{{ animatedStats.total }}</span>
        <span class="stat-label">检测样本数</span>
      </div>
      <div class="stat-card">
        <span class="stat-number">{{ animatedStats.models }}</span>
        <span class="stat-label">模型数量</span>
      </div>
      <div class="stat-card">
        <span class="stat-number">{{ animatedStats.datasets }}</span>
        <span class="stat-label">支持数据集</span>
      </div>
      <div class="stat-card highlight">
        <span class="stat-number">{{ animatedStats.accuracy }}%</span>
        <span class="stat-label">平均准确率</span>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <button v-if="!isLoggedIn" class="action-btn primary" @click="goToLogin">
        <span class="btn-icon">🔐</span>
        <span>登录使用</span>
      </button>
      <button v-else class="action-btn primary" @click="goToDetect">
        <span class="btn-icon">🛡️</span>
        <span>开始检测</span>
      </button>
      <button class="action-btn secondary" @click="goToModelLab">
        <span class="btn-icon">🧪</span>
        <span>模型实验</span>
      </button>
    </div>

    <!-- 右侧动态轮播 -->
    <div class="carousel-section">
      <div class="carousel-card compact">
        <div class="carousel-header">
          <span class="carousel-title">📢 检测公告</span>
          <button class="carousel-nav prev" @click="prevCarousel">‹</button>
          <button class="carousel-nav next" @click="nextCarousel">›</button>
        </div>
        <div class="carousel-content">
          <div v-for="(item, index) in carouselItems" :key="index" 
               class="carousel-item" :class="{ active: currentCarouselIndex === index }">
            <div class="item-icon">{{ item.icon }}</div>
            <div class="item-content">
              <h4>{{ item.title }}</h4>
              <p>{{ item.description }}</p>
              <span class="item-time">{{ item.time }}</span>
            </div>
          </div>
        </div>
        <div class="carousel-dots">
          <span 
            v-for="(_, index) in carouselItems" 
            :key="index" 
            class="dot" 
            :class="{ active: currentCarouselIndex === index }"
            @click="currentCarouselIndex = index"
          ></span>
        </div>
      </div>

      <div class="info-cards-wrapper">
        <!-- 最新模型 -->
        <div class="info-card">
          <div class="card-header">
            <span class="card-icon">🏆</span>
            <span class="card-title">最新模型</span>
          </div>
          <div class="model-list">
            <div v-for="model in latestModels" :key="model.name" class="model-item">
              <span class="model-name">{{ model.name }}</span>
              <span class="model-accuracy">{{ model.accuracy }}</span>
            </div>
          </div>
        </div>

        <!-- 最新数据集 -->
        <div class="info-card">
          <div class="card-header">
            <span class="card-icon">📊</span>
            <span class="card-title">最新数据集</span>
          </div>
          <div class="dataset-list">
            <div v-for="dataset in latestDatasets" :key="dataset.name" class="dataset-item">
              <span class="dataset-name">{{ dataset.name }}</span>
              <span class="dataset-size">{{ dataset.size }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { authState } from '../store/auth'

export default {
  name: 'Home',
  data() {
    return {
      currentCarouselIndex: 0,
      stats: { total: 12847, models: 15, datasets: 8, accuracy: 96.8 },
      animatedStats: { total: 0, models: 0, datasets: 0, accuracy: 0 },
      
      carouselItems: [
        {
          icon: '🔔',
          title: '系统更新通知',
          description: 'v2.0版本已发布，新增TimeSformer视频检测模型',
          time: '2分钟前'
        },
        {
          icon: '🔥',
          title: '高危样本预警',
          description: '检测到一批高风险深度伪造视频，请及时处理',
          time: '15分钟前'
        },
        {
          icon: '📈',
          title: '性能优化',
          description: '检测速度提升30%，平均响应时间降至2.3秒',
          time: '1小时前'
        },
        {
          icon: '🆕',
          title: '新数据集上线',
          description: 'DFDC-V2数据集已完成集成，包含10万+样本',
          time: '3小时前'
        }
      ],
      
      latestModels: [
        { name: 'TimeSformer', accuracy: '97.2%' },
        { name: 'EfficientNet', accuracy: '96.5%' },
        { name: 'Xception', accuracy: '96.2%' },
        { name: 'F3Net', accuracy: '95.8%' }
      ],
      
      latestDatasets: [
        { name: 'DFDC-V2', size: '100K+' },
        { name: 'FaceForensics++', size: '50K+' },
        { name: 'CelebDF', size: '10K+' },
        { name: 'ASVspoof', size: '20K+' }
      ],
      
      carouselInterval: null
    }
  },
  
  computed: {
    isLoggedIn() {
      return authState.isLoggedIn
    }
  },

  mounted() {
    this.animateStats()
    this.startCarousel()
  },
  
  beforeUnmount() {
    if (this.carouselInterval) {
      clearInterval(this.carouselInterval)
    }
  },
  
  methods: {
    animateStats() {
      const duration = 1500
      const steps = 60
      const interval = duration / steps
      
      let step = 0
      const timer = setInterval(() => {
        step++
        const progress = step / steps
        
        this.animatedStats.total = Math.floor(this.stats.total * progress)
        this.animatedStats.models = Math.floor(this.stats.models * progress)
        this.animatedStats.datasets = Math.floor(this.stats.datasets * progress)
        this.animatedStats.accuracy = (this.stats.accuracy * progress).toFixed(1)
        
        if (step >= steps) {
          clearInterval(timer)
          this.animatedStats = { ...this.stats }
        }
      }, interval)
    },
    
    startCarousel() {
      this.carouselInterval = setInterval(() => {
        this.nextCarousel()
      }, 4000)
    },
    
    nextCarousel() {
      this.currentCarouselIndex = (this.currentCarouselIndex + 1) % this.carouselItems.length
    },
    
    prevCarousel() {
      this.currentCarouselIndex = (this.currentCarouselIndex - 1 + this.carouselItems.length) % this.carouselItems.length
    },
    
    goToLogin() {
      // 跳转到登录界面
      this.$router.push('/login')
    },
    
    goToDetect() {
      // 已登录，跳转到图片检测
      this.$router.push('/image')
    },
    
    goToModelLab() {
      if (!authState.isLoggedIn) {
        this.$router.push('/login')
      } else {
        this.$router.push('/models')
      }
    },

    goFeature(path) {
      if (!authState.isLoggedIn) {
        this.$router.push('/login')
      } else {
        this.$router.push(path)
      }
    }
  }
}
</script>

<style scoped>
.home-page {
  padding: 0;
  height: 100%;
  overflow: hidden;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: clamp(0.75rem, 2vh, 1.25rem);
}

/* Hero区域 */
.hero-section {
  position: relative;
  padding: clamp(1rem, 3vh, 2rem);
  background: linear-gradient(135deg, #141C2F 0%, #0A1020 100%);
  border-radius: clamp(12px, 1.5vh, 16px);
  border: 1px solid rgba(0, 212, 255, 0.2);
  overflow: hidden;
  flex-shrink: 0;
  flex: 0 0 auto;
}

.hero-bg {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at 30% 30%, rgba(0, 212, 255, 0.15) 0%, transparent 50%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.hero-content {
  position: relative;
  z-index: 1;
}

.logo-section {
  text-align: center;
  margin-bottom: clamp(1rem, 3vh, 2rem);
}

.hero-logo {
  width: clamp(50px, 6vh, 80px);
  height: clamp(50px, 6vh, 80px);
  margin-bottom: clamp(0.5rem, 1.5vh, 1rem);
}

.hero-title {
  font-size: clamp(1.8rem, 4vh, 3.5rem);
  font-weight: 800;
  margin: 0 0 clamp(0.25rem, 0.75vh, 0.5rem) 0;
  background: linear-gradient(90deg, #00D4FF, #00FF88);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 40px rgba(0, 212, 255, 0.4);
}

.hero-subtitle {
  font-size: clamp(0.85rem, 1.5vh, 1.1rem);
  color: #94a3b8;
  margin: 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: clamp(0.5rem, 1.5vh, 1rem);
}

.feature-item {
  padding: clamp(0.6rem, 1.5vh, 1rem);
  background: rgba(0, 212, 255, 0.08);
  border: 1px solid rgba(0, 212, 255, 0.15);
  border-radius: clamp(8px, 1vh, 10px);
  text-align: center;
  font-size: clamp(0.75rem, 1.25vh, 0.9rem);
  color: #e2e8f0;
  cursor: pointer; /* 添加鼠标指针 */
  transition: all 0.3s;
}

.feature-item:hover {
  background: rgba(0, 212, 255, 0.2); /* 增强悬停效果 */
  border-color: rgba(0, 212, 255, 0.5);
  transform: translateY(-3px); /* 增加上移距离 */
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3); /* 添加阴影 */
}

/* 统计卡片 */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: clamp(0.5rem, 1.5vh, 1rem);
  flex-shrink: 0;
  flex: 0 0 auto;
}

.stat-card {
  padding: clamp(0.75rem, 2vh, 1.5rem);
  background: #141C2F;
  border-radius: clamp(10px, 1.25vh, 12px);
  border: 1px solid rgba(0, 212, 255, 0.15);
  text-align: center;
  transition: all 0.3s;
}

.stat-card:hover {
  border-color: rgba(0, 212, 255, 0.4);
  transform: translateY(-3px);
}

.stat-card.highlight {
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(0, 255, 136, 0.05));
  border-color: rgba(0, 212, 255, 0.3);
}

.stat-number {
  display: block;
  font-size: clamp(1.5rem, 3.5vh, 2.2rem);
  font-weight: 700;
  color: #00D4FF;
  margin-bottom: clamp(0.25rem, 0.5vh, 0.35rem);
}

.stat-card.highlight .stat-number {
  color: #00FF88;
}

.stat-label {
  font-size: clamp(0.7rem, 1.25vh, 0.85rem);
  color: #94a3b8;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: clamp(0.75rem, 2vh, 1.25rem);
  flex-shrink: 0;
  flex: 0 0 auto;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1.25vh, 0.75rem);
  padding: clamp(0.75rem, 2vh, 1rem) clamp(1.5rem, 4vh, 2.5rem);
  border-radius: clamp(10px, 1.25vh, 12px);
  font-size: clamp(0.9rem, 1.75vh, 1.1rem);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.action-btn.primary {
  background: linear-gradient(135deg, #00D4FF, #0099cc);
  color: #0A1020;
  box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
}

.action-btn.primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0, 212, 255, 0.4);
}

.action-btn.secondary {
  background: rgba(10, 16, 32, 0.8);
  border: 1px solid rgba(0, 212, 255, 0.3);
  color: #e2e8f0;
}

.action-btn.secondary:hover {
  background: rgba(0, 212, 255, 0.1);
  border-color: #00D4FF;
  transform: translateY(-3px);
}

.btn-icon {
  font-size: clamp(1rem, 2.5vh, 1.3rem);
}

/* 轮播区域 */
.carousel-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: clamp(0.5rem, 1.5vh, 1rem);
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.carousel-section > .info-card {
  display: flex;
  flex-direction: column;
  gap: clamp(0.5rem, 1.5vh, 1rem);
}

.carousel-section > .info-card + .info-card {
  margin-top: 0;
}

.info-cards-wrapper {
  display: flex;
  flex-direction: column;
  gap: clamp(0.5rem, 1.5vh, 1rem);
  height: 100%;
  overflow: hidden;
}

.info-cards-wrapper .info-card {
  flex: 1;
  min-height: 0;
}

.carousel-card {
  background: #141C2F;
  border-radius: clamp(10px, 1.25vh, 12px);
  border: 1px solid rgba(0, 212, 255, 0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.carousel-card.compact {
  max-height: 280px;
}

.carousel-header {
  display: flex;
  align-items: center;
  padding: clamp(0.5rem, 1.5vh, 0.75rem) clamp(0.75rem, 2vh, 1rem);
  border-bottom: 1px solid rgba(0, 212, 255, 0.1);
  background: linear-gradient(90deg, rgba(0, 212, 255, 0.08), rgba(0, 255, 136, 0.03));
  flex-shrink: 0;
}

.carousel-title {
  flex: 1;
  font-size: clamp(0.8rem, 1.4vh, 0.95rem);
  font-weight: 600;
  color: #f1f5f9;
}

.carousel-nav {
  width: clamp(22px, 2.5vh, 28px);
  height: clamp(22px, 2.5vh, 28px);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 50%;
  background: rgba(10, 16, 32, 0.8);
  color: #94a3b8;
  font-size: clamp(0.9rem, 1.75vh, 1.1rem);
  cursor: pointer;
  transition: all 0.3s;
  margin-left: clamp(0.25rem, 0.75vh, 0.375rem);
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.carousel-nav:hover {
  background: rgba(0, 212, 255, 0.2);
  color: #00D4FF;
}

.carousel-content {
  padding: clamp(0.625rem, 1.75vh, 1rem);
  flex: 1;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.carousel-item {
  display: flex;
  gap: clamp(0.5rem, 1.25vh, 0.875rem);
  display: none;
  width: 100%;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateX(10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.carousel-item.active {
  display: flex;
}

.item-icon {
  font-size: clamp(1.25rem, 2.75vh, 1.75rem);
  width: clamp(32px, 4.5vh, 45px);
  height: clamp(32px, 4.5vh, 45px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(0, 255, 136, 0.1));
  border-radius: clamp(6px, 0.875vh, 8px);
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 212, 255, 0.15);
}

.item-content {
  flex: 1;
}

.item-content h4 {
  font-size: clamp(0.8rem, 1.35vh, 0.95rem);
  color: #f1f5f9;
  margin: 0 0 clamp(0.2rem, 0.4vh, 0.3rem) 0;
  font-weight: 600;
}

.item-content p {
  font-size: clamp(0.7rem, 1.15vh, 0.8rem);
  color: #94a3b8;
  margin: 0 0 clamp(0.2rem, 0.4vh, 0.3rem) 0;
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-time {
  font-size: clamp(0.6rem, 0.95vh, 0.7rem);
  color: #64748b;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.item-time::before {
  content: '⏱️';
  font-size: 0.7em;
}

.carousel-dots {
  display: flex;
  justify-content: center;
  gap: clamp(0.3rem, 0.75vh, 0.4rem);
  padding: clamp(0.5rem, 1.25vh, 0.75rem);
  flex-shrink: 0;
  background: rgba(0, 212, 255, 0.02);
  border-top: 1px solid rgba(0, 212, 255, 0.08);
}

.dot {
  width: clamp(5px, 0.875vh, 7px);
  height: clamp(5px, 0.875vh, 7px);
  border-radius: 50%;
  background: rgba(0, 212, 255, 0.25);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dot:hover {
  background: rgba(0, 212, 255, 0.5);
  transform: scale(1.2);
}

.dot.active {
  background: linear-gradient(90deg, #00D4FF, #00FF88);
  width: clamp(18px, 2.5vh, 24px);
  border-radius: clamp(3px, 0.5vh, 4px);
  box-shadow: 0 0 8px rgba(0, 212, 255, 0.4);
}

/* 信息卡片 */
.info-card {
  background: #141C2F;
  border-radius: clamp(10px, 1.25vh, 12px);
  border: 1px solid rgba(0, 212, 255, 0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  gap: clamp(0.375rem, 1vh, 0.5rem);
  padding: clamp(0.75rem, 2vh, 1rem) clamp(0.875rem, 2.5vh, 1.25rem);
  border-bottom: 1px solid rgba(0, 212, 255, 0.1);
  background: rgba(0, 212, 255, 0.03);
  flex-shrink: 0;
}

.card-icon {
  font-size: clamp(0.95rem, 1.75vh, 1.1rem);
}

.card-title {
  font-size: clamp(0.8rem, 1.4vh, 0.95rem);
  font-weight: 600;
  color: #f1f5f9;
}

.model-list,
.dataset-list {
  padding: clamp(0.375rem, 1vh, 0.5rem);
  flex: 1;
  overflow-y: auto;
}

.model-item,
.dataset-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: clamp(0.5rem, 1.25vh, 0.75rem);
  border-radius: clamp(6px, 0.75vh, 8px);
  margin-bottom: clamp(0.25rem, 0.5vh, 0.35rem);
  transition: all 0.3s;
}

.model-item:hover,
.dataset-item:hover {
  background: rgba(0, 212, 255, 0.08);
}

.model-item:last-child,
.dataset-item:last-child {
  margin-bottom: 0;
}

.model-name,
.dataset-name {
  font-size: 0.85rem;
  color: #e2e8f0;
}

.model-accuracy {
  font-size: 0.85rem;
  font-weight: 600;
  color: #00FF88;
}

.dataset-size {
  font-size: 0.85rem;
  color: #00D4FF;
}

@media (max-width: 1366px) {
  .features-grid {
    grid-template-columns: repeat(6, 1fr);
  }
  
  .stats-row {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .carousel-section {
    grid-template-columns: 2fr 1fr;
  }
}

@media (max-width: 1200px) {
  .features-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .carousel-section {
    grid-template-columns: 1fr;
  }
  
  .info-cards-wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: clamp(0.5rem, 1.5vh, 1rem);
  }
}

@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .action-btn {
    width: 100%;
    justify-content: center;
  }
  
  .info-cards-wrapper {
    grid-template-columns: 1fr;
  }
}
</style>