<template>
  <div class="evidence-verify-container">
    <!-- 背景效果 -->
    <div class="bg-grid"></div>
    
    <!-- 顶部标题 -->
    <div class="page-header">
      <h1 class="title">🔐 证据验真中心</h1>
      <p class="subtitle">Evidence Verification & Chain of Custody</p>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 左侧：验证面板 -->
      <div class="left-panel">
        <!-- 证据ID输入卡片 -->
        <div class="card verify-card">
          <div class="card-header">
            <span class="icon animate-pulse">🔍</span>
            <span class="card-title">证据完整性验证</span>
            <span class="badge">VERIFICATION</span>
          </div>
          
          <div class="form-group">
            <label class="form-label">证据ID (Evidence ID)</label>
            <input 
              type="text" 
              v-model="evidenceId"
              placeholder="例如: ev_20260613_xxxxxx"
              class="input-field"
            />
            <p class="input-hint">请输入完整的证据ID进行验证</p>
          </div>

          <div class="form-group">
            <label class="form-label">文件哈希值 (可选)</label>
            <input 
              type="text" 
              v-model="fileHash"
              placeholder="SHA-256 哈希值"
              class="input-field"
            />
            <button class="btn-secondary" @click="calculateFileHash">
              📁 上传文件计算哈希
            </button>
            <input 
              type="file" 
              ref="hashFileInput" 
              style="display: none"
              @change="handleHashFileSelect"
            />
          </div>

          <div class="form-group">
            <label class="form-label required-field">时间戳（验证时间）</label>
            <input
              type="text"
              :value="formattedTimestamp"
              class="input-field readonly-input"
              readonly
            />
            <p class="input-hint">自动记录当前系统时间，不可更改</p>
          </div>

          <button 
            class="verify-btn"
            :disabled="!evidenceId || isVerifying"
            @click="startVerification"
          >
            <span v-if="!isVerifying" class="btn-content">
              <span class="btn-icon">✅</span>
              <span>启动验证</span>
            </span>
            <span v-else class="loading-content">
              <span class="spinner"></span>
              <span>验证中...</span>
            </span>
          </button>
        </div>

        <!-- 快速操作卡片 -->
        <div class="card quick-actions-card">
          <div class="card-header">
            <span class="icon">⚡</span>
            <span class="card-title">快速操作</span>
          </div>
          
          <div class="action-buttons">
            <button class="action-btn" @click="viewAllEvidence">
              <span class="action-icon">📋</span>
              <span>查看所有证据</span>
            </button>
            <button class="action-btn" @click="exportReport">
              <span class="action-icon">📄</span>
              <span>导出 PDF 报告</span>
            </button>
          </div>
        </div>
      </div>

      <!-- 右侧：验证结果 -->
      <div class="right-panel">
        <!-- 空状态 -->
        <div v-if="!verificationResult && !isVerifying" class="empty-state">
          <div class="empty-icon">🛡️</div>
          <h3>等待验证</h3>
          <p>输入证据ID后将在此处显示详细的验证结果</p>
          <div class="features-list">
            <div class="feature-item">✓ SHA-256 哈希校验</div>
            <div class="feature-item">✓ 时间戳一致性验证</div>
            <div class="feature-item">✓ 元数据完整性检查</div>
            <div class="feature-item">✓ 证据链追溯</div>
          </div>
        </div>

        <!-- 验证中 -->
        <div v-if="isVerifying" class="verifying-state">
          <div class="progress-ring-container">
            <svg width="150" height="150" viewBox="0 0 150 150">
              <circle cx="75" cy="75" r="65" fill="none" stroke="#1e293b" stroke-width="8"/>
              <circle 
                cx="75" 
                cy="75" 
                r="65" 
                fill="none" 
                stroke="#10b981" 
                stroke-width="8"
                stroke-dasharray="408"
                :stroke-dashoffset="408 - (408 * progress / 100)"
                transform="rotate(-90 75 75)"
                stroke-linecap="round"
              />
            </svg>
            <div class="progress-text">{{ progress }}%</div>
          </div>
          <p class="progress-status">{{ progressText }}</p>
          
          <!-- 验证步骤指示器 -->
          <div class="verification-steps">
            <div 
              v-for="(step, index) in verificationSteps" 
              :key="index"
              class="step-item"
              :class="getStepClass(index)"
            >
              <div class="step-icon">
                <span v-if="getStepStatus(index) === 'completed'">✅</span>
                <span v-else-if="getStepStatus(index) === 'active'" class="step-spinner"></span>
                <span v-else>⏸️</span>
              </div>
              <div class="step-content">
                <strong class="step-title">{{ step.title }}</strong>
                <p class="step-desc">{{ step.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 验证结果 -->
        <div v-if="verificationResult" class="result-container">
          <!-- 验证状态卡片 -->
          <div class="result-card status-card" :class="getStatusClass()">
            <div class="status-header">
              <div class="status-icon">{{ getStatusIcon() }}</div>
              <div class="status-info">
                <h3 class="status-title">{{ getStatusTitle() }}</h3>
                <p class="status-desc">{{ getStatusDescription() }}</p>
              </div>
            </div>
          </div>

          <!-- 哈希验证详情 -->
          <div class="result-card hash-card" v-if="verificationResult.details.hash_verification">
            <div class="card-title">🔑 SHA-256 哈希验证</div>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">验证状态</span>
                <span class="detail-value" :class="getVerifyStatusClass(verificationResult.details.hash_verification.verified)">
                  {{ verificationResult.details.hash_verification.verified ? '已验证' : '未验证' }}
                </span>
              </div>
              <div class="detail-item">
                <span class="detail-label">哈希匹配</span>
                <span class="detail-value" :class="getMatchStatusClass(verificationResult.details.hash_verification.match)">
                  {{ getMatchText(verificationResult.details.hash_verification.match) }}
                </span>
              </div>
              <div class="detail-item full-width">
                <span class="detail-label">存储哈希</span>
                <code class="hash-code">{{ verificationResult.details.hash_verification.stored_hash || 'N/A' }}</code>
              </div>
              <div class="detail-item full-width" v-if="verificationResult.details.hash_verification.provided_hash">
                <span class="detail-label">提供哈希</span>
                <code class="hash-code">{{ verificationResult.details.hash_verification.provided_hash }}</code>
              </div>
            </div>
          </div>

          <!-- 时间戳验证详情 -->
          <div class="result-card timestamp-card" v-if="verificationResult.details.timestamp_verification">
            <div class="card-title">⏰ 时间戳验证</div>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">验证状态</span>
                <span class="detail-value" :class="getVerifyStatusClass(verificationResult.details.timestamp_verification.verified)">
                  {{ verificationResult.details.timestamp_verification.verified ? '已验证' : '未验证' }}
                </span>
              </div>
              <div class="detail-item">
                <span class="detail-label">时间匹配</span>
                <span class="detail-value" :class="getMatchStatusClass(verificationResult.details.timestamp_verification.match)">
                  {{ getMatchText(verificationResult.details.timestamp_verification.match) }}
                </span>
              </div>
              <div class="detail-item full-width">
                <span class="detail-label">存储时间戳</span>
                <span class="detail-value">{{ formatTimestamp(verificationResult.details.timestamp_verification.stored_timestamp) }}</span>
              </div>
            </div>
          </div>

          <!-- 元数据信息 -->
          <div class="result-card metadata-card" v-if="verificationResult.details.metadata">
            <div class="card-title">📊 证据元数据</div>
            <div class="metadata-grid">
              <div class="metadata-item">
                <span class="metadata-label">原始文件名</span>
                <span class="metadata-value">{{ verificationResult.details.metadata.original_filename || 'N/A' }}</span>
              </div>
              <div class="metadata-item">
                <span class="metadata-label">文件大小</span>
                <span class="metadata-value">{{ formatFileSize(verificationResult.details.metadata.file_size) }}</span>
              </div>
              <div class="metadata-item">
                <span class="metadata-label">检测模型</span>
                <span class="metadata-value">{{ verificationResult.details.metadata.detection_model || 'N/A' }}</span>
              </div>
              <div class="metadata-item">
                <span class="metadata-label">风险评分</span>
                <span class="metadata-value risk-score">{{ verificationResult.details.metadata.risk_score || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <!-- 证据链时间轴 -->
          <div class="result-card timeline-card" v-if="verificationResult.details.evidence_chain">
            <div class="card-title">🔗 证据链追溯</div>
            <div class="evidence-timeline">
              <div 
                v-for="(event, index) in verificationResult.details.evidence_chain" 
                :key="index"
                class="timeline-item"
                :class="getTimelineItemClass(event.type)"
              >
                <div class="timeline-dot"></div>
                <div class="timeline-line" v-if="index < verificationResult.details.evidence_chain.length - 1"></div>
                <div class="timeline-content">
                  <div class="timeline-header">
                    <span class="timeline-icon">{{ getTimelineIcon(event.type) }}</span>
                    <strong class="timeline-title">{{ event.title }}</strong>
                    <span class="timeline-time">{{ formatTimestamp(event.timestamp) }}</span>
                  </div>
                  <p class="timeline-desc">{{ event.description }}</p>
                  <div class="timeline-meta" v-if="event.operator || event.ip">
                    <span v-if="event.operator" class="meta-tag">👤 {{ event.operator }}</span>
                    <span v-if="event.ip" class="meta-tag">🌐 {{ event.ip }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 验证时间 -->
          <div class="result-card verify-time-card">
            <div class="card-title">🕒 验证时间</div>
            <p class="verify-time">{{ new Date(verificationResult.verified_at).toLocaleString('zh-CN') }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 证据列表弹窗 -->
    <transition name="dialog-fade">
      <div v-if="showEvidenceListDialog" class="dialog-overlay" @click.self="closeEvidenceListDialog">
        <div class="dialog-container">
          <div class="dialog-header">
            <h3 class="dialog-title">📋 证据列表</h3>
            <button class="dialog-close" @click="closeEvidenceListDialog">✕</button>
          </div>
          
          <div class="dialog-content">
            <div class="list-summary">
              <span class="summary-text">共找到 <strong>{{ totalEvidence }}</strong> 条证据记录</span>
            </div>
            
            <div class="evidence-table-wrapper">
              <table class="evidence-table">
                <thead>
                  <tr>
                    <th>证据ID</th>
                    <th>文件名</th>
                    <th>检测模型</th>
                    <th>风险评分</th>
                    <th>时间戳</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="evidence in evidenceList" :key="evidence.evidence_id">
                    <td class="id-cell">{{ evidence.evidence_id }}</td>
                    <td class="filename-cell">{{ evidence.filename || 'N/A' }}</td>
                    <td>{{ evidence.model || 'N/A' }}</td>
                    <td>
                      <span class="risk-badge" :class="getRiskClass(evidence.risk_score)">
                        {{ (evidence.risk_score * 100).toFixed(1) }}%
                      </span>
                    </td>
                    <td class="timestamp-cell">{{ formatTimestamp(evidence.timestamp) }}</td>
                    <td>
                      <button class="view-btn" @click="viewEvidenceDetail(evidence.evidence_id)">查看</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div class="dialog-footer">
            <button class="btn-close" @click="closeEvidenceListDialog">关闭</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- 自定义提示弹窗 -->
    <transition name="alert-fade">
      <div v-if="showCustomAlertBox" class="custom-alert-overlay" @click.self="closeCustomAlert">
        <div class="custom-alert-box">
          <div class="alert-header">
            <span class="alert-icon">{{ alertIcon }}</span>
            <h4 class="alert-title">{{ alertTitle }}</h4>
            <button class="alert-close-btn" @click="closeCustomAlert">✕</button>
          </div>
          <div class="alert-body">
            <ul class="alert-list">
              <li v-for="(item, index) in alertMessages" :key="index">{{ item }}</li>
            </ul>
          </div>
          <div class="alert-footer">
            <button class="alert-ok-btn" @click="closeCustomAlert">确定</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { apiRequest } from '../api/config'
export default {
  name: 'EvidenceVerify',
  data() {
    return {
      evidenceId: '',
      fileHash: '',
      timestamp: this.getCurrentDateTime(),
      isVerifying: false,
      progress: 0,
      progressText: '',
      verificationResult: null,
      showEvidenceListDialog: false,
      evidenceList: [],
      totalEvidence: 0,
      showCustomAlertBox: false,
      alertTitle: '',
      alertMessages: [],
      alertIcon: '️',
      currentStep: 0,
      verificationSteps: [
        { title: '查询证据记录', description: '从数据库中检索证据ID对应的记录' },
        { title: '校验 SHA-256 哈希', description: '对比存储哈希与提供哈希的一致性' },
        { title: '验证时间戳一致性', description: '检查证据创建时间与系统时间的合理性' },
        { title: '检查元数据完整性', description: '验证文件名、大小、模型等元数据字段' },
        { title: '生成验证报告', description: '汇总所有验证结果并生成最终报告' }
      ]
    }
  },

  computed: {
    userName() {
      return localStorage.getItem('username') || 'admin'
    },
    formattedTimestamp() {
      if (!this.timestamp) return ''
      const d = new Date(this.timestamp)
      return d.toLocaleString('zh-CN', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: false
      })
    }
  },
  
  methods: {
    async startVerification() {
      this.isVerifying = true
      this.progress = 0
      this.currentStep = 0
      
      const steps = [
        { progress: 20, text: '查询证据数据库...' },
        { progress: 40, text: '验证哈希一致性...' },
        { progress: 60, text: '校验时间戳...' },
        { progress: 80, text: '检查元数据完整性...' },
        { progress: 100, text: '验证完成' }
      ]
      
      for (let i = 0; i < steps.length; i++) {
        const step = steps[i]
        await new Promise(r => setTimeout(r, 400))
        this.progress = step.progress
        this.progressText = step.text
        this.currentStep = i + 1
      }
      
      try {
        const res = await apiRequest('/evidence/verify', {
          method: 'POST',
          body: JSON.stringify({
            evidence_id: this.evidenceId,
            file_hash: this.fileHash || undefined,
            timestamp: this.timestamp || undefined
          })
        })
        
        if (!res.ok) {
          throw new Error(`服务器返回错误: ${res.status}`)
        }
        
        this.verificationResult = await res.json()
      } catch (error) {
        // 如果证据不存在，显示友好的提示
        if (error.message.includes('404')) {
          this.showCustomAlert('⚠️ 未找到该证据ID', [
            '证据ID输入错误',
            '该证据尚未在系统中注册',
            '请先完成检测并生成证据记录'
          ])
        } else {
          this.showCustomAlert('❌ 验证失败', [error.message])
        }
        console.error('验证错误:', error)
      } finally {
        this.isVerifying = false
      }
    },
    
    async calculateFileHash() {
      this.$refs.hashFileInput.click()
    },
    
    handleHashFileSelect(e) {
      const file = e.target.files[0]
      if (!file) return
      
      const formData = new FormData()
      formData.append('file', file)
      
      apiRequest('/evidence/calculate_hash', {
        method: 'POST',
        body: formData
      })
      .then(data => {
        if (data.success) {
          this.fileHash = data.file_hash
          this.showCustomAlert('✅ 哈希计算成功', [`SHA-256: ${data.file_hash.substring(0, 32)}...`])
        } else {
          this.showCustomAlert('❌ 哈希计算失败', [data.message])
        }
      })
      .catch(err => {
        this.showCustomAlert('❌ 请求失败', [err.message])
      })
    },
    
    viewAllEvidence() {
      apiRequest('/evidence/list')
        .then(data => {
          if (data.success) {
            this.showEvidenceListDialog = true
            this.evidenceList = data.evidence_list
            this.totalEvidence = data.total
          } else {
            this.showCustomAlert('❌ 获取证据列表失败', [data.message])
          }
        })
        .catch(err => {
          this.showCustomAlert('❌ 请求失败', [err.message])
        })
    },
    
    exportReport() {
      if (!this.verificationResult) {
        this.showCustomAlert('⚠️ 提示', ['请先完成验证'])
        return
      }

      // 提示用户如何保存为 PDF
      if (window.$toast) {
        window.$toast.info('📄 生成 PDF 报告', '将在新窗口打开打印对话框，请选择“另存为PDF”即可保存')
      }

      const r = this.verificationResult
      const statusText = r.verification_status === 'VERIFIED' ? '验证通过' : '验证失败'
      const statusColor = r.verification_status === 'VERIFIED' ? '#10b981' : '#ef4444'
      const now = new Date()
      const reportTime = now.toLocaleString('zh-CN', { hour12: false })
      const reportId = 'RPT-' + now.getFullYear() + String(now.getMonth()+1).padStart(2,'0') + String(now.getDate()).padStart(2,'0') + '-' + Math.random().toString(36).substring(2, 8).toUpperCase()

      const hashV = r.details?.hash_verification
      const tsV = r.details?.timestamp_verification
      const meta = r.details?.metadata

      const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>证据验真报告 - ${this.evidenceId}</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: "Microsoft YaHei", "PingFang SC", sans-serif; color: #1e293b; background: #fff; padding: 40px 50px; }
  .watermark {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none; z-index: 9999; overflow: hidden;
  }
  .watermark-text {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-25deg);
    font-size: 72px; font-weight: 900; color: rgba(0,0,0,0.04); white-space: nowrap;
    letter-spacing: 8px; user-select: none;
  }
  .header { border-bottom: 3px solid #1e40af; padding-bottom: 20px; margin-bottom: 30px; }
  .header-top { display: flex; justify-content: space-between; align-items: flex-start; }
  .logo { font-size: 24px; font-weight: 800; color: #1e40af; }
  .logo-sub { font-size: 12px; color: #64748b; margin-top: 2px; }
  .report-badge { text-align: right; }
  .report-id { font-size: 11px; color: #64748b; font-family: monospace; }
  .report-title { font-size: 28px; font-weight: 700; color: #0f172a; margin-top: 16px; }
  .report-subtitle { font-size: 13px; color: #64748b; margin-top: 4px; }

  .status-banner { display: flex; align-items: center; gap: 12px; padding: 16px 20px;
    border-radius: 8px; margin-bottom: 28px; border-left: 4px solid ${statusColor};
    background: ${r.verification_status === 'VERIFIED' ? '#f0fdf4' : '#fef2f2'}; }
  .status-dot { width: 16px; height: 16px; border-radius: 50%; background: ${statusColor}; }
  .status-label { font-size: 18px; font-weight: 700; color: ${statusColor}; }
  .status-desc { font-size: 13px; color: #64748b; margin-left: auto; }

  .section { margin-bottom: 24px; }
  .section-title { font-size: 15px; font-weight: 700; color: #1e40af; border-bottom: 1px solid #e2e8f0;
    padding-bottom: 8px; margin-bottom: 12px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 24px; }
  .grid-item { display: flex; justify-content: space-between; padding: 8px 0;
    border-bottom: 1px dotted #e2e8f0; }
  .grid-label { font-size: 12px; color: #64748b; min-width: 100px; }
  .grid-value { font-size: 13px; font-weight: 600; color: #1e293b; text-align: right; word-break: break-all; }
  .grid-value.success { color: #10b981; }
  .grid-value.danger { color: #ef4444; }
  .grid-value.code { font-family: monospace; font-size: 11px; color: #2563eb; }

  .full-row { grid-column: 1 / -1; }

  .footer { margin-top: 36px; padding-top: 16px; border-top: 1px solid #e2e8f0;
    display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; }
  .footer-right { text-align: right; }

  .stamp { position: absolute; right: 50px; top: 280px; }
  .stamp-circle { width: 120px; height: 120px; border: 4px solid ${statusColor}; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; transform: rotate(-15deg);
    opacity: 0.5; }
  .stamp-text { font-size: 16px; font-weight: 900; color: ${statusColor}; text-align: center; line-height: 1.3; }

  @media print {
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    @page { margin: 0; size: A4; }
    .watermark { position: fixed; }
  }
</style>
</head>
<body>
  <div class="watermark">
    <div class="watermark-text">${this.userName} | ${reportTime}</div>
  </div>

  <div class="header">
    <div class="header-top">
      <div>
        <div class="logo">DeepShield</div>
        <div class="logo-sub">数字取证分析平台</div>
      </div>
      <div class="report-badge">
        <div style="font-size:12px;font-weight:600;color:#1e40af;">数字取证证据验真报告</div>
        <div class="report-id">${reportId}</div>
      </div>
    </div>
    <div class="report-title">证据验真报告</div>
    <div class="report-subtitle">Evidence Verification Report | 生成时间: ${reportTime}</div>
  </div>

  <div class="status-banner">
    <div class="status-dot"></div>
    <span class="status-label">${statusText}</span>
    <span class="status-desc">${r.verification_status === 'VERIFIED' ? '证据完整性和真实性已确认，可用于法律取证' : '证据存在异常，建议进一步人工审查'}</span>
  </div>

  <div class="section">
    <div class="section-title">基本信息</div>
    <div class="grid">
      <div class="grid-item"><span class="grid-label">证据ID</span><span class="grid-value code">${this.evidenceId}</span></div>
      <div class="grid-item"><span class="grid-label">验证状态</span><span class="grid-value ${r.verification_status === 'VERIFIED' ? 'success' : 'danger'}">${statusText}</span></div>
      <div class="grid-item"><span class="grid-label">报告编号</span><span class="grid-value code">${reportId}</span></div>
      <div class="grid-item"><span class="grid-label">验证时间</span><span class="grid-value">${reportTime}</span></div>
      <div class="grid-item"><span class="grid-label">操作人员</span><span class="grid-value">${this.userName}</span></div>
      <div class="grid-item"><span class="grid-label">验证时间戳</span><span class="grid-value">${this.formattedTimestamp}</span></div>
    </div>
  </div>

  ${hashV ? `
  <div class="section">
    <div class="section-title">SHA-256 哈希验证</div>
    <div class="grid">
      <div class="grid-item"><span class="grid-label">验证状态</span><span class="grid-value ${hashV.verified ? 'success' : 'danger'}">${hashV.verified ? '已验证' : '未验证'}</span></div>
      <div class="grid-item"><span class="grid-label">哈希匹配</span><span class="grid-value ${hashV.match ? 'success' : 'danger'}">${hashV.match === null ? '未提供' : hashV.match ? '匹配' : '不匹配'}</span></div>
      <div class="grid-item full-row"><span class="grid-label">存储哈希</span><span class="grid-value code">${hashV.stored_hash || 'N/A'}</span></div>
      ${hashV.provided_hash ? `<div class="grid-item full-row"><span class="grid-label">提供哈希</span><span class="grid-value code">${hashV.provided_hash}</span></div>` : ''}
    </div>
  </div>` : ''}

  ${tsV ? `
  <div class="section">
    <div class="section-title">时间戳验证</div>
    <div class="grid">
      <div class="grid-item"><span class="grid-label">验证状态</span><span class="grid-value ${tsV.verified ? 'success' : 'danger'}">${tsV.verified ? '已验证' : '未验证'}</span></div>
      <div class="grid-item"><span class="grid-label">时间匹配</span><span class="grid-value ${tsV.match ? 'success' : 'danger'}">${tsV.match === null ? '未提供' : tsV.match ? '匹配' : '不匹配'}</span></div>
      <div class="grid-item full-row"><span class="grid-label">存储时间戳</span><span class="grid-value">${tsV.stored_timestamp ? new Date(tsV.stored_timestamp).toLocaleString('zh-CN') : 'N/A'}</span></div>
    </div>
  </div>` : ''}

  ${meta ? `
  <div class="section">
    <div class="section-title">证据元数据</div>
    <div class="grid">
      <div class="grid-item"><span class="grid-label">原始文件名</span><span class="grid-value">${meta.original_filename || 'N/A'}</span></div>
      <div class="grid-item"><span class="grid-label">文件大小</span><span class="grid-value">${this.formatFileSize(meta.file_size)}</span></div>
      <div class="grid-item"><span class="grid-label">检测模型</span><span class="grid-value">${meta.detection_model || 'N/A'}</span></div>
      <div class="grid-item"><span class="grid-label">风险评分</span><span class="grid-value">${meta.risk_score || 'N/A'}</span></div>
    </div>
  </div>` : ''}

  <div class="section">
    <div class="section-title">验证说明</div>
    <p style="font-size:12px;color:#475569;line-height:1.8;">
      本报告由 DeepShield 数字取证分析平台自动生成，记录了证据 <strong>${this.evidenceId}</strong> 的完整性验证结果。
      验证过程包含 SHA-256 哈希校验、时间戳一致性验证及元数据完整性检查。
      ${r.verification_status === 'VERIFIED' ? '该证据已通过全部验证项，可作为法律取证依据。' : '该证据存在验证异常项，建议进行人工复查。'}
    </p>
  </div>

  <div class="footer">
    <div class="footer-left">DeepShield 数字取证分析平台 | 本报告由系统自动生成</div>
    <div class="footer-right">操作人: ${this.userName} | ${reportTime}</div>
  </div>
</body>
</html>`

      const printWindow = window.open('', '_blank', 'width=900,height=700')
      if (!printWindow) {
        this.showCustomAlert('⚠️ 提示', ['弹窗被拦截，请允许本站弹窗后重试'])
        return
      }
      printWindow.document.write(html)
      printWindow.document.close()
      printWindow.focus()
      setTimeout(() => {
        printWindow.print()
      }, 500)
    },
    
    getStatusClass() {
      if (!this.verificationResult) return ''
      return this.verificationResult.verification_status === 'VERIFIED' ? 'status-verified' : 'status-failed'
    },
    
    getStatusIcon() {
      if (!this.verificationResult) return ''
      return this.verificationResult.verification_status === 'VERIFIED' ? '✅' : '❌'
    },
    
    getStatusTitle() {
      if (!this.verificationResult) return ''
      return this.verificationResult.verification_status === 'VERIFIED' ? '验证通过' : '验证失败'
    },
    
    getStatusDescription() {
      if (!this.verificationResult) return ''
      return this.verificationResult.verification_status === 'VERIFIED' 
        ? '证据完整性和真实性已确认，可用于法律取证' 
        : '证据存在异常，建议进一步人工审查'
    },
    
    getVerifyStatusClass(verified) {
      return verified ? 'status-success' : 'status-warning'
    },
    
    getMatchStatusClass(match) {
      if (match === null) return 'status-neutral'
      return match ? 'status-success' : 'status-error'
    },
    
    getMatchText(match) {
      if (match === null) return '未提供'
      return match ? '✓ 匹配' : '✗ 不匹配'
    },
    
    // 证据链时间轴辅助方法
    getTimelineItemClass(type) {
      const classMap = {
        'created': 'timeline-created',
        'uploaded': 'timeline-uploaded',
        'detected': 'timeline-detected',
        'verified': 'timeline-verified',
        'exported': 'timeline-exported',
        'accessed': 'timeline-accessed'
      }
      return classMap[type] || ''
    },
    
    getTimelineIcon(type) {
      const iconMap = {
        'created': '📝',
        'uploaded': '⬆️',
        'detected': '🔍',
        'verified': '✅',
        'exported': '📥',
        'accessed': '👁️'
      }
      return iconMap[type] || '📌'
    },
    
    // 验证步骤辅助方法
    getStepStatus(index) {
      if (index < this.currentStep) return 'completed'
      if (index === this.currentStep) return 'active'
      return 'pending'
    },
    
    getStepClass(index) {
      const status = this.getStepStatus(index)
      return `step-${status}`
    },
    
    formatTimestamp(ts) {
      if (!ts) return 'N/A'
      return new Date(ts).toLocaleString('zh-CN')
    },
    
    // 获取当前日期时间（格式：YYYY-MM-DDTHH:mm:ss）
    getCurrentDateTime() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')
      return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`
    },
    
    formatFileSize(bytes) {
      if (!bytes) return 'N/A'
      if (bytes < 1024) return bytes + ' B'
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
      return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
    },
    
    closeEvidenceListDialog() {
      this.showEvidenceListDialog = false
      this.evidenceList = []
      this.totalEvidence = 0
    },
    
    viewEvidenceDetail(evidenceId) {
      this.closeEvidenceListDialog()
      this.evidenceId = evidenceId
      // 自动触发验证
      this.$nextTick(() => {
        this.startVerification()
      })
    },
    
    getRiskClass(riskScore) {
      if (!riskScore) return 'risk-neutral'
      if (riskScore >= 0.8) return 'risk-high'
      if (riskScore >= 0.5) return 'risk-medium'
      return 'risk-low'
    },
    
    showCustomAlert(title, messages) {
      this.alertTitle = title
      this.alertMessages = Array.isArray(messages) ? messages : [messages]
      this.showCustomAlertBox = true
      
      // 根据标题设置图标
      if (title.includes('✅')) {
        this.alertIcon = '✅'
      } else if (title.includes('❌')) {
        this.alertIcon = '❌'
      } else if (title.includes('⚠️')) {
        this.alertIcon = '️'
      } else {
        this.alertIcon = 'ℹ️'
      }
    },
    
    closeCustomAlert() {
      this.showCustomAlertBox = false
      this.alertTitle = ''
      this.alertMessages = []
      this.alertIcon = '️'
    }
  }
}
</script>

<style scoped>
/* 容器 */
.evidence-verify-container {
  position: relative;
  padding: 2rem;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f172a 100%);
  min-height: 100vh;
  color: #e2e8f0;
}

.bg-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  background-image: 
    linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* 头部 */
.page-header {
  margin-bottom: 2.5rem;
  padding: 2rem;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(16, 185, 129, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.title {
  font-size: 2.8rem;
  font-weight: 800;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #10b981 0%, #00d4ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1rem;
  color: #94a3b8;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 3px;
}

/* 主内容 */
.main-content {
  display: grid;
  grid-template-columns: 450px 1fr;
  gap: 2rem;
}

.left-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 卡片 */
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

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #f1f5f9;
}

.badge {
  margin-left: auto;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  border-radius: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 表单 */
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  color: #cbd5e1;
  margin-bottom: 0.5rem;
}

.input-field {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  background: rgba(15, 23, 42, 0.6);
  color: #f1f5f9;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.input-hint {
  font-size: 0.75rem;
  color: #64748b;
  margin: 0.5rem 0 0 0;
}

/* 日期时间输入框包装器 */
.datetime-input-wrapper {
  position: relative;
  width: 100%;
}

.datetime-input {
  padding-right: 3rem;
}

.calendar-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  pointer-events: none;
  opacity: 0.8;
}

.btn-secondary {
  margin-top: 0.5rem;
  padding: 0.6rem 1rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 8px;
  color: #10b981;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
}

.btn-secondary:hover {
  background: rgba(16, 185, 129, 0.2);
}

/* 验证按钮 */
.verify-btn {
  width: 100%;
  padding: 1.2rem;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #64748b, #475569);
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: not-allowed;
  transition: all 0.3s;
}

.verify-btn:not(:disabled) {
  background: linear-gradient(135deg, #10b981, #059669);
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
}

.verify-btn:not(:disabled):hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5);
}

.btn-content, .loading-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 快速操作 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.action-btn {
  padding: 1rem;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 8px;
  color: #a78bfa;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.action-btn:hover {
  background: rgba(139, 92, 246, 0.2);
  transform: translateX(5px);
}

.action-icon {
  font-size: 1.2rem;
}

/* 右侧面板 */
.right-panel {
  min-height: 600px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 3rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 16px;
  border: 2px dashed rgba(148, 163, 184, 0.2);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #94a3b8;
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  color: #64748b;
  margin: 0 0 1.5rem 0;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.feature-item {
  padding: 0.5rem 1rem;
  background: rgba(16, 185, 129, 0.1);
  border-left: 3px solid #10b981;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #10b981;
}

/* 验证中状态 */
.verifying-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 3rem;
}

.progress-ring-container {
  position: relative;
  margin-bottom: 2rem;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2rem;
  font-weight: 700;
  color: #10b981;
}

.progress-status {
  font-size: 1.1rem;
  color: #94a3b8;
  margin: 0;
  animation: fadeInOut 2s infinite;
}

@keyframes fadeInOut {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

/* 结果卡片 */
.result-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.result-card {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.1);
  padding: 1.5rem;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #f1f5f9;
  margin: 0 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

/* 状态卡片 */
.status-card {
  border: 2px solid;
}

.status-card.status-verified {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.status-card.status-failed {
  border-color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.status-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.status-icon {
  font-size: 3rem;
}

.status-title {
  font-size: 1.5rem;
  margin: 0 0 0.5rem 0;
  color: #f1f5f9;
}

.status-desc {
  font-size: 0.9rem;
  color: #94a3b8;
  margin: 0;
}

/* 详情网格 */
.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-label {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
}

.detail-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #f1f5f9;
}

.status-success { color: #10b981; }
.status-error { color: #ef4444; }
.status-warning { color: #f59e0b; }
.status-neutral { color: #64748b; }

.hash-code {
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  background: rgba(15, 23, 42, 0.6);
  padding: 0.5rem;
  border-radius: 4px;
  color: #00d4ff;
  word-break: break-all;
}

/* 元数据网格 */
.metadata-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.metadata-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metadata-label {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
}

.metadata-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #f1f5f9;
}

.metadata-value.risk-score {
  color: #f59e0b;
  font-size: 1.2rem;
}

.verify-time {
  font-size: 1rem;
  color: #00d4ff;
  margin: 0;
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

/* 弹窗样式 */
.dialog-overlay {
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

.dialog-container {
  background: #141C2F;
  border-radius: 16px;
  border: 1px solid rgba(0, 212, 255, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  width: 90%;
  max-width: 1000px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(0, 212, 255, 0.1);
  background: rgba(0, 212, 255, 0.03);
}

.dialog-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0;
}

.dialog-close {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 50%;
  color: #ef4444;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dialog-close:hover {
  background: rgba(239, 68, 68, 0.2);
  transform: rotate(90deg);
}

.dialog-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.list-summary {
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(0, 212, 255, 0.05);
  border-left: 3px solid #00D4FF;
  border-radius: 4px;
}

.summary-text {
  font-size: 0.9rem;
  color: #94a3b8;
}

.summary-text strong {
  color: #00D4FF;
  font-size: 1.1rem;
}

.evidence-table-wrapper {
  overflow-x: auto;
}

.evidence-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.evidence-table thead {
  background: rgba(0, 212, 255, 0.08);
}

.evidence-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  border-bottom: 2px solid rgba(0, 212, 255, 0.1);
}

.evidence-table tbody tr {
  border-bottom: 1px solid rgba(0, 212, 255, 0.05);
  transition: background 0.3s;
}

.evidence-table tbody tr:hover {
  background: rgba(0, 212, 255, 0.05);
}

.evidence-table td {
  padding: 0.75rem 1rem;
  color: #e2e8f0;
}

.id-cell {
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  color: #00D4FF;
}

.filename-cell {
  font-weight: 500;
  color: #f1f5f9;
}

.timestamp-cell {
  font-size: 0.8rem;
  color: #94a3b8;
}

.risk-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.risk-high {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.risk-medium {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.risk-low {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.risk-neutral {
  background: rgba(100, 116, 139, 0.15);
  color: #64748b;
  border: 1px solid rgba(100, 116, 139, 0.3);
}

.view-btn {
  padding: 0.4rem 0.8rem;
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.3);
  border-radius: 6px;
  color: #00D4FF;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.view-btn:hover {
  background: rgba(0, 212, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
}

.dialog-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(0, 212, 255, 0.1);
  background: rgba(0, 212, 255, 0.03);
  display: flex;
  justify-content: flex-end;
}

.btn-close {
  padding: 0.6rem 1.5rem;
  background: rgba(100, 116, 139, 0.2);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 8px;
  color: #94a3b8;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-close:hover {
  background: rgba(100, 116, 139, 0.3);
  color: #f1f5f9;
}

/* 弹窗动画 */
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.3s ease;
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}

.dialog-fade-enter-active .dialog-container,
.dialog-fade-leave-active .dialog-container {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.dialog-fade-enter-from .dialog-container,
.dialog-fade-leave-to .dialog-container {
  transform: scale(0.9);
  opacity: 0;
}

/* 自定义提示弹窗样式 */
.custom-alert-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}

.custom-alert-box {
  background: #141C2F;
  border-radius: 12px;
  border: 1px solid rgba(0, 212, 255, 0.2);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  width: 90%;
  max-width: 450px;
  overflow: hidden;
}

.alert-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(0, 212, 255, 0.1);
  background: rgba(0, 212, 255, 0.03);
}

.alert-icon {
  font-size: 1.5rem;
}

.alert-title {
  flex: 1;
  font-size: 1rem;
  font-weight: 600;
  color: #f1f5f9;
  margin: 0;
}

.alert-close-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 50%;
  color: #ef4444;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.alert-close-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.alert-body {
  padding: 1.25rem;
}

.alert-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.alert-list li {
  padding: 0.5rem 0;
  color: #e2e8f0;
  font-size: 0.9rem;
  line-height: 1.5;
  border-bottom: 1px solid rgba(0, 212, 255, 0.05);
}

.alert-list li:last-child {
  border-bottom: none;
}

.alert-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid rgba(0, 212, 255, 0.1);
  background: rgba(0, 212, 255, 0.03);
  display: flex;
  justify-content: flex-end;
}

.alert-ok-btn {
  padding: 0.6rem 2rem;
  background: linear-gradient(135deg, #00D4FF, #0099cc);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.alert-ok-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
}

/* 弹窗动画 */
.alert-fade-enter-active,
.alert-fade-leave-active {
  transition: opacity 0.3s ease;
}

.alert-fade-enter-from,
.alert-fade-leave-to {
  opacity: 0;
}

/* 时间戳只读样式 */
.required-field::after {
  content: ' *';
  color: #ef4444;
  font-weight: 700;
}

.readonly-input {
  cursor: default;
  /* 使用与其他输入框相同的背景色 */
  background: rgba(15, 23, 42, 0.6) !important;
  /* 使用与其他输入框相同的边框色 */
  border-color: rgba(148, 163, 184, 0.2) !important;
  /* 移除额外 padding，保持与其他输入框宽度一致 */
  padding-right: 0.75rem !important;
}

.readonly-input:focus {
  border-color: rgba(148, 163, 184, 0.2) !important;
  box-shadow: none !important;
}

/* 证据链时间轴样式 */
.timeline-card {
  padding: 1.5rem;
}

.evidence-timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline-item {
  position: relative;
  padding-bottom: 2rem;
  animation: fadeInUp 0.5s ease forwards;
  opacity: 0;
}

.timeline-item:nth-child(1) { animation-delay: 0.1s; }
.timeline-item:nth-child(2) { animation-delay: 0.2s; }
.timeline-item:nth-child(3) { animation-delay: 0.3s; }
.timeline-item:nth-child(4) { animation-delay: 0.4s; }
.timeline-item:nth-child(5) { animation-delay: 0.5s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.timeline-dot {
  position: absolute;
  left: -2rem;
  top: 0.25rem;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3b82f6;
  border: 3px solid rgba(59, 130, 246, 0.3);
  z-index: 2;
  transition: all 0.3s ease;
}

.timeline-item:hover .timeline-dot {
  transform: scale(1.3);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

.timeline-created .timeline-dot { background: #10b981; border-color: rgba(16, 185, 129, 0.3); }
.timeline-uploaded .timeline-dot { background: #3b82f6; border-color: rgba(59, 130, 246, 0.3); }
.timeline-detected .timeline-dot { background: #f59e0b; border-color: rgba(245, 158, 11, 0.3); }
.timeline-verified .timeline-dot { background: #10b981; border-color: rgba(16, 185, 129, 0.3); }
.timeline-exported .timeline-dot { background: #8b5cf6; border-color: rgba(139, 92, 246, 0.3); }
.timeline-accessed .timeline-dot { background: #64748b; border-color: rgba(100, 116, 139, 0.3); }

.timeline-line {
  position: absolute;
  left: calc(-2rem + 7px);
  top: 1.25rem;
  width: 2px;
  height: calc(100% - 1rem);
  background: linear-gradient(to bottom, rgba(148, 163, 184, 0.3), transparent);
  z-index: 1;
}

.timeline-content {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 10px;
  padding: 1rem 1.25rem;
  transition: all 0.3s ease;
}

.timeline-item:hover .timeline-content {
  background: rgba(15, 23, 42, 0.6);
  border-color: rgba(148, 163, 184, 0.3);
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.timeline-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.timeline-icon {
  font-size: 1.25rem;
}

.timeline-title {
  font-size: 0.95rem;
  color: #f1f5f9;
  font-weight: 600;
}

.timeline-time {
  font-size: 0.8rem;
  color: #64748b;
  margin-left: auto;
  font-family: 'Courier New', monospace;
}

.timeline-desc {
  font-size: 0.85rem;
  color: #94a3b8;
  line-height: 1.6;
  margin: 0.5rem 0;
}

.timeline-meta {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.75rem;
  flex-wrap: wrap;
}

.meta-tag {
  font-size: 0.75rem;
  color: #cbd5e1;
  background: rgba(148, 163, 184, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.15);
}

@media (max-width: 768px) {
  .timeline-time {
    margin-left: 0;
    width: 100%;
    order: 3;
  }
}

/* 验证步骤指示器样式 */
.verification-steps {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 10px;
  transition: all 0.3s ease;
  opacity: 0.6;
}

.step-item:hover {
  background: rgba(15, 23, 42, 0.6);
  transform: translateX(4px);
}

.step-completed {
  opacity: 1;
  border-color: rgba(16, 185, 129, 0.4);
  background: rgba(16, 185, 129, 0.05);
}

.step-active {
  opacity: 1;
  border-color: rgba(59, 130, 246, 0.5);
  background: rgba(59, 130, 246, 0.08);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.15);
}

.step-pending {
  opacity: 0.5;
}

.step-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(59, 130, 246, 0.3);
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.step-content {
  flex: 1;
  min-width: 0;
}

.step-title {
  font-size: 0.95rem;
  color: #f1f5f9;
  font-weight: 600;
  display: block;
  margin-bottom: 0.25rem;
}

.step-desc {
  font-size: 0.8rem;
  color: #94a3b8;
  line-height: 1.5;
  margin: 0;
}

@media (max-width: 768px) {
  .verification-steps {
    max-width: 100%;
  }
  
  .step-item {
    padding: 0.75rem;
  }
}
</style>
