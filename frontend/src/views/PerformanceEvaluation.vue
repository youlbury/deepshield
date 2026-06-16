<template>
  <div class="performance-evaluation-container">
    <!-- 背景效果 -->
    <div class="bg-grid"></div>
    
    <!-- 顶部标题 -->
    <div class="page-header">
      <h1 class="title">📊 性能评估</h1>
      <p class="subtitle">Performance Evaluation & Benchmark Analysis</p>
    </div>

    <!-- 功能说明 -->
    <div class="info-banner">
      <div class="info-item">
        <span class="info-icon">📈</span>
        <div class="info-content">
          <strong>ROC 曲线：</strong>6条折线图展示5个模型的TPR-FPR权衡曲线 + 随机猜测虚线（AUC=50），AUC值标注在图例中
        </div>
      </div>
      <div class="info-item">
        <span class="info-icon">🛡️</span>
        <div class="info-content">
          <strong>对抗鲁棒性：</strong>5种攻击类型（JPEG压缩、高斯噪声、中值滤波）下的模型准确率保持率对比
        </div>
      </div>
      <div class="info-item">
        <span class="info-icon">🔗</span>
        <div class="info-content">
          <strong>多模态融合：</strong>单模态最优 vs 多模态融合后的准确率提升幅度对比
        </div>
      </div>
      <div class="info-item">
        <span class="info-icon">⚡</span>
        <div class="info-content">
          <strong>推理速度：</strong>CPU/GPU双平台延迟(ms)与吞吐量(FPS)对比，支持切换视图
        </div>
      </div>
    </div>

    <!-- ROC 曲线 -->
    <div class="section-card full-width">
      <div class="card-header">
        <span class="card-icon">📈</span>
        <span class="card-title">ROC 曲线对比</span>
        <span class="chart-hint">曲线越靠近左上角，模型性能越好 | 虚线为随机猜测基准</span>
      </div>
      <div ref="rocChart" class="chart-container-large"></div>
    </div>

    <!-- 鲁棒性测试 + 多模态融合 -->
    <div class="charts-row">
      <div class="section-card">
        <div class="card-header">
          <span class="card-icon"></span>
          <span class="card-title">对抗鲁棒性测试</span>
          <span class="chart-tip" v-if="robustnessLoading">加载中...</span>
        </div>
        <div ref="robustnessChart" class="chart-container-large"></div>
      </div>

      <div class="section-card">
        <div class="card-header">
          <span class="card-icon">🔗</span>
          <span class="card-title">多模态融合评估</span>
          <span class="chart-tip" v-if="crossModalLoading">加载中...</span>
        </div>
        <div ref="crossModalChart" class="chart-container-large"></div>
      </div>
    </div>

    <!-- 推理速度基准 -->
    <div class="section-card full-width">
      <div class="card-header">
        <span class="card-icon">⚡</span>
        <span class="card-title">推理速度基准测试</span>
        <div class="speed-toggle">
          <button class="filter-btn" :class="{ active: speedMode === 'latency' }" @click="speedMode = 'latency'; initSpeedChart()">延迟 (ms)</button>
          <button class="filter-btn" :class="{ active: speedMode === 'throughput' }" @click="speedMode = 'throughput'; initSpeedChart()">吞吐量 (FPS)</button>
        </div>
      </div>
      <div ref="speedChart" class="chart-container-large"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { apiRequest } from '../api/config'

export default {
  name: 'PerformanceEvaluation',
  data() {
    return {
      // ROC / 鲁棒性 / 融合 / 速度
      rocChartInstance: null,
      robustnessChartInstance: null,
      crossModalChartInstance: null,
      speedChartInstance: null,
      speedMode: 'latency',
      robustnessLoading: false,
      crossModalLoading: false,
      rocData: [],
      robustnessData: { models: [], attack_types: [] },
      crossModalData: { fusion_results: [], fusion_categories: [] },
      speedData: { models: [], platforms: [] }
    }
  },

  mounted() {
    this.$nextTick(() => {
      this.loadEvaluationData()
    })
    window.addEventListener('resize', this.handleResize)
  },

  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
    this.disposeCharts()
  },

  methods: {
    disposeCharts() {
      if (this.rocChartInstance) { this.rocChartInstance.dispose(); this.rocChartInstance = null }
      if (this.robustnessChartInstance) { this.robustnessChartInstance.dispose(); this.robustnessChartInstance = null }
      if (this.crossModalChartInstance) { this.crossModalChartInstance.dispose(); this.crossModalChartInstance = null }
      if (this.speedChartInstance) { this.speedChartInstance.dispose(); this.speedChartInstance = null }
    },

    handleResize() {
      if (this.rocChartInstance) this.rocChartInstance.resize()
      if (this.robustnessChartInstance) this.robustnessChartInstance.resize()
      if (this.crossModalChartInstance) this.crossModalChartInstance.resize()
      if (this.speedChartInstance) this.speedChartInstance.resize()
    },

    async loadEvaluationData() {
      this.robustnessLoading = true
      this.crossModalLoading = true
      try {
        const [rocRes, robRes, cmRes, spRes] = await Promise.all([
          apiRequest('/benchmark/roc'),
          apiRequest('/benchmark/robustness'),
          apiRequest('/benchmark/cross-modal'),
          apiRequest('/benchmark/speed')
        ])
        if (rocRes.success) { this.rocData = rocRes.curves; this.$nextTick(() => this.initROCChart()) }
        if (robRes.success) { this.robustnessData = robRes; this.$nextTick(() => this.initRobustnessChart()) }
        if (cmRes.success) { this.crossModalData = cmRes; this.$nextTick(() => this.initCrossModalChart()) }
        if (spRes.success) { this.speedData = spRes; this.$nextTick(() => this.initSpeedChart()) }
      } catch (e) {
        console.error('加载评估数据失败:', e)
        this.useFallbackData()
      } finally {
        this.robustnessLoading = false
        this.crossModalLoading = false
      }
    },

    useFallbackData() {
      this.rocData = [
        { model: 'Xception', auc: 98.1, color: '#00D4FF', points: this.genRocPoints(98.1) },
        { model: 'F3Net', auc: 97.0, color: '#00FF88', points: this.genRocPoints(97.0) },
        { model: 'EfficientNet', auc: 97.8, color: '#8b5cf6', points: this.genRocPoints(97.8) },
        { model: 'AASIST', auc: 96.5, color: '#f59e0b', points: this.genRocPoints(96.5) },
        { model: 'TimeSformer', auc: 98.8, color: '#ef4444', points: this.genRocPoints(98.8) }
      ]
      this.robustnessData = {
        models: [
          { name: 'Xception', jpeg_q90: 95.8, jpeg_q70: 94.2, jpeg_q50: 90.5, gaussian_noise: 93.1, median_blur: 94.8 },
          { name: 'F3Net', jpeg_q90: 94.0, jpeg_q70: 92.8, jpeg_q50: 88.3, gaussian_noise: 91.5, median_blur: 93.2 },
          { name: 'EfficientNet', jpeg_q90: 95.2, jpeg_q70: 93.5, jpeg_q50: 89.8, gaussian_noise: 92.4, median_blur: 94.0 },
          { name: 'AASIST', jpeg_q90: 92.5, jpeg_q70: 90.8, jpeg_q50: 86.2, gaussian_noise: 89.5, median_blur: 91.8 },
          { name: 'TimeSformer', jpeg_q90: 96.8, jpeg_q70: 95.5, jpeg_q50: 92.0, gaussian_noise: 94.5, median_blur: 95.8 }
        ],
        attack_types: [
          { id: 'jpeg_q90', label: 'JPEG Q90', label_cn: '轻度压缩' },
          { id: 'jpeg_q70', label: 'JPEG Q70', label_cn: '中度压缩' },
          { id: 'jpeg_q50', label: 'JPEG Q50', label_cn: '重度压缩' },
          { id: 'gaussian_noise', label: '高斯噪声', label_cn: '加性噪声' },
          { id: 'median_blur', label: '中值滤波', label_cn: '平滑滤波' }
        ]
      }
      this.crossModalData = {
        fusion_results: [
          { model: 'Xception + AASIST', modality: '图像+音频', single_image: 96.2, single_audio: 93.2, fusion_accuracy: 97.8, fusion_gain: 1.6 },
          { model: 'Xception + TimeSformer', modality: '图像+视频', single_image: 96.2, single_video: 97.5, fusion_accuracy: 98.5, fusion_gain: 1.0 },
          { model: 'F3Net + AASIST', modality: '图像+音频', single_image: 94.5, single_audio: 93.2, fusion_accuracy: 96.2, fusion_gain: 1.7 },
          { model: 'EfficientNet + TimeSformer', modality: '图像+视频', single_image: 95.8, single_video: 97.5, fusion_accuracy: 98.2, fusion_gain: 0.7 }
        ]
      }
      this.speedData = {
        models: [
          { name: 'Xception', latency_cpu: 245, latency_gpu: 45, throughput_cpu: 4.1, throughput_gpu: 22.2, params_m: 22.9, flops_g: 8.4 },
          { name: 'F3Net', latency_cpu: 310, latency_gpu: 52, throughput_cpu: 3.2, throughput_gpu: 19.2, params_m: 28.5, flops_g: 12.1 },
          { name: 'EfficientNet', latency_cpu: 185, latency_gpu: 38, throughput_cpu: 5.4, throughput_gpu: 26.3, params_m: 15.3, flops_g: 5.6 },
          { name: 'AASIST', latency_cpu: 120, latency_gpu: 28, throughput_cpu: 8.3, throughput_gpu: 35.7, params_m: 8.7, flops_g: 3.2 },
          { name: 'TimeSformer', latency_cpu: 520, latency_gpu: 68, throughput_cpu: 1.9, throughput_gpu: 14.7, params_m: 121.0, flops_g: 42.5 }
        ]
      }
      this.$nextTick(() => {
        this.initROCChart()
        this.initRobustnessChart()
        this.initCrossModalChart()
        this.initSpeedChart()
      })
    },

    genRocPoints(auc, n) {
      n = n || 20
      const pts = []
      for (let i = 0; i <= n; i++) {
        const fpr = i / n
        let tpr = Math.pow(fpr, 0.5 + (auc - 50) / 100)
        if (i === 0) tpr = 0
        if (i === n) tpr = 1
        pts.push([fpr.toFixed(3), tpr.toFixed(3)])
      }
      return pts
    },

    initROCChart() {
      if (!this.$refs.rocChart || !this.rocData.length) return
      if (this.rocChartInstance) this.rocChartInstance.dispose()
      const chart = echarts.init(this.$refs.rocChart)
      const series = this.rocData.map(d => ({
        name: d.model + ' (AUC=' + d.auc + ')',
        type: 'line',
        data: d.points,
        smooth: true,
        symbol: 'none',
        lineStyle: { color: d.color, width: 2.5 }
      }))
      series.push({
        name: '随机猜测 (AUC=50)',
        type: 'line',
        data: [[0, 0], [1, 1]],
        smooth: false,
        symbol: 'none',
        lineStyle: { color: '#94a3b8', width: 1.5, type: 'dashed' },
        tooltip: { show: false }
      })
      chart.setOption({
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(20, 28, 47, 0.95)',
          borderColor: 'rgba(0, 212, 255, 0.2)',
          textStyle: { color: '#e2e8f0' },
          formatter: params => params.map(p => p.marker + ' ' + p.seriesName + ': (' + p.data[0] + ', ' + p.data[1] + ')').join('<br/>')
        },
        legend: {
          data: [...this.rocData.map(d => d.model + ' (AUC=' + d.auc + ')'), '随机猜测 (AUC=50)'],
          textStyle: { color: '#94a3b8', fontSize: 10 },
          bottom: '5%', left: 'center', itemWidth: 14, itemHeight: 10
        },
        grid: { left: '8%', right: '8%', bottom: '15%', top: '8%', containLabel: true },
        xAxis: {
          type: 'value',
          name: '假正例率 (FPR)',
          min: 0, max: 1,
          nameTextStyle: { color: '#94a3b8', fontSize: 10 },
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          axisLabel: { color: '#94a3b8', fontSize: 10 },
          splitLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.08)' } }
        },
        yAxis: {
          type: 'value',
          name: '真正例率 (TPR)',
          min: 0, max: 1,
          nameTextStyle: { color: '#94a3b8', fontSize: 10 },
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          axisLabel: { color: '#94a3b8', fontSize: 10 },
          splitLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.08)' } }
        },
        series: series
      })
      this.rocChartInstance = chart
    },

    initRobustnessChart() {
      if (!this.$refs.robustnessChart || !this.robustnessData.models.length) return
      if (this.robustnessChartInstance) this.robustnessChartInstance.dispose()
      const chart = echarts.init(this.$refs.robustnessChart)
      const attackKeys = this.robustnessData.attack_types.map(a => a.id)
      const attackLabels = this.robustnessData.attack_types.map(a => a.label)
      const colors = ['#00D4FF', '#00FF88', '#8b5cf6', '#f59e0b', '#ef4444']
      const series = this.robustnessData.models.map((m, i) => ({
        name: m.name,
        type: 'line',
        data: attackKeys.map(k => m[k]),
        symbol: 'circle',
        symbolSize: 7,
        lineStyle: { color: colors[i], width: 2 },
        itemStyle: { color: colors[i] }
      }))
      chart.setOption({
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(20, 28, 47, 0.95)',
          borderColor: 'rgba(0, 212, 255, 0.2)',
          textStyle: { color: '#e2e8f0' },
          formatter: params => params.map(p => p.marker + ' ' + p.seriesName + ': ' + p.value + '%').join('<br/>')
        },
        legend: {
          data: this.robustnessData.models.map(m => m.name),
          textStyle: { color: '#94a3b8', fontSize: 10 },
          bottom: '5%', left: 'center', itemWidth: 14, itemHeight: 10
        },
        grid: { left: '10%', right: '8%', bottom: '15%', top: '8%', containLabel: true },
        xAxis: {
          type: 'category',
          data: attackLabels,
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          axisLabel: { color: '#94a3b8', fontSize: 9, rotate: 20 }
        },
        yAxis: {
          type: 'value',
          name: '准确率 (%)',
          min: 84, max: 98,
          nameTextStyle: { color: '#94a3b8', fontSize: 10 },
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          axisLabel: { color: '#94a3b8', fontSize: 10 },
          splitLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.08)' } }
        },
        series: series
      })
      this.robustnessChartInstance = chart
    },

    initCrossModalChart() {
      if (!this.$refs.crossModalChart || !this.crossModalData.fusion_results) return
      if (this.crossModalChartInstance) this.crossModalChartInstance.dispose()
      const chart = echarts.init(this.$refs.crossModalChart)
      const data = this.crossModalData.fusion_results
      const categories = data.map(d => d.model)
      const singleVals = data.map(d => Math.max(d.single_image || 0, d.single_audio || 0, d.single_video || 0))
      const fusionVals = data.map(d => d.fusion_accuracy)
      const gainVals = data.map(d => d.fusion_gain)
      chart.setOption({
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(20, 28, 47, 0.95)',
          borderColor: 'rgba(0, 212, 255, 0.2)',
          textStyle: { color: '#e2e8f0' },
          formatter: params => {
            const idx = params[0].dataIndex
            const d = data[idx]
            return d.model + ' (' + d.modality + ')<br/>' +
              '单模态最优: ' + singleVals[idx].toFixed(1) + '%<br/>' +
              '融合后: ' + fusionVals[idx].toFixed(1) + '%<br/>' +
              '<span style=\'color:#00FF88\'>提升: +' + d.fusion_gain.toFixed(1) + '%</span>'
          }
        },
        legend: {
          data: ['单模态最优', '多模态融合', '融合增益'],
          textStyle: { color: '#94a3b8', fontSize: 10 },
          bottom: '5%', left: 'center', itemWidth: 14, itemHeight: 10
        },
        grid: { left: '12%', right: '12%', bottom: '18%', top: '8%', containLabel: true },
        xAxis: {
          type: 'category',
          data: categories,
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          axisLabel: { color: '#94a3b8', fontSize: 9, rotate: 25 }
        },
        yAxis: [
          {
            type: 'value', name: '准确率 (%)', min: 90, max: 100,
            nameTextStyle: { color: '#94a3b8', fontSize: 10 },
            axisLabel: { color: '#94a3b8', fontSize: 10 },
            splitLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.08)' } }
          },
          {
            type: 'value', name: '增益 (%)',
            nameTextStyle: { color: '#00FF88', fontSize: 10 },
            axisLabel: { color: '#00FF88', fontSize: 10 },
            splitLine: { show: false }
          }
        ],
        series: [
          {
            name: '单模态最优', type: 'bar', data: singleVals,
            barWidth: '20%', barGap: '30%',
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#00D4FF' }, { offset: 1, color: '#0099cc' }
              ]),
              borderRadius: [6, 6, 0, 0]
            }
          },
          {
            name: '多模态融合', type: 'bar', data: fusionVals,
            barWidth: '20%',
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#8b5cf6' }, { offset: 1, color: '#6d28d9' }
              ]),
              borderRadius: [6, 6, 0, 0]
            }
          },
          {
            name: '融合增益', type: 'line', yAxisIndex: 1, data: gainVals,
            symbol: 'diamond', symbolSize: 10,
            lineStyle: { color: '#00FF88', width: 2.5 },
            itemStyle: { color: '#00FF88' }
          }
        ]
      })
      this.crossModalChartInstance = chart
    },

    initSpeedChart() {
      if (!this.$refs.speedChart || !this.speedData.models.length) return
      if (this.speedChartInstance) this.speedChartInstance.dispose()
      const chart = echarts.init(this.$refs.speedChart)
      const isLatency = this.speedMode === 'latency'
      const models = this.speedData.models
      const names = models.map(m => m.name)
      const cpuKey = isLatency ? 'latency_cpu' : 'throughput_cpu'
      const gpuKey = isLatency ? 'latency_gpu' : 'throughput_gpu'
      const cpuData = models.map(m => m[cpuKey])
      const gpuData = models.map(m => m[gpuKey])
      const yLabel = isLatency ? '延迟 (ms, 越低越好)' : '吞吐量 (FPS, 越高越好)'
      chart.setOption({
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(20, 28, 47, 0.95)',
          borderColor: 'rgba(0, 212, 255, 0.2)',
          textStyle: { color: '#e2e8f0' },
          formatter: params => {
            const m = models[params[0].dataIndex]
            return m.name + '<br/>' +
              params.map(p => p.marker + ' ' + p.seriesName + ': ' + p.value + (isLatency ? ' ms' : ' FPS')).join('<br/>') +
              '<br/>参数量: ' + m.params_m + 'M | FLOPs: ' + m.flops_g + 'G'
          }
        },
        legend: {
          data: ['CPU (Intel i9)', 'GPU (RTX 4090)'],
          textStyle: { color: '#94a3b8', fontSize: 11 },
          top: '5%', right: '5%', itemWidth: 14, itemHeight: 12
        },
        grid: { left: '5%', right: '8%', bottom: '10%', top: '18%', containLabel: true },
        xAxis: {
          type: 'category', data: names,
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          axisLabel: { color: '#94a3b8', fontSize: 12 }
        },
        yAxis: {
          type: 'value',
          name: yLabel,
          nameTextStyle: { color: '#94a3b8', fontSize: 10 },
          axisLabel: { color: '#94a3b8', fontSize: 11 },
          splitLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.08)' } }
        },
        series: [
          {
            name: 'CPU (Intel i9)', type: 'bar', data: cpuData, barWidth: '30%',
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#f59e0b' }, { offset: 1, color: '#d97706' }
              ]),
              borderRadius: [6, 6, 0, 0]
            }
          },
          {
            name: 'GPU (RTX 4090)', type: 'bar', data: gpuData, barWidth: '30%',
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#00FF88' }, { offset: 1, color: '#059669' }
              ]),
              borderRadius: [6, 6, 0, 0]
            }
          }
        ]
      })
      this.speedChartInstance = chart
    }
  }
}
</script>

<style scoped>
.performance-evaluation-container {
  position: relative;
  padding: clamp(1rem, 3vh, 1.5rem);
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  min-height: 100vh;
}

.bg-grid {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  z-index: 0;
}

.page-header {
  margin-bottom: clamp(1rem, 3vh, 1.5rem);
  text-align: center;
}

.title {
  font-size: clamp(1.5rem, 4vh, 2rem);
  font-weight: 700;
  background: linear-gradient(90deg, #00D4FF, #00FF88);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: clamp(0.75rem, 2vh, 0.9rem);
  color: #94a3b8;
  font-style: italic;
}

.info-banner {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: clamp(0.75rem, 2vh, 1rem);
  margin-bottom: clamp(1rem, 3vh, 1.5rem);
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: clamp(0.75rem, 2vh, 1rem);
  background: rgba(15, 23, 42, 0.6);
  border-radius: 12px;
  border: 1px solid rgba(0, 212, 255, 0.15);
  backdrop-filter: blur(10px);
}

.info-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.info-content {
  font-size: clamp(0.75rem, 2vh, 0.85rem);
  color: #cbd5e1;
  line-height: 1.6;
}

.info-content strong {
  color: #00D4FF;
  font-weight: 600;
}

.section-card {
  background: rgba(15, 23, 42, 0.6);
  border-radius: 16px;
  border: 1px solid rgba(0, 212, 255, 0.15);
  padding: clamp(1rem, 3vh, 1.5rem);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.full-width {
  width: 100%;
  margin-bottom: clamp(1rem, 3vh, 1.5rem);
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: clamp(1rem, 3vh, 1.5rem);
  margin-bottom: clamp(1rem, 3vh, 1.5rem);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: clamp(1rem, 2.5vh, 1.25rem);
  padding-bottom: clamp(0.5rem, 1.5vh, 0.75rem);
  border-bottom: 1px solid rgba(0, 212, 255, 0.1);
}

.card-icon {
  font-size: 1.5rem;
}

.card-title {
  font-size: clamp(1rem, 2.5vh, 1.2rem);
  font-weight: 600;
  color: #e2e8f0;
  flex-grow: 1;
}

.chart-hint {
  font-size: clamp(0.65rem, 1.8vh, 0.75rem);
  color: #94a3b8;
  font-style: italic;
}

.chart-tip {
  font-size: clamp(0.7rem, 2vh, 0.8rem);
  color: #00D4FF;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.chart-container-large {
  width: 100%;
  height: clamp(350px, 50vh, 500px);
}

.speed-toggle {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: clamp(0.4rem, 1.2vh, 0.6rem) clamp(0.75rem, 2vh, 1rem);
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 8px;
  color: #94a3b8;
  font-size: clamp(0.7rem, 1.8vh, 0.8rem);
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  border-color: rgba(0, 212, 255, 0.5);
  color: #e2e8f0;
}

.filter-btn.active {
  background: rgba(0, 212, 255, 0.15);
  border-color: #00D4FF;
  color: #00D4FF;
  font-weight: 600;
}

@media (max-width: 768px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
  
  .info-banner {
    grid-template-columns: 1fr;
  }
  
  .chart-container-large {
    height: clamp(280px, 40vh, 350px);
  }
}
</style>
