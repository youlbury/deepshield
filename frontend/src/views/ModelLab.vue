<template>
  <div class="model-lab-page">
    <div class="page-header">
      <h1 class="title">模型实验室</h1>
      <p class="subtitle">多模型性能对比与基准测试平台</p>
    </div>

    <!-- 功能说明 -->
    <div class="info-banner">
      <div class="info-item">
        <span class="info-icon">️</span>
        <div class="info-content">
          <strong>图像检测：</strong>Xception, F3Net, EfficientNet
        </div>
      </div>
      <div class="info-item">
        <span class="info-icon"></span>
        <div class="info-content">
          <strong>音频检测：</strong>AASIST
        </div>
      </div>
      <div class="info-item">
        <span class="info-icon"></span>
        <div class="info-content">
          <strong>视频检测：</strong>TimeSformer, Xception
        </div>
      </div>
    </div>
    
    <!-- 模型说明 -->
    <div class="model-info-section">
      <div class="section-title">
        <span class="title-icon">🧠</span>
        <h3>核心检测模型</h3>
        <span class="title-badge">Core Models</span>
      </div>
          
      <div class="model-categories">
        <!-- 图像检测模型 -->
        <div class="category-card image-category">
          <div class="category-header">
            <span class="category-icon">️</span>
            <div class="category-info">
              <h4>图像检测模型</h4>
              <p class="category-desc">Image Detection Models</p>
            </div>
          </div>
          <div class="model-list">
            <div class="model-item">
              <span class="model-color" style="background: #00d9ff;"></span>
              <div class="model-details">
                <strong>Xception</strong>
                <span class="model-type">深度卷积网络 | Google</span>
              </div>
            </div>
            <div class="model-item">
              <span class="model-color" style="background: #00ff88;"></span>
              <div class="model-details">
                <strong>F3Net</strong>
                <span class="model-type">频域感知特征融合 | DeepFake专用</span>
              </div>
            </div>
            <div class="model-item">
              <span class="model-color" style="background: #a855f7;"></span>
              <div class="model-details">
                <strong>EfficientNet</strong>
                <span class="model-type">高效复合缩放网络 | Google</span>
              </div>
            </div>
          </div>
        </div>
    
        <!-- 音频检测模型 -->
        <div class="category-card audio-category">
          <div class="category-header">
            <span class="category-icon"></span>
            <div class="category-info">
              <h4>音频检测模型</h4>
              <p class="category-desc">Audio Detection Models</p>
            </div>
          </div>
          <div class="model-list">
            <div class="model-item">
              <span class="model-color" style="background: #ffa500;"></span>
              <div class="model-details">
                <strong>AASIST</strong>
                <span class="model-type">频谱时序图注意力网络 | 反欺骗检测</span>
              </div>
            </div>
          </div>
        </div>
    
        <!-- 视频检测模型 -->
        <div class="category-card video-category">
          <div class="category-header">
            <span class="category-icon">🎬</span>
            <div class="category-info">
              <h4>视频检测模型</h4>
              <p class="category-desc">Video Detection Models</p>
            </div>
          </div>
          <div class="model-list">
            <div class="model-item">
              <span class="model-color" style="background: #ff4444;"></span>
              <div class="model-details">
                <strong>TimeSformer</strong>
                <span class="model-type">时空Transformer | 视频理解</span>
              </div>
            </div>
            <div class="model-item">
              <span class="model-color" style="background: #00d9ff;"></span>
              <div class="model-details">
                <strong>Xception</strong>
                <span class="model-type">帧级特征提取 | 复用图像模型</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 雷达图 + 数据集选择 -->
    <div class="charts-row">
      <div class="section-card">
        <div class="card-header">
          <span class="card-icon">🎯</span>
          <span class="card-title">模型性能雷达图</span>
          <span class="chart-tip">5 模型对比</span>
        </div>
        <div ref="radarChart" class="chart-container-large"></div>
      </div>

      <div class="section-card">
        <div class="card-header">
          <span class="card-icon">📊</span>
          <span class="card-title">数据集选择</span>
          <span v-if="selectedDatasets.length > 0" class="selection-hint">已选 {{ selectedDatasets.length }} 个</span>
        </div>
        <div class="dataset-grid">
          <div
            v-for="dataset in datasets"
            :key="dataset.id"
            class="dataset-card"
            :class="{ selected: selectedDatasets.includes(dataset.id) }"
            @click="toggleDataset(dataset.id)"
          >
            <div class="dataset-icon">{{ dataset.icon }}</div>
            <div class="dataset-info">
              <span class="dataset-name">{{ dataset.name }}</span>
              <span class="dataset-cn">{{ dataset.cnName }}</span>
              <span class="dataset-size">{{ dataset.size }}</span>
            </div>
            <div class="dataset-check">
              <span v-if="selectedDatasets.includes(dataset.id)">✓</span>
            </div>
          </div>
        </div>

        <button
          class="benchmark-btn"
          :class="{ active: selectedDatasets.length > 0 }"
          :disabled="selectedDatasets.length === 0"
          @click="runBenchmark"
        >
          <span v-if="!isBenchmarking" class="btn-content">
            <span class="btn-icon">▶</span>
            <span>运行基准测试</span>
          </span>
          <span v-else class="loading-content">
            <span class="spinner"></span>
            <span>运行中...</span>
          </span>
        </button>
      </div>
    </div>

    <!-- 散点图 -->
    <div class="section-card full-width">
      <div class="card-header">
        <span class="card-icon">✨</span>
        <span class="card-title">模型性能散点图</span>
        <div class="chart-controls">
          <span class="chart-tip" v-if="isScatterRunning">实时更新中...</span>
          <span class="chart-hint">鼠标悬停查看详情 | 圆圈大小 = 推理延迟 (ms)</span>
        </div>
      </div>
      <div ref="scatterChart" class="chart-container-large"></div>
    </div>

    <!-- 对比柱状图 -->
    <div class="section-card full-width">
      <div class="card-header">
        <span class="card-icon">📈</span>
        <span class="card-title">模型对比分析</span>
        <div class="metric-filter">
          <button
            v-for="metric in comparisonMetrics"
            :key="metric.id"
            class="filter-btn"
            :class="{ active: selectedMetric === metric.id }"
            @click="selectedMetric = metric.id"
          >
            {{ metric.label }}<span class="metric-en">({{ metric.enLabel }})</span>
          </button>
        </div>
      </div>
      <p class="chart-description">点击上方指标按钮切换视图，绿色柱子为当前最优模型</p>
      <div ref="comparisonChart" class="chart-container-large"></div>
    </div>

    <!-- Benchmark 结果 -->
    <div v-if="benchmarkResult" class="section-card full-width">
      <div class="card-header">
        <span class="card-icon">🏆</span>
        <span class="card-title">基准测试结果</span>
        <span class="selection-hint">{{ selectedDatasets.length }} 个数据集</span>
      </div>
      <div class="benchmark-results">
        <div
          v-for="(result, modelName) in benchmarkResult"
          :key="modelName"
          class="result-card"
        >
          <div class="result-header">
            <span class="result-model">{{ getModelDisplayName(modelName) }}</span>
            <span class="result-rank" :class="getRankClass(result.rank)">No.{{ result.rank }}</span>
          </div>
          <div class="result-metrics">
            <div class="metric-item">
              <span class="metric-label">准确率 (Accuracy)</span>
              <span class="metric-value">{{ result.accuracy }}%</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">AUC</span>
              <span class="metric-value">{{ result.auc }}%</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">等错误率 (EER)</span>
              <span class="metric-value">{{ result.eer }}%</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">推理延迟 (Latency)</span>
              <span class="metric-value">{{ result.latency }}ms</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'ModelLab',
  data() {
    return {
      selectedMetric: 'accuracy',
      selectedDatasets: ['faceforensics'],
      isBenchmarking: false,
      isScatterRunning: false,
      benchmarkResult: null,

      radarChartInstance: null,
      comparisonChartInstance: null,
      scatterChartInstance: null,
      scatterAnimationTimer: null,
      scatterData: [],

      availableModels: [
        { id: 'xception', name: 'Xception', cnName: 'Xception 深度可分离卷积网络' },
        { id: 'f3net', name: 'F3Net', cnName: 'F3Net 频域感知融合网络' },
        { id: 'efficientnet', name: 'EfficientNet', cnName: 'EfficientNet 高效缩放网络' },
        { id: 'aasist', name: 'AASIST', cnName: 'AASIST 图注意力反欺骗网络' },
        { id: 'timesformer', name: 'TimeSformer', cnName: 'TimeSformer 时空 Transformer' }
      ],

      datasets: [
        { id: 'faceforensics', name: 'FaceForensics++', cnName: '面部伪造检测', size: '5 万+ 样本', icon: '🖼' },
        { id: 'dfdc', name: 'DFDC', cnName: '深度伪造检测挑战赛', size: '10 万+ 样本', icon: '🎬' },
        { id: 'celebdf', name: 'Celeb-DF', cnName: '名人深度伪造', size: '1 万+ 样本', icon: '👤' },
        { id: 'asvspoof', name: 'ASVspoof 2021', cnName: '语音反欺骗挑战赛', size: '2 万+ 样本', icon: '🎵' }
      ],

      comparisonMetrics: [
        { id: 'accuracy', label: '准确率', enLabel: 'Accuracy' },
        { id: 'auc', label: 'AUC', enLabel: 'Area Under Curve' },
        { id: 'recall', label: '召回率', enLabel: 'Recall' },
        { id: 'precision', label: '精确率', enLabel: 'Precision' },
        { id: 'f1', label: 'F1 分数', enLabel: 'F1 Score' }
      ],

      modelMetrics: {
        xception: { accuracy: 96.2, auc: 98.1, recall: 95.8, precision: 96.5, f1: 95.8 },
        f3net: { accuracy: 94.5, auc: 97.0, recall: 94.2, precision: 94.8, f1: 93.8 },
        efficientnet: { accuracy: 95.8, auc: 97.8, recall: 95.5, precision: 96.0, f1: 95.2 },
        aasist: { accuracy: 93.2, auc: 96.5, recall: 92.8, precision: 93.5, f1: 92.5 },
        timesformer: { accuracy: 97.5, auc: 98.8, recall: 97.2, precision: 97.8, f1: 97.0 }
      },

      scatterBaseData: [
        { name: 'Xception', x: 96.2, y: 98.1, z: 45, category: '图像' },
        { name: 'F3Net', x: 95.5, y: 97.5, z: 52, category: '图像' },
        { name: 'EfficientNet', x: 95.8, y: 97.8, z: 38, category: '图像' },
        { name: 'AASIST', x: 94.8, y: 97.2, z: 28, category: '音频' },
        { name: 'TimeSformer', x: 97.1, y: 98.5, z: 68, category: '视频' }
      ]
    }
  },

  mounted() {
    this.$nextTick(() => {
      this.initAllCharts()
    })
    window.addEventListener('resize', this.handleResize)
  },

  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
    this.disposeCharts()
  },

  methods: {
    getModelDisplayName(modelId) {
      const model = this.availableModels.find(m => m.id === modelId.toLowerCase())
      if (model) return `${model.name}（${model.cnName}）`
      return modelId
    },

    getMetricLabel(metricId) {
      const m = this.comparisonMetrics.find(x => x.id === metricId)
      return m ? `${m.label} (${m.enLabel})` : metricId
    },

    initAllCharts() {
      this.initRadarChart()
      this.initScatterChart()
      this.initComparisonChart()
      this.startScatterAnimation()
    },

    disposeCharts() {
      if (this.radarChartInstance) { this.radarChartInstance.dispose(); this.radarChartInstance = null }
      if (this.scatterChartInstance) { this.scatterChartInstance.dispose(); this.scatterChartInstance = null }
      if (this.comparisonChartInstance) { this.comparisonChartInstance.dispose(); this.comparisonChartInstance = null }
      if (this.scatterAnimationTimer) { clearInterval(this.scatterAnimationTimer); this.scatterAnimationTimer = null }
    },

    handleResize() {
      if (this.radarChartInstance) this.radarChartInstance.resize()
      if (this.scatterChartInstance) this.scatterChartInstance.resize()
      if (this.comparisonChartInstance) this.comparisonChartInstance.resize()
    },

    initRadarChart() {
      if (!this.$refs.radarChart) return
      if (this.radarChartInstance) this.radarChartInstance.dispose()

      const chart = echarts.init(this.$refs.radarChart)
      const colors = ['#00D4FF', '#00FF88', '#8b5cf6', '#f59e0b', '#ef4444']

      const seriesData = this.availableModels.map((model, idx) => {
        const metrics = this.modelMetrics[model.id]
        const color = colors[idx % colors.length]
        return {
          value: [metrics.accuracy, metrics.auc, metrics.recall, metrics.precision, metrics.f1],
          name: model.name,
          symbol: 'circle',
          symbolSize: 6,
          lineStyle: { color, width: 2 },
          itemStyle: { color },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: color + '40' },
              { offset: 1, color: color + '10' }
            ])
          }
        }
      })

      chart.setOption({
        tooltip: {
          backgroundColor: 'rgba(20, 28, 47, 0.95)',
          borderColor: 'rgba(0, 212, 255, 0.2)',
          textStyle: { color: '#e2e8f0' }
        },
        legend: {
          data: this.availableModels.map(m => m.name),
          textStyle: { color: '#94a3b8', fontSize: 11 },
          bottom: '5%',
          left: 'center',
          itemWidth: 16,
          itemHeight: 12,
          itemGap: 20
        },
        radar: {
          indicator: [
            { name: '准确率\nAccuracy', max: 100 },
            { name: 'AUC', max: 100 },
            { name: '召回率\nRecall', max: 100 },
            { name: '精确率\nPrecision', max: 100 },
            { name: 'F1 分数', max: 100 }
          ],
          center: ['50%', '45%'],
          radius: '52%',
          axisName: { color: '#94a3b8', fontSize: 12, fontWeight: 600, padding: [3, 5] },
          splitArea: { areaStyle: { color: ['rgba(0, 212, 255, 0.03)', 'rgba(0, 212, 255, 0.06)'] } },
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          splitLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.2)' } }
        },
        series: [{ type: 'radar', data: seriesData }]
      })
      this.radarChartInstance = chart
    },

    initScatterChart() {
      if (!this.$refs.scatterChart) return
      if (this.scatterChartInstance) this.scatterChartInstance.dispose()

      const chart = echarts.init(this.$refs.scatterChart)

      this.scatterData = this.scatterBaseData.map(item => ({
        ...item,
        x: item.x + (Math.random() - 0.5) * 0.5,
        y: item.y + (Math.random() - 0.5) * 0.5
      }))

      const makeSeries = (category, color, shadowColor) => ({
        name: category,
        type: 'scatter',
        data: this.scatterData.filter(d => d.category === category).map(d => ({
          value: [d.x, d.y, d.z],
          name: d.name
        })),
        symbolSize: data => Math.max(18, 24 + (68 - data[2]) * 0.4),
        itemStyle: { color, shadowBlur: 15, shadowColor },
        emphasis: {
          itemStyle: { shadowBlur: 25, shadowColor }
        },
        label: {
          show: true,
          position: 'right',
          formatter: p => p.name,
          fontSize: 11,
          color: '#cbd5e1',
          distance: 6
        }
      })

      chart.setOption({
        tooltip: {
          backgroundColor: 'rgba(20, 28, 47, 0.95)',
          borderColor: 'rgba(0, 212, 255, 0.2)',
          textStyle: { color: '#e2e8f0' },
          formatter: p => `<strong>${p.name}</strong><br/>
            准确率 Accuracy: ${p.value[0].toFixed(2)}%<br/>
            AUC: ${p.value[1].toFixed(2)}%<br/>
            推理延迟 Latency: ${p.data.value[2]}ms<br/>
            模态: ${p.seriesName}`
        },
        legend: {
          data: ['图像', '音频', '视频'],
          textStyle: { color: '#94a3b8', fontSize: 12 },
          top: '5%',
          right: '5%',
          itemWidth: 14,
          itemHeight: 14
        },
        grid: { left: '8%', right: '18%', bottom: '8%', top: '15%', containLabel: true },
        xAxis: {
          name: '准确率 Accuracy (%)',
          nameTextStyle: { color: '#94a3b8', fontSize: 11 },
          type: 'value',
          min: 93, max: 98,
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          axisLabel: { color: '#94a3b8', fontSize: 11 },
          splitLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.1)' } }
        },
        yAxis: {
          name: 'AUC (%)',
          nameTextStyle: { color: '#94a3b8', fontSize: 11 },
          type: 'value',
          min: 96, max: 99,
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          axisLabel: { color: '#94a3b8', fontSize: 11 },
          splitLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.1)' } }
        },
        series: [
          makeSeries('图像', '#00D4FF', 'rgba(0, 212, 255, 0.6)'),
          makeSeries('音频', '#00FF88', 'rgba(0, 255, 136, 0.6)'),
          makeSeries('视频', '#8b5cf6', 'rgba(139, 92, 246, 0.6)')
        ]
      })
      this.scatterChartInstance = chart
    },

    startScatterAnimation() {
      this.isScatterRunning = true
      this.scatterAnimationTimer = setInterval(() => {
        if (!this.scatterChartInstance) return
        this.scatterData = this.scatterBaseData.map(item => ({
          ...item,
          x: item.x + (Math.random() - 0.5) * 0.8,
          y: item.y + (Math.random() - 0.5) * 0.6
        }))
        this.scatterChartInstance.setOption({
          series: [
            {
              data: this.scatterData.filter(d => d.category === '图像').map(d => ({ value: [d.x, d.y, d.z], name: d.name }))
            },
            {
              data: this.scatterData.filter(d => d.category === '音频').map(d => ({ value: [d.x, d.y, d.z], name: d.name }))
            },
            {
              data: this.scatterData.filter(d => d.category === '视频').map(d => ({ value: [d.x, d.y, d.z], name: d.name }))
            }
          ]
        })
      }, 2000)
    },

    stopScatterAnimation() {
      this.isScatterRunning = false
      if (this.scatterAnimationTimer) {
        clearInterval(this.scatterAnimationTimer)
        this.scatterAnimationTimer = null
      }
    },

    initComparisonChart() {
      if (!this.$refs.comparisonChart) return
      if (this.comparisonChartInstance) this.comparisonChartInstance.dispose()

      const chart = echarts.init(this.$refs.comparisonChart)
      const modelNames = this.availableModels.map(m => m.name)
      const values = this.availableModels.map(m => this.modelMetrics[m.id][this.selectedMetric])
      const maxIdx = values.indexOf(Math.max(...values))

      chart.setOption({
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(20, 28, 47, 0.95)',
          borderColor: 'rgba(0, 212, 255, 0.2)',
          textStyle: { color: '#e2e8f0' },
          axisPointer: { type: 'shadow' },
          formatter: p => {
            const m = this.comparisonMetrics.find(x => x.id === this.selectedMetric)
            return `${p[0].name}<br/>${m ? m.label + ' (' + m.enLabel + ')' : this.selectedMetric}: ${p[0].value}`
          }
        },
        grid: { left: '3%', right: '4%', bottom: '10%', top: '10%', containLabel: true },
        xAxis: {
          type: 'category',
          data: modelNames,
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          axisLabel: { color: '#94a3b8', fontSize: 12 }
        },
        yAxis: {
          type: 'value',
          min: 90, max: 100,
          name: this.getMetricLabel(this.selectedMetric),
          nameTextStyle: { color: '#94a3b8', fontSize: 10 },
          axisLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.3)' } },
          axisLabel: { color: '#94a3b8', fontSize: 11 },
          splitLine: { lineStyle: { color: 'rgba(0, 212, 255, 0.1)' } }
        },
        series: [{
          type: 'bar',
          data: values.map((val, idx) => ({
            value: val,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: idx === maxIdx ? '#00FF88' : '#00D4FF' },
                { offset: 1, color: idx === maxIdx ? '#059669' : '#0099cc' }
              ]),
              borderRadius: [8, 8, 0, 0]
            }
          })),
          barWidth: '45%',
          emphasis: { itemStyle: { shadowBlur: 15, shadowColor: 'rgba(0, 212, 255, 0.5)' } }
        }]
      })
      this.comparisonChartInstance = chart
    },

    toggleDataset(id) {
      const index = this.selectedDatasets.indexOf(id)
      if (index > -1) {
        this.selectedDatasets.splice(index, 1)
      } else {
        this.selectedDatasets.push(id)
      }
    },

    async runBenchmark() {
      if (this.selectedDatasets.length === 0) return

      this.isBenchmarking = true
      this.benchmarkResult = null
      this.stopScatterAnimation()

      await new Promise(r => setTimeout(r, 2000))

      const count = this.selectedDatasets.length
      const factor = 0.95 + count * 0.04

      // 根据选择的数据集更新所有模型指标
      const newMetrics = {}
      this.availableModels.forEach(model => {
        const base = {
          xception: { accuracy: 96.2, auc: 98.1, recall: 95.8, precision: 96.5, f1: 95.8 },
          f3net: { accuracy: 94.5, auc: 97.0, recall: 94.2, precision: 94.8, f1: 93.8 },
          efficientnet: { accuracy: 95.8, auc: 97.8, recall: 95.5, precision: 96.0, f1: 95.2 },
          aasist: { accuracy: 93.2, auc: 96.5, recall: 92.8, precision: 93.5, f1: 92.5 },
          timesformer: { accuracy: 97.5, auc: 98.8, recall: 97.2, precision: 97.8, f1: 97.0 }
        }[model.id]
        // 数据集越多，指标略微下降（模拟真实场景）
        const jitter = () => (Math.random() - 0.5) * 2
        newMetrics[model.id] = {
          accuracy: Math.round((base.accuracy * factor + jitter()) * 10) / 10,
          auc: Math.round((base.auc * factor + jitter()) * 10) / 10,
          recall: Math.round((base.recall * factor + jitter()) * 10) / 10,
          precision: Math.round((base.precision * factor + jitter()) * 10) / 10,
          f1: Math.round((base.f1 * factor + jitter()) * 10) / 10
        }
      })
      this.modelMetrics = newMetrics

      // 生成benchmark结果
      const modelIds = ['TimeSformer', 'EfficientNet', 'Xception', 'F3Net', 'AASIST']
      this.benchmarkResult = {}
      modelIds.forEach((name, idx) => {
        const id = name.toLowerCase()
        const m = newMetrics[id]
        this.benchmarkResult[name] = {
          rank: idx + 1,
          accuracy: m.accuracy.toFixed(1),
          auc: m.auc.toFixed(1),
          eer: ((100 - m.auc) / 2).toFixed(1),
          latency: { timesformer: 68, efficientnet: 38, xception: 45, f3net: 52, aasist: 28 }[id]
        }
      })

      this.isBenchmarking = false

      this.$nextTick(() => {
        this.initRadarChart()
        this.initComparisonChart()
        this.initScatterChart()
        this.startScatterAnimation()
      })
    },

    getRankClass(rank) {
      if (rank === 1) return 'rank-1'
      if (rank === 2) return 'rank-2'
      if (rank === 3) return 'rank-3'
      return 'rank-other'
    }
  },

  watch: {
    selectedMetric() {
      this.initComparisonChart()
    }
  }
}
</script>

<style scoped>
.model-lab-page {
  padding: 1rem 1.5rem 2rem 1rem;
  min-height: 100%;
  /* 移除 overflow，由外层 el-scrollbar 统一管理 */
  display: flex;
  flex-direction: column;
}

/* 自定义滚动条 */
.model-lab-page::-webkit-scrollbar { width: 6px; }
.model-lab-page::-webkit-scrollbar-track { background: transparent; }
.model-lab-page::-webkit-scrollbar-thumb { background: rgba(0, 212, 255, 0.2); border-radius: 3px; }

.page-header {
  margin-bottom: 1rem;
  padding: 1.25rem 1.5rem;
  flex-shrink: 0;
  background: #141C2F;
  border-radius: 12px;
  border: 1px solid rgba(0, 212, 255, 0.15);
}

.title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  background: linear-gradient(90deg, #00D4FF, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 12px;
  color: #64748b;
  margin: 0;
}

/* 功能说明 - 纵向排列 */
.info-banner {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.05), rgba(0, 255, 136, 0.05));
  border-radius: 12px;
  border: 1px solid rgba(0, 212, 255, 0.1);
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.info-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
  margin-top: 1px;
}

.info-content {
  font-size: 0.85rem;
  color: #cbd5e1;
  line-height: 1.6;
}

.info-content strong {
  color: #00D4FF;
  font-weight: 600;
}

/* 模型说明区域 */
.model-info-section {
  margin-bottom: 1.25rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.05), rgba(0, 217, 255, 0.05));
  border-radius: 12px;
  border: 1px solid rgba(139, 92, 246, 0.15);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.title-icon {
  font-size: 1.5rem;
}

.section-title h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0;
}

.title-badge {
  font-size: 0.75rem;
  color: #8b5cf6;
  padding: 0.25rem 0.75rem;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 12px;
  font-weight: 600;
}

.model-categories {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.category-card {
  background: rgba(20, 28, 47, 0.6);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
}

.category-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 217, 255, 0.1);
  border-color: rgba(0, 217, 255, 0.2);
}

.image-category { border-left: 3px solid #00d9ff; }
.audio-category { border-left: 3px solid #ffa500; }
.video-category { border-left: 3px solid #ff4444; }

.category-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.category-icon {
  font-size: 1.5rem;
}

.category-info h4 {
  font-size: 0.95rem;
  font-weight: 600;
  color: #f1f5f9;
  margin: 0 0 0.25rem 0;
}

.category-desc {
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 0;
}

.model-list {
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.model-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.model-item:hover {
  background: rgba(255, 255, 255, 0.06);
  transform: translateX(4px);
}

.model-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 8px currentColor;
}

.model-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.model-details strong {
  font-size: 0.875rem;
  font-weight: 600;
  color: #e2e8f0;
}

.model-type {
  font-size: 0.7rem;
  color: #94a3b8;
}

/* 图表行 */
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  min-height: 420px;
  margin-bottom: 1.25rem;
}

.section-card {
  background: #141C2F;
  border-radius: 12px;
  border: 1px solid rgba(0, 212, 255, 0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  margin-bottom: 1.25rem;
}

.section-card.full-width {
  grid-column: span 2;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(0, 212, 255, 0.1);
  background: rgba(0, 212, 255, 0.03);
  flex-shrink: 0;
}

.card-icon { font-size: 1.25rem; }

.card-title {
  flex: 1;
  font-size: 1rem;
  font-weight: 600;
  color: #f1f5f9;
  margin-left: 0.5rem;
}

.chart-tip {
  font-size: 0.75rem;
  color: #00FF88;
  animation: pulse 2s ease-in-out infinite;
}

.selection-hint {
  font-size: 0.75rem;
  color: #00D4FF;
  padding: 0.25rem 0.75rem;
  background: rgba(0, 212, 255, 0.1);
  border-radius: 12px;
  font-weight: 600;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.chart-hint {
  font-size: 0.7rem;
  color: #94a3b8;
  padding: 0.25rem 0.5rem;
  background: rgba(0, 212, 255, 0.1);
  border-radius: 4px;
}

.chart-description {
  margin: 0;
  padding: 0.75rem 1.5rem;
  font-size: 0.8rem;
  color: #94a3b8;
  background: rgba(0, 212, 255, 0.05);
  border-bottom: 1px solid rgba(0, 212, 255, 0.1);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* 数据集 */
.dataset-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  padding: 1rem;
}

.dataset-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 0.75rem;
  background: rgba(10, 16, 32, 0.6);
  border: 1px solid rgba(0, 212, 255, 0.1);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.25s;
}

.dataset-card:hover { border-color: rgba(0, 212, 255, 0.3); }

.dataset-card.selected {
  background: rgba(0, 212, 255, 0.15);
  border-color: #00D4FF;
}

.dataset-icon { font-size: 1.4rem; flex-shrink: 0; }

.dataset-info { flex: 1; min-width: 0; }

.dataset-name {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #f1f5f9;
}

.dataset-cn {
  display: block;
  font-size: 0.65rem;
  color: #64748b;
  margin-top: 2px;
}

.dataset-size {
  font-size: 0.65rem;
  color: #475569;
}

.dataset-check {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(0, 212, 255, 0.2);
  border: 1px solid rgba(0, 212, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  color: #00D4FF;
  flex-shrink: 0;
}

/* Benchmark按钮 */
.benchmark-btn {
  width: calc(100% - 2rem);
  margin: 1rem;
  padding: 0.875rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #475569, #334155);
  cursor: not-allowed;
  transition: all 0.3s;
}

.benchmark-btn.active {
  background: linear-gradient(135deg, #00D4FF, #0099cc);
  cursor: pointer;
}

.benchmark-btn.active:hover {
  box-shadow: 0 4px 20px rgba(0, 212, 255, 0.4);
  transform: translateY(-1px);
}

.benchmark-btn .btn-content,
.benchmark-btn .loading-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* 图表容器 */
.chart-container-large {
  flex: 1;
  min-height: 380px;
  height: 380px;
  padding: 1rem;
}

/* 指标过滤 */
.metric-filter { display: flex; gap: 0.35rem; flex-wrap: wrap; }

.filter-btn {
  padding: 0.4rem 0.75rem;
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 6px;
  background: rgba(10, 16, 32, 0.6);
  color: #94a3b8;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.25s;
  white-space: nowrap;
}

.filter-btn:hover { border-color: rgba(0, 212, 255, 0.5); }

.filter-btn.active {
  background: rgba(0, 212, 255, 0.2);
  border-color: #00D4FF;
  color: #00D4FF;
}

.metric-en {
  font-size: 0.65rem;
  color: #64748b;
  margin-left: 3px;
}

.filter-btn.active .metric-en { color: #00D4FF; }

/* Benchmark结果 */
.benchmark-results {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  padding: 1rem;
}

.result-card {
  background: rgba(10, 16, 32, 0.6);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid rgba(0, 212, 255, 0.1);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.result-model {
  font-size: 0.85rem;
  font-weight: 600;
  color: #f1f5f9;
}

.result-rank {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 700;
}

.result-rank.rank-1 { background: rgba(255, 215, 0, 0.2); color: #ffd700; }
.result-rank.rank-2 { background: rgba(192, 192, 192, 0.2); color: #c0c0c0; }
.result-rank.rank-3 { background: rgba(205, 127, 50, 0.2); color: #cd7f32; }
.result-rank.rank-other { background: rgba(100, 116, 139, 0.2); color: #64748b; }

.result-metrics { display: flex; flex-direction: column; gap: 0.5rem; }

.metric-item { display: flex; justify-content: space-between; }

.metric-label { font-size: 0.7rem; color: #64748b; }

.metric-value { font-size: 0.8rem; font-weight: 600; color: #00D4FF; }

/* 速度切换 */
.speed-toggle { display: flex; gap: 0.35rem; }

/* 响应式 */
@media (max-width: 1200px) {
  .charts-row { grid-template-columns: 1fr; }
  .section-card.full-width { grid-column: span 1; }
  .benchmark-results { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 768px) {
  .dataset-grid { grid-template-columns: 1fr; }
  .benchmark-results { grid-template-columns: repeat(2, 1fr); }
  .metric-filter { gap: 0.25rem; }
  .filter-btn { padding: 0.3rem 0.5rem; font-size: 0.7rem; }
  .model-lab-page { padding: 0.5rem; }
}
</style>