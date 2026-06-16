<template>
  <div class="forensics-container">
    <!-- 科技感背景粒子效果 -->
    <div class="bg-particles"></div>
    
    <!-- 顶部标题 -->
    <div class="page-header">
      <div class="header-glow"></div>
      <h1 class="title">🔍 取证分析中心</h1>
      <p class="subtitle">Digital Evidence Forensics & Chain of Custody Management</p>
      <div class="header-stats">
        <span class="stat-item">📁 证据总数: {{ evidenceList.length }}</span>
        <span class="stat-item">⚠️ 高风险: {{ highRiskCount }}</span>
        <span class="stat-item">📄 报告生成: {{ reportCount }}</span>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 左侧面板 - 搜索和筛选 -->
      <div class="left-panel">
        <!-- 搜索卡片 -->
        <div class="card search-card">
          <div class="card-header">
            <span class="icon">🔍</span>
            <span class="card-title">搜索证据</span>
          </div>
          
          <div class="search-input-wrapper">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="搜索证据ID、文件名..." 
              class="search-input"
            />
            <button class="search-btn" @click="searchEvidence">
              <span>搜索</span>
            </button>
          </div>
          
          <!-- 筛选条件 -->
          <div class="filter-section">
            <div class="filter-item">
              <label>风险等级</label>
              <select v-model="filterRisk" class="filter-select">
                <option value="all">全部</option>
                <option value="high">高风险</option>
                <option value="medium">中风险</option>
                <option value="low">低风险</option>
              </select>
            </div>
            
            <div class="filter-item">
              <label>文件类型</label>
              <select v-model="filterType" class="filter-select">
                <option value="all">全部</option>
                <option value="image">图片</option>
                <option value="video">视频</option>
                <option value="audio">音频</option>
              </select>
            </div>
            
            <div class="filter-item">
              <label>检测状态</label>
              <select v-model="filterStatus" class="filter-select">
                <option value="all">全部</option>
                <option value="completed">已完成</option>
                <option value="pending">待审核</option>
              </select>
            </div>
          </div>
          
          <button class="filter-reset-btn" @click="resetFilters">
            重置筛选
          </button>
        </div>

        <!-- 快捷操作 -->
        <div class="card action-card">
          <div class="card-header">
            <span class="icon">⚡</span>
            <span class="card-title">快捷操作</span>
          </div>
          
          <div class="action-buttons">
            <button class="action-btn primary" @click="exportAllEvidence">
              <span>📊 导出全部证据</span>
            </button>
            <button class="action-btn secondary" @click="generateSummary">
              <span>📈 生成汇总报告</span>
            </button>
            <button class="action-btn danger" @click="clearSelected">
              <span>🗑️ 清空已选</span>
            </button>
          </div>
        </div>
      </div>

      <!-- 右侧面板 -->
      <div class="right-panel">
        <!-- 证据列表 -->
        <div class="card evidence-list-card">
          <div class="card-header">
            <span class="icon">📋</span>
            <span class="card-title">证据列表</span>
            <span class="result-count">共 {{ filteredEvidence.length }} 条记录</span>
          </div>
          
          <!-- 列表头部 -->
          <div class="list-header">
            <label class="checkbox-label">
              <input type="checkbox" @change="toggleSelectAll" :checked="allSelected" />
              <span>全选</span>
            </label>
            <div class="sort-options">
              <select v-model="sortBy" class="sort-select">
                <option value="timestamp">按时间排序</option>
                <option value="risk_score">按风险排序</option>
                <option value="filename">按文件名排序</option>
              </select>
              <button class="sort-btn" @click="toggleSortOrder">
                {{ sortOrder === 'desc' ? '↓' : '↑' }}
              </button>
            </div>
          </div>
          
          <!-- 证据列表 -->
          <div class="evidence-list">
            <div 
              v-for="evidence in filteredEvidence" 
              :key="evidence.id"
              class="evidence-item"
              :class="{ 'selected': selectedEvidence.includes(evidence.id), 'risk-high': evidence.risk_score >= 70, 'risk-medium': evidence.risk_score >= 40 && evidence.risk_score < 70 }"
              @click="selectEvidence(evidence.id)"
            >
              <label class="checkbox-label">
                <input type="checkbox" :checked="selectedEvidence.includes(evidence.id)" @change.stop="toggleSelect(evidence.id)" />
              </label>
              
              <div class="evidence-icon" :class="evidence.type">
                {{ getFileIcon(evidence.type) }}
              </div>
              
              <div class="evidence-info">
                <div class="evidence-header">
                  <span class="evidence-filename">{{ evidence.filename }}</span>
                  <span class="evidence-risk-badge" :class="getRiskClass(evidence.risk_score)">
                    {{ getRiskLevel(evidence.risk_score) }}
                  </span>
                </div>
                <div class="evidence-meta">
                  <span class="meta-item">📅 {{ formatDate(evidence.timestamp) }}</span>
                  <span class="meta-item">🆔 {{ evidence.evidence_id }}</span>
                  <span class="meta-item">🎯 {{ evidence.risk_score }}分</span>
                </div>
              </div>
              
              <button class="view-btn" @click.stop="viewEvidence(evidence)">
                查看详情
              </button>
            </div>
          </div>
          
          <!-- 空状态 -->
          <div v-if="filteredEvidence.length === 0" class="empty-state">
            <div class="empty-icon">📭</div>
            <p>暂无匹配的证据记录</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 证据详情弹窗 -->
    <div v-if="selectedEvidenceDetail" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>证据详情</h2>
          <button class="close-btn" @click="closeModal">✕</button>
        </div>
        
        <div class="modal-body">
          <!-- 基本信息 -->
          <div class="detail-section">
            <h3>基本信息</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">证据ID</span>
                <code>{{ selectedEvidenceDetail.evidence_id }}</code>
              </div>
              <div class="detail-item">
                <span class="detail-label">文件名</span>
                <span>{{ selectedEvidenceDetail.filename }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">文件类型</span>
                <span>{{ selectedEvidenceDetail.type }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">检测时间</span>
                <span>{{ formatDate(selectedEvidenceDetail.timestamp) }}</span>
              </div>
            </div>
          </div>

          <!-- 风险评估 -->
          <div class="detail-section">
            <h3>风险评估</h3>
            <div class="risk-display" :class="getRiskClass(selectedEvidenceDetail.risk_score)">
              <div class="risk-circle">
                <span class="risk-value">{{ selectedEvidenceDetail.risk_score }}</span>
                <span class="risk-label">风险分</span>
              </div>
              <div class="risk-info">
                <h4>{{ getRiskLevel(selectedEvidenceDetail.risk_score) }}</h4>
                <p>{{ getRiskDescription(selectedEvidenceDetail.risk_score) }}</p>
              </div>
            </div>
          </div>

          <!-- 检测结果 -->
          <div class="detail-section">
            <h3>检测结果</h3>
            <div class="result-grid">
              <div class="result-item">
                <span class="result-label">检测模型</span>
                <span class="result-value">{{ selectedEvidenceDetail.model_name }}</span>
              </div>
              <div class="result-item">
                <span class="result-label">置信度</span>
                <span class="result-value">{{ (selectedEvidenceDetail.confidence * 100).toFixed(2) }}%</span>
              </div>
              <div class="result-item">
                <span class="result-label">伪造类型</span>
                <span class="result-value">{{ selectedEvidenceDetail.forgery_type || '未检测到伪造' }}</span>
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="modal-actions">
            <button class="modal-btn primary" @click="downloadReport(selectedEvidenceDetail)">
              📄 下载取证报告
            </button>
            <button class="modal-btn secondary" @click="viewFullReport(selectedEvidenceDetail)">
              📊 查看完整报告
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 自定义提示框 -->
    <transition name="alert-fade">
      <div v-if="customAlert.show" class="custom-alert-overlay" @click.self="customAlert.show = false">
        <div class="custom-alert-box">
          <div class="alert-header">
            <span class="alert-title">{{ customAlert.title }}</span>
            <button class="alert-close" @click="customAlert.show = false">×</button>
          </div>
          <div class="alert-body">
            <ul class="alert-messages">
              <li v-for="(msg, index) in customAlert.messages" :key="index">{{ msg }}</li>
            </ul>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'Forensics',
  data() {
    return {
      searchQuery: '',
      filterRisk: 'all',
      filterType: 'all',
      filterStatus: 'all',
      sortBy: 'timestamp',
      sortOrder: 'desc',
      selectedEvidence: [],
      selectedEvidenceDetail: null,
      customAlert: {
        show: false,
        title: '',
        messages: []
      },
      
      evidenceList: [
        {
          id: 1,
          evidence_id: 'EVID-2024-001',
          filename: 'meeting_video.mp4',
          type: 'video',
          risk_score: 85,
          confidence: 0.92,
          model_name: 'EfficientNet + LSTM',
          forgery_type: 'DeepFake换脸',
          timestamp: '2024-01-15T10:30:00Z',
          status: 'completed'
        },
        {
          id: 2,
          evidence_id: 'EVID-2024-002',
          filename: 'document_scan.jpg',
          type: 'image',
          risk_score: 25,
          confidence: 0.88,
          model_name: 'Ensemble',
          forgery_type: null,
          timestamp: '2024-01-14T15:45:00Z',
          status: 'completed'
        },
        {
          id: 3,
          evidence_id: 'EVID-2024-003',
          filename: 'voice_recording.wav',
          type: 'audio',
          risk_score: 68,
          confidence: 0.76,
          model_name: 'AASIST',
          forgery_type: 'TTS语音合成',
          timestamp: '2024-01-13T09:20:00Z',
          status: 'pending'
        },
        {
          id: 4,
          evidence_id: 'EVID-2024-004',
          filename: 'contract_signature.png',
          type: 'image',
          risk_score: 45,
          confidence: 0.81,
          model_name: 'HiFi-Net',
          forgery_type: '图像篡改',
          timestamp: '2024-01-12T14:10:00Z',
          status: 'completed'
        },
        {
          id: 5,
          evidence_id: 'EVID-2024-005',
          filename: 'video_clip.mov',
          type: 'video',
          risk_score: 18,
          confidence: 0.95,
          model_name: 'Temporal',
          forgery_type: null,
          timestamp: '2024-01-11T11:00:00Z',
          status: 'completed'
        },
        {
          id: 6,
          evidence_id: 'EVID-2024-006',
          filename: 'interview_audio.mp3',
          type: 'audio',
          risk_score: 72,
          confidence: 0.89,
          model_name: 'Wav2Vec 2.0',
          forgery_type: '语音克隆',
          timestamp: '2024-01-10T16:30:00Z',
          status: 'pending'
        }
      ]
    }
  },
  
  computed: {
    highRiskCount() {
      return this.evidenceList.filter(e => e.risk_score >= 70).length
    },
    
    reportCount() {
      return this.evidenceList.filter(e => e.status === 'completed').length
    },
    
    allSelected() {
      return this.filteredEvidence.length > 0 && 
             this.filteredEvidence.every(e => this.selectedEvidence.includes(e.id))
    },
    
    filteredEvidence() {
      let result = [...this.evidenceList]
      
      // 搜索过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(e => 
          e.evidence_id.toLowerCase().includes(query) ||
          e.filename.toLowerCase().includes(query)
        )
      }
      
      // 风险等级过滤
      if (this.filterRisk !== 'all') {
        result = result.filter(e => {
          if (this.filterRisk === 'high') return e.risk_score >= 70
          if (this.filterRisk === 'medium') return e.risk_score >= 40 && e.risk_score < 70
          if (this.filterRisk === 'low') return e.risk_score < 40
          return true
        })
      }
      
      // 文件类型过滤
      if (this.filterType !== 'all') {
        result = result.filter(e => e.type === this.filterType)
      }
      
      // 状态过滤
      if (this.filterStatus !== 'all') {
        result = result.filter(e => e.status === this.filterStatus)
      }
      
      // 排序
      result.sort((a, b) => {
        let comparison = 0
        if (this.sortBy === 'timestamp') {
          comparison = new Date(a.timestamp) - new Date(b.timestamp)
        } else if (this.sortBy === 'risk_score') {
          comparison = a.risk_score - b.risk_score
        } else if (this.sortBy === 'filename') {
          comparison = a.filename.localeCompare(b.filename)
        }
        
        return this.sortOrder === 'desc' ? -comparison : comparison
      })
      
      return result
    }
  },
  
  methods: {
    showCustomAlert(title, messages) {
      // 使用自定义弹窗组件替代原生alert
      this.customAlert = {
        show: true,
        title: title,
        messages: Array.isArray(messages) ? messages : [messages]
      }
      
      // 3秒后自动关闭
      setTimeout(() => {
        this.customAlert.show = false
      }, 3000)
    },
    
    searchEvidence() {
      // 搜索功能已通过 computed 实现
    },
    
    resetFilters() {
      this.searchQuery = ''
      this.filterRisk = 'all'
      this.filterType = 'all'
      this.filterStatus = 'all'
    },
    
    toggleSortOrder() {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
    },
    
    toggleSelectAll() {
      if (this.allSelected) {
        this.selectedEvidence = []
      } else {
        this.selectedEvidence = this.filteredEvidence.map(e => e.id)
      }
    },
    
    toggleSelect(id) {
      const index = this.selectedEvidence.indexOf(id)
      if (index > -1) {
        this.selectedEvidence.splice(index, 1)
      } else {
        this.selectedEvidence.push(id)
      }
    },
    
    selectEvidence(id) {
      const index = this.selectedEvidence.indexOf(id)
      if (index > -1) {
        this.selectedEvidence.splice(index, 1)
      } else {
        this.selectedEvidence.push(id)
      }
    },
    
    viewEvidence(evidence) {
      this.selectedEvidenceDetail = evidence
    },
    
    closeModal() {
      this.selectedEvidenceDetail = null
    },
    
    downloadReport(evidence) {
      if (window.$toast) {
        window.$toast.info('📥 下载报告', `正在下载证据 ${evidence.evidence_id} 的取证报告...`)
      }
      // TODO: 实现真实的下载逻辑
    },
    
    viewFullReport(evidence) {
      if (window.$toast) {
        window.$toast.info('📄 查看报告', `正在打开证据 ${evidence.evidence_id} 的完整报告...`)
      }
      // TODO: 实现真实的查看逻辑
    },
    
    exportAllEvidence() {
      console.log('开始导出全部证据...')
      console.log('filteredEvidence:', this.filteredEvidence)
      
      if (this.filteredEvidence.length === 0) {
        this.showCustomAlert('⚠️ 提示', ['暂无证据数据可导出'])
        return
      }
      
      try {
        // 生成CSV格式的导出数据
        const headers = ['证据ID', '文件名', '类型', '风险等级', '风险分数', '检测时间', '状态']
        const rows = this.filteredEvidence.map(evidence => [
          evidence.evidence_id,
          evidence.filename,
          evidence.type,
          this.getRiskLevel(evidence.risk_score),
          evidence.risk_score,
          evidence.timestamp,
          evidence.status || '已完成'
        ])
        
        console.log('CSV Headers:', headers)
        console.log('CSV Rows:', rows)
        
        // 构建CSV内容
        const csvContent = [
          headers.join(','),
          ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
        ].join('\n')
        
        console.log('CSV Content:', csvContent)
        
        // 添加BOM头以支持中文
        const BOM = '\uFEFF'
        const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' })
        
        console.log('Blob created:', blob)
        
        // 创建下载链接
        const link = document.createElement('a')
        const url = URL.createObjectURL(blob)
        const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-')
        
        link.href = url
        link.download = `证据列表_${timestamp}.csv`
        link.style.display = 'none'
        document.body.appendChild(link)
        
        console.log('触发下载...')
        
        // 尝试多种下载方式
        try {
          link.click()
        } catch (e) {
          console.error('link.click() 失败:', e)
          // 备用方案：使用 window.open
          window.open(url, '_blank')
        }
        
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
        
        console.log('导出完成')
        this.showCustomAlert('✅ 导出成功', [`已导出 ${this.filteredEvidence.length} 条证据记录`])
      } catch (error) {
        console.error('导出失败:', error)
        this.showCustomAlert('❌ 导出失败', [error.message])
      }
    },
    
    generateSummary() {
      console.log('开始生成汇总报告...')
      console.log('filteredEvidence:', this.filteredEvidence)
          
      if (this.filteredEvidence.length === 0) {
        this.showCustomAlert('⚠️ 提示', ['暂无证据数据可生成报告'])
        return
      }
          
      try {
        // 统计信息
        const total = this.filteredEvidence.length
        const highRisk = this.filteredEvidence.filter(e => e.risk_score >= 70).length
        const mediumRisk = this.filteredEvidence.filter(e => e.risk_score >= 40 && e.risk_score < 70).length
        const lowRisk = this.filteredEvidence.filter(e => e.risk_score < 40).length
        const avgScore = (this.filteredEvidence.reduce((sum, e) => sum + e.risk_score, 0) / total).toFixed(1)
            
        console.log('统计信息:', { total, highRisk, mediumRisk, lowRisk, avgScore })
            
        // 生成JSON格式的报告
        const report = {
          reportTitle: '取证分析汇总报告',
          generatedAt: new Date().toLocaleString('zh-CN'),
          summary: {
            totalEvidence: total,
            highRiskCount: highRisk,
            mediumRiskCount: mediumRisk,
            lowRiskCount: lowRisk,
            averageRiskScore: avgScore
          },
          evidenceList: this.filteredEvidence.map(e => ({
            evidenceId: e.evidence_id,
            filename: e.filename,
            type: e.type,
            riskLevel: this.getRiskLevel(e.risk_score),
            riskScore: e.risk_score,
            timestamp: e.timestamp
          }))
        }
            
        console.log('Report JSON:', report)
            
        // 下载JSON文件
        const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
        const link = document.createElement('a')
        const url = URL.createObjectURL(blob)
        const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-')
            
        link.href = url
        link.download = `取证汇总报告_${timestamp}.json`
        link.style.display = 'none'
        document.body.appendChild(link)
                
        console.log('触发下载...')
                
        // 尝试多种下载方式
        try {
          link.click()
        } catch (e) {
          console.error('link.click() 失败:', e)
          // 备用方案：使用 window.open
          window.open(url, '_blank')
        }
                
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
                
        console.log('报告生成完成')
        this.showCustomAlert('✅ 报告生成成功', [
          `总证据数: ${total}`,
          `高风险: ${highRisk} | 中风险: ${mediumRisk} | 低风险: ${lowRisk}`,
          `平均风险分: ${avgScore}`
        ])
      } catch (error) {
        console.error('生成报告失败:', error)
        this.showCustomAlert('❌ 生成失败', [error.message])
      }
    },
    
    clearSelected() {
      this.selectedEvidence = []
    },
    
    getFileIcon(type) {
      const icons = {
        image: '🖼️',
        video: '🎬',
        audio: '🎵'
      }
      return icons[type] || '📄'
    },
    
    getRiskClass(score) {
      if (score >= 70) return 'risk-high'
      if (score >= 40) return 'risk-medium'
      return 'risk-low'
    },
    
    getRiskLevel(score) {
      if (score >= 70) return '高风险'
      if (score >= 40) return '中风险'
      return '低风险'
    },
    
    getRiskDescription(score) {
      if (score >= 70) return '检测到明显的伪造痕迹，强烈建议人工复核'
      if (score >= 40) return '存在可疑特征，需要结合其他证据综合判断'
      return '未发现明显异常，证据可信度较高'
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
.forensics-container {
  position: relative;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  /* 移除 overflow: hidden，允许内容滚动 */
}

.page-header {
  position: relative;
  margin-bottom: 1rem;
  padding: 1.25rem 1.5rem;
  flex-shrink: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(0, 212, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.header-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(0, 212, 255, 0.1) 0%, transparent 70%);
  animation: glowRotate 10s linear infinite;
}

@keyframes glowRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.title {
  font-size: 2.8rem;
  font-weight: 800;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #00d4ff 0%, #00ff88 50%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
  position: relative;
  z-index: 1;
}

.subtitle {
  font-size: 1rem;
  color: #94a3b8;
  margin: 0 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 3px;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.header-stats {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
  position: relative;
  z-index: 1;
}

.stat-item {
  padding: 0.5rem 1rem;
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.3);
  border-radius: 8px;
  font-size: 0.9rem;
  color: #00d4ff;
  font-weight: 600;
  transition: all 0.3s;
}

.stat-item:hover {
  background: rgba(0, 212, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 1rem;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.left-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: hidden;
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

.search-input-wrapper {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  color: #e2e8f0;
  font-size: 0.9rem;
}

.search-input:focus {
  outline: none;
  border-color: #00d4ff;
}

.search-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  border: none;
  border-radius: 8px;
  color: #0f172a;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.4);
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-item label {
  font-size: 0.85rem;
  color: #94a3b8;
}

.filter-select {
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  color: #e2e8f0;
  font-size: 0.9rem;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: #00d4ff;
}

.filter-reset-btn {
  width: 100%;
  padding: 0.75rem;
  margin-top: 1rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  color: #94a3b8;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-reset-btn:hover {
  border-color: #00d4ff;
  color: #00d4ff;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.action-btn {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn.primary {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  color: #0f172a;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.4);
}

.action-btn.secondary {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #e2e8f0;
}

.action-btn.secondary:hover {
  border-color: #00d4ff;
}

.action-btn.danger {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.action-btn.danger:hover {
  background: rgba(239, 68, 68, 0.3);
}

.right-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: hidden;
}

.result-count {
  margin-left: auto;
  font-size: 0.85rem;
  color: #94a3b8;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: #e2e8f0;
}

.checkbox-label input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-select {
  padding: 0.5rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 6px;
  color: #e2e8f0;
  font-size: 0.85rem;
  cursor: pointer;
}

.sort-btn {
  padding: 0.5rem 0.75rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 6px;
  color: #94a3b8;
  font-size: 0.85rem;
  cursor: pointer;
}

.sort-btn:hover {
  border-color: #00d4ff;
  color: #00d4ff;
}

.evidence-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  overflow: hidden;
  flex: 1;
}

.evidence-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 10px;
  border: 1px solid rgba(148, 163, 184, 0.1);
  cursor: pointer;
  transition: all 0.3s;
}

.evidence-item:hover {
  background: rgba(15, 23, 42, 0.7);
  border-color: rgba(0, 212, 255, 0.3);
}

.evidence-item.selected {
  background: rgba(0, 212, 255, 0.1);
  border-color: #00d4ff;
}

.evidence-item.risk-high {
  border-left: 3px solid #ef4444;
}

.evidence-item.risk-medium {
  border-left: 3px solid #f59e0b;
}

.evidence-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 1.5rem;
}

.evidence-icon.image {
  background: rgba(16, 185, 129, 0.2);
}

.evidence-icon.video {
  background: rgba(239, 68, 68, 0.2);
}

.evidence-icon.audio {
  background: rgba(139, 92, 246, 0.2);
}

.evidence-info {
  flex: 1;
  min-width: 0;
}

.evidence-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.evidence-filename {
  font-size: 1rem;
  font-weight: 600;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.evidence-risk-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.evidence-risk-badge.risk-high {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.evidence-risk-badge.risk-medium {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.evidence-risk-badge.risk-low {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.evidence-meta {
  display: flex;
  gap: 1.5rem;
}

.meta-item {
  font-size: 0.85rem;
  color: #94a3b8;
}

.view-btn {
  padding: 0.5rem 1rem;
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.3);
  border-radius: 6px;
  color: #00d4ff;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.view-btn:hover {
  background: rgba(0, 212, 255, 0.2);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  color: #64748b;
  margin: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 600px;
  background: rgba(30, 41, 59, 0.95);
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.modal-header h2 {
  font-size: 1.5rem;
  color: #f1f5f9;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  background: rgba(239, 68, 68, 0.2);
  border: none;
  border-radius: 50%;
  color: #ef4444;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s;
}

.close-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}

.modal-body {
  padding: 1.5rem;
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section h3 {
  font-size: 1.1rem;
  color: #f1f5f9;
  margin: 0 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 8px;
}

.detail-label {
  font-size: 0.8rem;
  color: #94a3b8;
}

.detail-item code {
  font-size: 0.85rem;
  color: #00d4ff;
  word-break: break-all;
}

.detail-item span:last-child {
  font-size: 0.9rem;
  color: #e2e8f0;
}

.risk-display {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
  border-radius: 10px;
}

.risk-display.risk-high {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.risk-display.risk-medium {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.risk-display.risk-low {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.risk-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 3px solid;
}

.risk-display.risk-high .risk-circle {
  border-color: #ef4444;
  color: #ef4444;
}

.risk-display.risk-medium .risk-circle {
  border-color: #f59e0b;
  color: #f59e0b;
}

.risk-display.risk-low .risk-circle {
  border-color: #10b981;
  color: #10b981;
}

.risk-value {
  font-size: 1.8rem;
  font-weight: 700;
}

.risk-label {
  font-size: 0.7rem;
  opacity: 0.8;
}

.risk-info h4 {
  font-size: 1.2rem;
  margin: 0 0 0.5rem 0;
}

.risk-display.risk-high .risk-info h4 {
  color: #ef4444;
}

.risk-display.risk-medium .risk-info h4 {
  color: #f59e0b;
}

.risk-display.risk-low .risk-info h4 {
  color: #10b981;
}

.risk-info p {
  font-size: 0.9rem;
  color: #94a3b8;
  margin: 0;
  line-height: 1.4;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.result-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 8px;
}

.result-label {
  font-size: 0.8rem;
  color: #94a3b8;
}

.result-value {
  font-size: 0.9rem;
  color: #e2e8f0;
  font-weight: 600;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.modal-btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.modal-btn.primary {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  color: #0f172a;
}

.modal-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.4);
}

.modal-btn.secondary {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #e2e8f0;
}

.modal-btn.secondary:hover {
  border-color: #00d4ff;
}

@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .left-panel {
    order: 2;
  }
  
  .right-panel {
    order: 1;
  }
}

@media (max-width: 768px) {
  .forensics-container {
    padding: 1rem;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .header-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .evidence-meta {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .detail-grid,
  .result-grid {
    grid-template-columns: 1fr;
  }
  
  .risk-display {
    flex-direction: column;
    text-align: center;
  }
  
  .modal-actions {
    flex-direction: column;
  }
}

/* 自定义提示框样式 */
.alert-fade-enter-active,
.alert-fade-leave-active {
  transition: opacity 0.3s ease;
}

.alert-fade-enter-from,
.alert-fade-leave-to {
  opacity: 0;
}

.custom-alert-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.custom-alert-box {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border: 2px solid rgba(0, 212, 255, 0.3);
  border-radius: 16px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5),
              0 0 30px rgba(0, 212, 255, 0.2);
  animation: alertSlideIn 0.3s ease-out;
}

@keyframes alertSlideIn {
  from {
    transform: translateY(-30px) scale(0.9);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.alert-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(0, 212, 255, 0.2);
}

.alert-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #00D4FF;
}

.alert-close {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  line-height: 1;
  transition: all 0.2s;
}

.alert-close:hover {
  color: #ef4444;
  transform: rotate(90deg);
}

.alert-body {
  padding: 1.25rem 1.5rem;
}

.alert-messages {
  list-style: none;
  margin: 0;
  padding: 0;
}

.alert-messages li {
  color: #cbd5e1;
  font-size: 0.95rem;
  line-height: 1.6;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.alert-messages li:last-child {
  border-bottom: none;
}
</style>