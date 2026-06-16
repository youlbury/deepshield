<template>
  <div class="about-page">
    <div class="about-content">
      <h1>关于 DeepShield</h1>
      
      <section class="info-section">
        <h2>系统简介</h2>
        <p>DeepShield 是一个面向 AI 生成内容的多模态内容安全检测与数字取证平台，致力于提供专业级的深度伪造检测服务。</p>
      </section>

      <section class="info-section">
        <h2>核心功能</h2>
        <ul>
          <li><strong>多模态检测：</strong>支持图像、视频、音频全模态深度伪造检测</li>
          <li><strong>多种算法：</strong>集成 HiFi-Net、CNND、EXIF 等多种检测模型</li>
          <li><strong>零信任架构：</strong>SHA256 证据链确保数据完整性与可追溯性</li>
          <li><strong>对抗鲁棒性：</strong>评估模型在 JPEG 压缩等攻击下的稳定性</li>
          <li><strong>司法级报告：</strong>自动生成包含热力图的 PDF 取证报告</li>
        </ul>
      </section>

      <section class="info-section">
        <h2>技术栈</h2>
        <div class="tech-grid">
          <div class="tech-item"><strong>后端:</strong> Flask + Python</div>
          <div class="tech-item"><strong>前端:</strong> Vue 3 + Vite</div>
          <div class="tech-item"><strong>数据库:</strong> SQLite (Flask-SQLAlchemy)</div>
          <div class="tech-item"><strong>图像处理:</strong> OpenCV + Pillow</div>
          <div class="tech-item"><strong>音频处理:</strong> Librosa</div>
          <div class="tech-item"><strong>报告生成:</strong> ReportLab</div>
        </div>
      </section>

      <section class="info-section">
        <h2>联系我们</h2>
        <p>如有问题或建议，欢迎反馈！</p>
      </section>
    </div>
  </div>
</template>

<script>
export default { name: 'About' }
</script>

<style scoped>
.about-page {
  max-width: 1000px;
  margin: 0 auto;
}

.about-content {
  background: rgba(22, 27, 34, 0.8);
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 40px;
}

.about-content h1 {
  font-size: 32px;
  color: #58a6ff;
  margin-bottom: 30px;
  text-align: center;
}

.info-section {
  margin-bottom: 30px;
  padding-bottom: 30px;
  border-bottom: 1px solid #30363d;
}

.info-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.info-section h2 {
  font-size: 20px;
  color: #e6edf3;
  margin-bottom: 15px;
}

.info-section p {
  color: #8b949e;
  line-height: 1.8;
  font-size: 15px;
}

.info-section ul {
  list-style: none;
  padding-left: 0;
}

.info-section li {
  color: #8b949e;
  padding: 8px 0;
  padding-left: 20px;
  position: relative;
}

.info-section li:before {
  content: "▹";
  position: absolute;
  left: 0;
  color: #58a6ff;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.tech-item {
  background: rgba(13, 17, 23, 0.6);
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 15px;
  color: #8b949e;
}

.tech-item strong {
  color: #58a6ff;
}

.system-info {
  background: rgba(13, 17, 23, 0.6);
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 20px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #30363d;
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  color: #8b949e;
}

.value {
  color: #58a6ff;
  font-weight: 600;
}
</style>
