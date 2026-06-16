<template>
  <div class="risk-analysis-container">
    <!-- 顶部标题 -->
    <div class="page-header">
      <h1 class="title">📊 风险分析中心</h1>
      <p class="subtitle">Risk Assessment & Threat Analysis Dashboard</p>
      <div class="header-stats">
        <span class="stat-item">📈 分析任务: {{ analysisTasks.length }}</span>
        <span class="stat-item">🔴 高危风险: {{ highRiskCount }}</span>
        <span class="stat-item">✅ 已评估: {{ completedCount }}</span>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 左侧面板 - 风险概览 -->
      <div class="left-panel">
        <!-- 风险分布卡片 -->
        <div class="card risk-distribution-card">
          <div class="card-header">
            <span class="icon">📊</span>
            <span class="card-title">风险分布</span>
          </div>
          
          <div class="distribution-chart">
            <div class="pie-chart">
              <svg viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#1e293b" stroke-width="20"/>
                <circle cx="50" cy="50" r="40" fill="none" stroke="#ef4444" stroke-width="20"
                  :stroke-dasharray="highRiskPercentage * 2.51 + ' 251'" stroke-dashoffset="0"/>
                <circle cx="50" cy="50" r="40" fill="none" stroke="#f59e0b" stroke-width="20"
                  :stroke-dasharray="mediumRiskPercentage * 2.51 + ' 251'" :stroke-dashoffset="-highRiskPercentage * 2.51"/>
                <circle cx="50" cy="50" r="40" fill="none" stroke="#10b981" stroke-width="20"
                  :stroke-dasharray="lowRiskPercentage * 2.51 + ' 251'" :stroke-dashoffset="-(highRiskPercentage + mediumRiskPercentage) * 2.51"/>
              </svg>
              <div class="pie-center">
                <span class="total-count">{{ totalRiskCount }}</span>
                <span class="total-label">总风险</span>
              </div>
            </div>
            
            <div class="legend">
              <div class="legend-item">
                <span class="legend-color high"></span>
                <span class="legend-text">高风险</span>
                <span class="legend-value">{{ highRiskCount }}</span>
              </div>
              <div class="legend-item">
                <span class="legend-color medium"></span>
                <span class="legend-text">中风险</span>
                <span class="legend-value">{{ mediumRiskCount }}</span>
              </div>
              <div class="legend-item">
                <span class="legend-color low"></span>
                <span class="legend-text">低风险</span>
                <span class="legend-value">{{ lowRiskCount }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 风险趋势卡片 -->
        <div class="card trend-card">
          <div class="card-header">
            <span class="icon">📈</span>
            <span class="card-title">风险趋势</span>
          </div>
          
          <div class="trend-chart">
            <div class="chart-container">
              <div class="y-axis">
                <span>100</span>
                <span>75</span>
                <span>50</span>
                <span>25</span>
                <span>0</span>
              </div>
              <div class="chart-area">
                <svg class="line-chart" viewBox="0 0 200 100" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:0.3"/>
                      <stop offset="100%" style="stop-color:#00d4ff;stop-opacity:0"/>
                    </linearGradient>
                  </defs>
                  <path :d="areaPath" fill="url(#areaGradient)"/>
                  <path :d="linePath" fill="none" stroke="#00d4ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle v-for="(point, index) in chartPoints" :key="index"
                    :cx="point.x" :cy="point.y" r="4" fill="#00d4ff" stroke="#0f172a" stroke-width="2"/>
                </svg>
              </div>
            </div>
            <div class="x-axis">
              <span>周一</span>
              <span>周二</span>
              <span>周三</span>
              <span>周四</span>
              <span>周五</span>
              <span>周六</span>
              <span>周日</span>
            </div>
          </div>
        </div>

        <!-- 风险来源 -->
        <div class="card source-card">
          <div class="card-header">
            <span class="icon">🔍</span>
            <span class="card-title">风险来源</span>
          </div>
          
          <div class="source-list">
            <div v-for="source in riskSources" :key="source.name" class="source-item">
              <div class="source-info">
                <span class="source-icon">{{ source.icon }}</span>
                <span class="source-name">{{ source.name }}</span>
              </div>
              <div class="source-bar-wrapper">
                <div class="source-bar" :style="{ width: source.percentage + '%' }" :class="source.level"></div>
              </div>
              <span class="source-percentage">{{ source.percentage }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 中间面板 - 任务列表 -->
      <div class="middle-panel">
        <div class="card task-list-card">
          <div class="card-header">
            <span class="icon">📋</span>
            <span class="card-title">分析任务</span>
            <span class="result-count">共 {{ analysisTasks.length }} 项</span>
          </div>
          
          <div class="task-filter-tabs">
            <button 
              v-for="tab in taskTabs" 
              :key="tab.value"
              class="filter-tab"
              :class="{ active: activeTaskTab === tab.value }"
              @click="activeTaskTab = tab.value"
            >
              {{ tab.label }}
              <span class="tab-count">{{ getTaskCount(tab.value) }}</span>
            </button>
          </div>
          
          <div class="task-list">
            <div 
              v-for="task in filteredTasks" 
              :key="task.id"
              class="task-item"
              :class="{ 'risk-high': task.risk_level === 'high', 'risk-medium': task.risk_level === 'medium' }"
              @click="selectTask(task)"
            >
              <div class="task-priority" :class="task.priority">
                {{ task.priority === 'high' ? '!' : task.priority === 'medium' ? '!!' : '!!!' }}
              </div>
              <div class="task-content">
                <div class="task-header">
                  <span class="task-title">{{ task.title }}</span>
                  <span class="task-risk-badge" :class="task.risk_level">
                    {{ getRiskLevelText(task.risk_level) }}
                  </span>
                </div>
                <div class="task-meta">
                  <span class="meta-item">{{ task.source }}</span>
                  <span class="meta-item">{{ formatDate(task.created_at) }}</span>
                </div>
                <div class="task-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: task.progress + '%' }" :class="task.risk_level"></div>
                  </div>
                  <span class="progress-text">{{ task.progress }}%</span>
                </div>
              </div>
              <button class="task-action" @click.stop="viewTaskDetail(task)">
                分析
              </button>
            </div>
          </div>
          
          <div v-if="filteredTasks.length === 0" class="empty-state">
            <div class="empty-icon">📭</div>
            <p>暂无{{ getActiveTabLabel() }}任务</p>
          </div>
        </div>
      </div>

      <!-- 右侧面板 - 详情 -->
      <div class="right-panel">
        <!-- 选中任务详情 -->
        <div v-if="selectedTask" class="card detail-card">
          <div class="card-header">
            <span class="icon">📊</span>
            <span class="card-title">任务详情</span>
          </div>
          
          <div class="detail-header">
            <h3>{{ selectedTask.title }}</h3>
            <span class="detail-risk-badge" :class="selectedTask.risk_level">
              {{ getRiskLevelText(selectedTask.risk_level) }}
            </span>
          </div>
          
          <div class="detail-info-grid">
            <div class="info-item">
              <span class="info-label">任务ID</span>
              <code>{{ selectedTask.task_id }}</code>
            </div>
            <div class="info-item">
              <span class="info-label">来源</span>
              <span>{{ selectedTask.source }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">优先级</span>
              <span :class="'priority-' + selectedTask.priority">{{ getPriorityText(selectedTask.priority) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">创建时间</span>
              <span>{{ formatDate(selectedTask.created_at) }}</span>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>风险描述</h4>
            <p>{{ selectedTask.description }}</p>
          </div>
          
          <div class="detail-section">
            <h4>检测结果</h4>
            <div class="result-cards">
              <div class="result-card">
                <span class="result-icon">🎯</span>
                <div class="result-content">
                  <span class="result-label">风险评分</span>
                  <span class="result-value" :class="selectedTask.risk_level">{{ selectedTask.risk_score }}分</span>
                </div>
              </div>
              <div class="result-card">
                <span class="result-icon">📊</span>
                <div class="result-content">
                  <span class="result-label">置信度</span>
                  <span class="result-value">{{ (selectedTask.confidence * 100).toFixed(1) }}%</span>
                </div>
              </div>
              <div class="result-card">
                <span class="result-icon">⏱️</span>
                <div class="result-content">
                  <span class="result-label">检测耗时</span>
                  <span class="result-value">{{ selectedTask.duration }}s</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>建议措施</h4>
            <ul class="suggestion-list">
              <li v-for="(suggestion, index) in selectedTask.suggestions" :key="index">
                {{ suggestion }}
              </li>
            </ul>
          </div>
          
          <div class="detail-actions">
            <button class="action-btn primary" @click="generateReport(selectedTask)">
              📄 生成报告
            </button>
            <button class="action-btn secondary" @click="exportAnalysis(selectedTask)">
              📤 导出分析
            </button>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-else class="card empty-detail-card">
          <div class="empty-detail-content">
            <div class="empty-icon">👆</div>
            <p>选择一个任务查看详情</p>
            <p class="hint">点击左侧任务列表中的项目</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RiskAnalysis',
  data() {
    return {
      activeTaskTab: 'all',
      selectedTask: null,
      
      taskTabs: [
        { label: '全部', value: 'all' },
        { label: '待处理', value: 'pending' },
        { label: '分析中', value: 'analyzing' },
        { label: '已完成', value: 'completed' }
      ],
      
      analysisTasks: [
        {
          id: 1,
          task_id: 'RISK-2024-001',
          title: '视频文件深度伪造检测',
          description: '检测到视频中存在DeepFake换脸技术痕迹，人脸特征与原始视频存在明显差异。',
          source: '视频检测模块',
          risk_level: 'high',
          risk_score: 85,
          confidence: 0.92,
          priority: 'high',
          progress: 80,
          duration: 15.6,
          created_at: '2024-01-15T10:30:00Z',
          status: 'analyzing',
          suggestions: [
            '建议人工复核确认伪造内容',
            '收集原始视频进行对比分析',
            '保留检测日志作为证据'
          ]
        },
        {
          id: 2,
          task_id: 'RISK-2024-002',
          title: '音频语音克隆风险评估',
          description: '音频信号存在异常的频谱特征，疑似经过TTS语音合成处理。',
          source: '音频检测模块',
          risk_level: 'medium',
          risk_score: 62,
          confidence: 0.81,
          priority: 'medium',
          progress: 100,
          duration: 8.2,
          created_at: '2024-01-14T15:45:00Z',
          status: 'completed',
          suggestions: [
            '建议结合上下文分析真实性',
            '使用多模型交叉验证',
            '标记为待进一步验证'
          ]
        },
        {
          id: 3,
          task_id: 'RISK-2024-003',
          title: '图像文档篡改检测',
          description: '文档图像存在局部区域像素异常，可能经过编辑或合成处理。',
          source: '图像检测模块',
          risk_level: 'medium',
          risk_score: 55,
          confidence: 0.76,
          priority: 'medium',
          progress: 60,
          duration: 5.8,
          created_at: '2024-01-13T09:20:00Z',
          status: 'analyzing',
          suggestions: [
            '检查图像元数据完整性',
            '分析图像压缩痕迹',
            '与原始文档进行比对'
          ]
        },
        {
          id: 4,
          task_id: 'RISK-2024-004',
          title: '实时流视频异常检测',
          description: '实时视频流中检测到帧间不一致性，存在潜在的视频篡改风险。',
          source: '实时检测模块',
          risk_level: 'high',
          risk_score: 78,
          confidence: 0.89,
          priority: 'high',
          progress: 30,
          duration: 2.1,
          created_at: '2024-01-12T14:10:00Z',
          status: 'pending',
          suggestions: [
            '立即暂停视频流传输',
            '启动多帧比对分析',
            '通知相关负责人'
          ]
        },
        {
          id: 5,
          task_id: 'RISK-2024-005',
          title: '音频降噪处理分析',
          description: '音频文件经过降噪处理，部分原始特征已丢失，可能存在刻意掩盖痕迹。',
          source: '音频检测模块',
          risk_level: 'low',
          risk_score: 32,
          confidence: 0.65,
          priority: 'low',
          progress: 100,
          duration: 3.4,
          created_at: '2024-01-11T11:00:00Z',
          status: 'completed',
          suggestions: [
            '记录降噪处理情况',
            '作为辅助参考证据',
            '无需进一步处理'
          ]
        }
      ],
      
      riskSources: [
        { name: '视频检测', icon: '🎬', percentage: 35, level: 'high' },
        { name: '音频检测', icon: '🎵', percentage: 28, level: 'medium' },
        { name: '图像检测', icon: '🖼️', percentage: 22, level: 'medium' },
        { name: '实时流', icon: '⚡', percentage: 15, level: 'low' }
      ],
      
      weeklyRiskData: [65, 72, 58, 78, 85, 68, 75]
    }
  },
  
  computed: {
    highRiskCount() {
      return this.analysisTasks.filter(t => t.risk_level === 'high').length
    },
    
    mediumRiskCount() {
      return this.analysisTasks.filter(t => t.risk_level === 'medium').length
    },
    
    lowRiskCount() {
      return this.analysisTasks.filter(t => t.risk_level === 'low').length
    },
    
    totalRiskCount() {
      return this.highRiskCount + this.mediumRiskCount + this.lowRiskCount
    },
    
    highRiskPercentage() {
      return this.totalRiskCount > 0 ? (this.highRiskCount / this.totalRiskCount * 100).toFixed(1) : 0
    },
    
    mediumRiskPercentage() {
      return this.totalRiskCount > 0 ? (this.mediumRiskCount / this.totalRiskCount * 100).toFixed(1) : 0
    },
    
    lowRiskPercentage() {
      return this.totalRiskCount > 0 ? (this.lowRiskCount / this.totalRiskCount * 100).toFixed(1) : 0
    },
    
    completedCount() {
      return this.analysisTasks.filter(t => t.status === 'completed').length
    },
    
    filteredTasks() {
      if (this.activeTaskTab === 'all') {
        return this.analysisTasks
      }
      return this.analysisTasks.filter(t => t.status === this.activeTaskTab)
    },
    
    chartPoints() {
      const maxValue = 100
      const points = this.weeklyRiskData.map((value, index) => ({
        x: index * 33.33 + 16.67,
        y: maxValue - value
      }))
      return points
    },
    
    linePath() {
      if (this.chartPoints.length === 0) return ''
      return this.chartPoints.reduce((path, point, index) => {
        return path + (index === 0 ? `M ${point.x} ${point.y}` : ` L ${point.x} ${point.y}`)
      }, '')
    },
    
    areaPath() {
      if (this.chartPoints.length === 0) return ''
      const linePath = this.linePath
      const lastPoint = this.chartPoints[this.chartPoints.length - 1]
      const firstPoint = this.chartPoints[0]
      return `${linePath} L ${lastPoint.x} 100 L ${firstPoint.x} 100 Z`
    }
  },
  
  methods: {
    getTaskCount(status) {
      if (status === 'all') return this.analysisTasks.length
      return this.analysisTasks.filter(t => t.status === status).length
    },
    
    getActiveTabLabel() {
      const tab = this.taskTabs.find(t => t.value === this.activeTaskTab)
      return tab ? tab.label : ''
    },
    
    getRiskLevelText(level) {
      const texts = {
        high: '高风险',
        medium: '中风险',
        low: '低风险'
      }
      return texts[level] || level
    },
    
    getPriorityText(priority) {
      const texts = {
        high: '紧急',
        medium: '中等',
        low: '低'
      }
      return texts[priority] || priority
    },
    
    selectTask(task) {
      this.selectedTask = task
    },
    
    viewTaskDetail(task) {
      this.selectedTask = task
    },
    
    generateReport(task) {
      if (window.$toast) {
        window.$toast.info('📊 生成报告', `正在为任务 ${task.task_id} 生成风险分析报告...`)
      }
      // TODO: 实现真实的报告生成逻辑
    },
    
    exportAnalysis(task) {
      if (window.$toast) {
        window.$toast.info('📥 导出结果', `正在导出任务 ${task.task_id} 的分析结果...`)
      }
      // TODO: 实现真实的导出逻辑
    },
    
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.risk-analysis-container {
  padding: 0;
  color: #e2e8f0;
}

.page-header {
  margin-bottom: 2rem;
  padding: 1.5rem 2rem;
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(0, 212, 255, 0.2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(90deg, #00E5FF, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0 0 1rem 0;
}

.header-stats {
  display: flex;
  gap: 1.5rem;
  margin-top: 1rem;
}

.stat-item {
  padding: 6px 12px;
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.3);
  border-radius: 6px;
  font-size: 13px;
  color: #00E5FF;
  font-weight: 500;
}

.main-content {
  display: grid;
  grid-template-columns: 320px 1fr 320px;
  gap: 1.5rem;
}

.card {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.1);
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.card-header .icon {
  font-size: 1.5rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #f1f5f9;
}

.distribution-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.pie-chart {
  position: relative;
  width: 160px;
  height: 160px;
}

.pie-chart svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.pie-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.total-count {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #f1f5f9;
}

.total-label {
  font-size: 0.8rem;
  color: #94a3b8;
}

.legend {
  width: 100%;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.legend-color.high {
  background: #ef4444;
}

.legend-color.medium {
  background: #f59e0b;
}

.legend-color.low {
  background: #10b981;
}

.legend-text {
  flex: 1;
  font-size: 0.9rem;
  color: #94a3b8;
}

.legend-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #f1f5f9;
}

.trend-chart {
  padding-top: 1rem;
}

.chart-container {
  display: flex;
  gap: 0.5rem;
  height: 100px;
}

.y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 0.7rem;
  color: #64748b;
  text-align: right;
  width: 30px;
}

.chart-area {
  flex: 1;
  position: relative;
}

.line-chart {
  width: 100%;
  height: 100%;
}

.x-axis {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.7rem;
  color: #64748b;
}

.source-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.source-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.source-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 80px;
}

.source-icon {
  font-size: 1rem;
}

.source-name {
  font-size: 0.85rem;
  color: #e2e8f0;
}

.source-bar-wrapper {
  flex: 1;
  height: 8px;
  background: rgba(15, 23, 42, 0.8);
  border-radius: 4px;
  overflow: hidden;
}

.source-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.source-bar.high {
  background: linear-gradient(90deg, #ef4444, #f87171);
}

.source-bar.medium {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
}

.source-bar.low {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.source-percentage {
  font-size: 0.85rem;
  font-weight: 600;
  color: #00d4ff;
  width: 40px;
  text-align: right;
}

.result-count {
  margin-left: auto;
  font-size: 0.85rem;
  color: #94a3b8;
}

.task-filter-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  overflow-x: auto;
}

.filter-tab {
  padding: 0.5rem 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  color: #94a3b8;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}

.filter-tab:hover {
  border-color: #00d4ff;
  color: #00d4ff;
}

.filter-tab.active {
  background: rgba(0, 212, 255, 0.1);
  border-color: #00d4ff;
  color: #00d4ff;
}

.tab-count {
  padding: 0.125rem 0.5rem;
  background: rgba(0, 212, 255, 0.2);
  border-radius: 10px;
  font-size: 0.7rem;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 500px;
  overflow-y: auto;
}

.task-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 10px;
  border: 1px solid rgba(148, 163, 184, 0.1);
  cursor: pointer;
  transition: all 0.3s;
}

.task-item:hover {
  background: rgba(15, 23, 42, 0.7);
  border-color: rgba(0, 212, 255, 0.3);
}

.task-item.risk-high {
  border-left: 3px solid #ef4444;
}

.task-item.risk-medium {
  border-left: 3px solid #f59e0b;
}

.task-priority {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 0.8rem;
  font-weight: 700;
  flex-shrink: 0;
}

.task-priority.high {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.task-priority.medium {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.task-priority.low {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.task-content {
  flex: 1;
  min-width: 0;
}

.task-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.task-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.task-risk-badge {
  padding: 0.125rem 0.5rem;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 600;
}

.task-risk-badge.high {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.task-risk-badge.medium {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.task-risk-badge.low {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.task-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.meta-item {
  font-size: 0.8rem;
  color: #94a3b8;
}

.task-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: rgba(15, 23, 42, 0.8);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.progress-fill.high {
  background: linear-gradient(90deg, #ef4444, #f87171);
}

.progress-fill.medium {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
}

.progress-fill.low {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.progress-text {
  font-size: 0.8rem;
  color: #94a3b8;
  width: 35px;
  text-align: right;
}

.task-action {
  padding: 0.5rem 1rem;
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.3);
  border-radius: 6px;
  color: #00d4ff;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  flex-shrink: 0;
}

.task-action:hover {
  background: rgba(0, 212, 255, 0.2);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.detail-header h3 {
  font-size: 1.25rem;
  color: #f1f5f9;
  margin: 0;
  line-height: 1.4;
}

.detail-risk-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
}

.detail-risk-badge.high {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.detail-risk-badge.medium {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.detail-risk-badge.low {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.detail-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 8px;
}

.info-label {
  font-size: 0.75rem;
  color: #94a3b8;
}

.info-item code {
  font-size: 0.85rem;
  color: #00d4ff;
}

.info-item span:last-child {
  font-size: 0.85rem;
  color: #e2e8f0;
}

.info-item span.priority-high {
  color: #ef4444;
}

.info-item span.priority-medium {
  color: #f59e0b;
}

.info-item span.priority-low {
  color: #10b981;
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section h4 {
  font-size: 1rem;
  color: #f1f5f9;
  margin: 0 0 0.75rem 0;
}

.detail-section p {
  font-size: 0.9rem;
  color: #94a3b8;
  line-height: 1.5;
  margin: 0;
}

.result-cards {
  display: flex;
  gap: 0.75rem;
}

.result-card {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 8px;
}

.result-icon {
  font-size: 1.5rem;
}

.result-content {
  display: flex;
  flex-direction: column;
}

.result-label {
  font-size: 0.75rem;
  color: #94a3b8;
}

.result-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #f1f5f9;
}

.result-value.high {
  color: #ef4444;
}

.result-value.medium {
  color: #f59e0b;
}

.result-value.low {
  color: #10b981;
}

.suggestion-list {
  margin: 0;
  padding-left: 1.25rem;
}

.suggestion-list li {
  font-size: 0.85rem;
  color: #94a3b8;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.suggestion-list li:last-child {
  margin-bottom: 0;
}

.detail-actions {
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn.primary {
  background: linear-gradient(135deg, #8b5cf6, #6d28d9);
  color: #fff;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}

.action-btn.secondary {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #e2e8f0;
}

.action-btn.secondary:hover {
  border-color: #8b5cf6;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  color: #64748b;
  margin: 0;
}

.empty-detail-card {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.empty-detail-content {
  text-align: center;
}

.empty-detail-content .empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-detail-content p {
  color: #64748b;
  margin: 0 0 0.5rem 0;
}

.empty-detail-content p.hint {
  font-size: 0.85rem;
  color: #475569;
}

@media (max-width: 1400px) {
  .main-content {
    grid-template-columns: 300px 1fr;
  }
  
  .right-panel {
    grid-column: 1 / -1;
  }
}

@media (max-width: 1000px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .left-panel {
    order: 2;
  }
  
  .middle-panel {
    order: 1;
  }
  
  .right-panel {
    order: 3;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 1.5rem;
  }
  
  .header-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .detail-info-grid {
    grid-template-columns: 1fr;
  }
  
  .result-cards {
    flex-direction: column;
  }
  
  .detail-actions {
    flex-direction: column;
  }
  
  .task-meta {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style>