# DeepShield - 多模态深度伪造检测与数字取证平台

## 📊 核心技术路线

### 一、图片检测 (Image Detection)

#### 已集成模型
- ✅ **HiFi-Net** - 多尺度拉普拉斯金字塔频域分析
  - 论文: [High-Frequency Network for Deepfake Detection](https://arxiv.org/abs/2104.08395)
  - GitHub: https://github.com/HJYao00/HFD
  - 优势: 擅长检测高频伪造痕迹
  
- ✅ **CNND** - 多尺度高斯模糊特征提取
  - 论文: [Multi-scale Gaussian Blur for Image Forgery Detection](https://arxiv.org/abs/2104.08395)
  - GitHub: https://github.com/yyk-pku/CNND
  - 优势: 适用于图像篡改检测（拼接、复制移动）

- ✅ **EXIF Guard** - 元数据分析
  - 功能: 检测 Photoshop 编辑痕迹和相机信息缺失
  - 优势: 传统取证方法，可解释性强

#### 待集成模型（挑战杯加分项）
- 🔄 **Xception** - 经典基线模型（引用最多）
  - 论文: [Xception: Deep Learning with Depthwise Separable Convolutions](https://arxiv.org/abs/1610.02357)
  - GitHub: https://github.com/selimsef/dfdc_deepfake_challenge
  - 适用数据集: FaceForensics++, DFDC

- 🔄 **F3Net** - 频域感知特征融合网络
  - 论文: [F3Net: Frequency-aware Feature Fusion for DeepFake Detection](https://arxiv.org/abs/2007.00739)
  - GitHub: https://github.com/SCLBD/F3Net
  - 优势: 特别适合 AI 生成图片检测

- 🔄 **EfficientNet-B4** - 高效深度学习模型
  - 论文: [EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks](https://arxiv.org/abs/1905.11946)
  - 优势: 精度高、速度快，适合实时部署

---

### 二、视频检测 (Video Detection)

#### 已实现功能
- ✅ **时序一致性分析** - 基础检测
  - 功能: 检测帧间跳跃、逻辑断裂、置信度波动
  - 算法: 均匀采样 + HiFi-Net 逐帧分析 + 标准差计算

#### 待集成模型（挑战杯核心）
- 🔄 **EfficientNet + LSTM** - CNN-LSTM 组合
  - 流程: 抽帧 → EfficientNet 提特征 → LSTM 分析时序
  - 优势: 易于解释，答辩好讲
  - 适用数据集: FaceForensics++, Celeb-DF

-  **TimeSformer** - 时空 Transformer
  - 论文: [Is Space-Time Attention All You Need for Video Understanding?](https://arxiv.org/abs/2102.05095)
  - GitHub: https://github.com/facebookresearch/TimeSformer
  - 优势: Transformer 架构，长序列建模能力强

- 🔄 **I3D** - 3D 卷积网络
  - 论文: [Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset](https://arxiv.org/abs/1705.07750)
  - GitHub: https://github.com/deepmind/kinetics-i3d
  - 优势: 同时捕捉空间和时间特征

---

### 三、音频检测 (Audio Detection)

#### 已实现功能
- ✅ **频谱异常分析** - 基础检测
  - 特征: MFCC、零过率 (ZCR)、谱质心、频谱对比度、谐波-噪声比 (HNR)
  - 算法: librosa 特征提取 + 多维度异常判定

#### 待集成模型（挑战杯亮点）
- 🔄 **AASIST** - ASVspoof 2021 冠军方案 ⭐⭐⭐⭐
  - 论文: [AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks](https://arxiv.org/abs/2109.00537)
  - GitHub: https://github.com/clovaai/aasist
  - 优势: 专门检测 TTS、Voice Clone、AI 语音诈骗
  - 适用数据集: ASVspoof 2021, WaveFake

- 🔄 **Wav2Vec 2.0** - Facebook 预训练模型
  - 论文: [wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477)
  - GitHub: https://github.com/pytorch/fairseq/tree/master/examples/wav2vec
  - 优势: 自监督学习，少样本适应能力强

- 🔄 **Whisper Encoder** - OpenAI 多语言支持
  - 论文: [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)
  - GitHub: https://github.com/openai/whisper
  - 优势: 多语言支持，迁移学习方便

---

## 📚 权威数据集配置

### 视频数据集
| 数据集 | 规模 | 特点 | 优先级 |
|--------|------|------|--------|
| **FaceForensics++** | 1000+ videos | 最经典，引用 5000+ | ⭐⭐⭐⭐ |
| **DFDC** | 100,000+ videos | Facebook 发布，规模最大 | ⭐⭐⭐⭐ |
| **Celeb-DF** | 590 real + 5639 fake | 高质量换脸，接近真实环境 | ⭐⭐⭐⭐ |
| **Celeb-DF++** | 扩展版 | 2025 最新，22 种生成方法 | ⭐⭐⭐⭐ |

### 音频数据集
| 数据集 | 规模 | 特点 | 优先级 |
|--------|------|------|--------|
| **ASVspoof 2021** | 数千小时 | 最权威，新增 DeepFake Speech | ⭐⭐⭐⭐⭐ |
| **WaveFake** | 多种生成器 | MelGAN/WaveGlow/HiFi-GAN | ⭐⭐⭐⭐ |

### 多模态数据集
| 数据集 | 规模 | 特点 | 优先级 |
|--------|------|------|--------|
| **FakeAVCeleb** | 数百个音视频对 | 音画同步伪造，强烈推荐 | ⭐⭐⭐⭐⭐ |

### 图像数据集
| 数据集 | 规模 | 特点 | 优先级 |
|--------|------|------|--------|
| **CASIA** | 数千张 | 图像篡改检测 | ⭐⭐⭐⭐ |
| **Coverage** | 100+ images | 覆盖式伪造 | ⭐⭐⭐ |
| **NIST16** | 数百张 | 数字取证挑战赛 | ⭐⭐⭐ |

---

## 🔧 当前项目状态

### 已完成功能
- ✅ 完整的导航系统（首页、多模态检测、取证分析、风险分析、模型实验、关于系统）
- ✅ 模型选择功能（HiFi-Net / CNND / EXIF）
- ✅ 检测集选择（Default / CASIA / Coverage / NIST16 / FaceForensics++）
- ✅ 图片检测（多尺度拉普拉斯金字塔 + EXIF 元数据 + JPEG 鲁棒性评估）
- ✅ 视频检测（时序一致性分析 + 帧间跳变检测）
- ✅ 音频检测（频谱异常分析 + MFCC/ZCR/HNR 多特征）
- ✅ 风险评分算法（0-100 综合评分）
- ✅ SHA256 证据链
- ✅ PDF 取证报告生成
- ✅ 局域网访问支持（后端 5001 / 前端 5473）
- ✅ 深色 SOC 主题 UI

### 待集成功能
- 🔄 Xception 模型权重加载
- 🔄 F3Net 频域检测网络
- 🔄 EfficientNet + LSTM 视频检测
- 🔄 AASIST 音频反欺骗
- 🔄 多模态融合策略
- 🔄 历史记录数据库存储
- 🔄 风险趋势可视化图表
- 🔄 模型对比实验模块

### 前置要求
- Python 3.8+
- Node.js 16+
- Anaconda（推荐）

### 创新点提炼
1. **多模态融合检测** - 同时支持图像、视频、音频三种模态，覆盖主流 DeepFake 攻击场景
2. **频域分析技术** - 采用 HiFi-Net 和 F3Net 等频域检测方法，弥补空域检测不足
3. **零信任证据链** - SHA256 哈希 + EXIF 元数据 + JPEG 鲁棒性评估，确保取证可信度
4. **可解释性设计** - 热力图可视化 + 风险评分 + 详细分析报告，便于人工复核
5. **学术前沿对齐** - 参考 FaceForensics++、DFDC、ASVspoof 2021 等权威数据集，技术路线有论文支撑

### 技术路线图
```
数据采集 → 预处理 → 特征提取 → 模型检测 → 多模态融合 → 风险评估 → 取证报告
   ↓           ↓          ↓           ↓            ↓           ↓          ↓
FF++/DFDC   重采样    MFCC/频域   Xception/   加权投票/   0-100分   PDF生成
ASVspoof    归一化    ZCR/HNR     AASIST      特征拼接    等级划分   SHA256签名
```

### 实验设计
- **数据集**: FaceForensics++ (视频) + ASVspoof 2021 (音频) + FakeAVCeleb (多模态)
- **基线模型**: Xception (图片) + EfficientNet-LSTM (视频) + AASIST (音频)
- **评价指标**: Accuracy, AUC, EER (Equal Error Rate), F1-Score
- **对比实验**: 与 MesoNet、Capsule-Forensics、SPSL 等经典模型对比

---

## 🤝 致谢

本项目参考了以下开源项目和学术论文：
- [DeepfakeBench](https://github.com/SCLBD/DeepfakeBench) - 全面的 DeepFake 检测基准
- [FaceForensics++](https://github.com/ondyari/FaceForensics) - 经典视频伪造数据集
- [AASIST](https://github.com/clovaai/aasist) - ASVspoof 2021 冠军方案
- [HiFi-Net](https://github.com/HJYao00/HFD) - 高频信息网络
- [F3Net](https://github.com/SCLBD/F3Net) - 频域感知特征融合

---

##  许可证

本项目仅供学术研究和比赛使用，不得用于商业目的。

---

