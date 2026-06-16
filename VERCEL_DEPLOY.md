# Vercel 部署指南

## 📋 问题诊断

您遇到的 **404 NOT_FOUND** 错误是因为：
- ✅ Vercel 只能托管**静态前端文件**（HTML/CSS/JS）
- ❌ 您的项目包含 **Flask Python 后端**，无法在 Vercel 运行
- ❌ 缺少 `vercel.json` 配置文件

---

## 🚀 解决方案（推荐方案 1）

### 方案 1：分离部署（前端 Vercel + 后端 Railway）

#### 第一步：部署后端到 Railway.app

1. **注册 Railway**
   - 访问 https://railway.app
   - 使用 GitHub 账号登录

2. **创建新项目**
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 选择您的 chovy 仓库

3. **配置环境变量**
   ```
   FLASK_ENV=production
   DATABASE_URL=sqlite:///chovy_evidence.db
   ```

4. **添加 Python Buildpack**
   - Railway 会自动检测 `requirements.txt`
   - 确保根目录有 `requirements.txt` 或 `setup.py`

5. **获取后端 URL**
   - 部署成功后，Railway 会分配一个域名
   - 例如：`https://chovy-backend.railway.app`

#### 第二步：配置前端 API 地址

1. **修改 `.env.production`**
   ```bash
   # frontend/.env.production
   VITE_API_BASE_URL=https://chovy-backend.railway.app/api
   ```
   ⚠️ **将 URL 替换为您的实际后端地址**

2. **提交代码到 GitHub**
   ```bash
   git add .
   git commit -m "配置 Vercel 部署和 API 地址"
   git push origin main
   ```

#### 第三步：部署前端到 Vercel

1. **连接 GitHub**
   - 访问 https://vercel.com
   - 点击 "Add New Project"
   - 导入您的 chovy 仓库

2. **配置构建设置**
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **添加环境变量**（可选）
   ```
   VITE_API_BASE_URL=https://chovy-backend.railway.app/api
   ```

4. **点击 Deploy**
   - Vercel 会自动构建并部署
   - 部署成功后会分配一个域名
   - 例如：`https://chovy-frontend.vercel.app`

---

## 🔧 已完成的配置

我已经为您创建了以下文件：

### 1. `vercel.json` - Vercel 部署配置
```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### 2. `frontend/.env.production` - 生产环境 API 配置
```env
VITE_API_BASE_URL=https://your-backend-url.railway.app/api
```

### 3. `frontend/src/api/config.js` - 统一 API 请求模块
- 自动根据环境变量切换 API 地址
- 开发环境：使用 Vite 代理（`/api` → `localhost:5001`）
- 生产环境：使用配置的完整 URL

### 4. 更新了 API 调用
- ✅ `EvidenceVerify.vue` - 使用 `apiRequest()`
- ✅ `PerformanceEvaluation.vue` - 使用 `apiRequest()`

### 5. `.gitignore` - 忽略敏感文件
- 防止提交 `.env`、数据库、上传文件等

---

## 🧪 本地测试

### 开发模式（前后端一起运行）

```bash
# 终端 1：启动 Flask 后端
cd chovy
python app.py

# 终端 2：启动 Vue 前端
cd chovy/frontend
npm run dev
```

访问 `http://localhost:5473`

### 生产构建测试

```bash
cd chovy/frontend
npm run build
npx serve dist
```

---

## 📊 其他后端部署选项

| 平台 | 免费层 | 优点 | 缺点 |
|------|--------|------|------|
| **Railway** | $5 信用额度 | 简单易用，自动 SSL | 需要信用卡 |
| **Render** | 免费 | 永久免费层 | 冷启动慢 |
| **PythonAnywhere** | 免费 | 专为 Python 优化 | 功能受限 |
| **Fly.io** | 免费额度 | 全球 CDN | 配置复杂 |
| **Heroku** | 付费 | 稳定可靠 | 无免费层 |

---

## ⚠️ 常见问题

### Q1: 前端仍然显示 404？
**A:** 检查浏览器控制台的网络请求，确认 API 地址是否正确：
```javascript
console.log(import.meta.env.VITE_API_BASE_URL)
```

### Q2: CORS 错误？
**A:** 在 Flask 后端确保启用了 CORS：
```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Q3: 如何更新 API 地址？
**A:** 修改 `frontend/.env.production`，然后重新部署：
```bash
git add frontend/.env.production
git commit -m "更新 API 地址"
git push
```
Vercel 会自动重新构建。

### Q4: 能否只部署前端，不部署后端？
**A:** 可以，但所有 API 调用会失败。您需要：
- 要么部署后端到其他平台
- 要么将后端逻辑改为 Serverless Functions（工作量大）

---

## 🎯 快速开始清单

- [ ] 1. 注册 Railway.app 并部署后端
- [ ] 2. 获取后端 URL（如 `https://xxx.railway.app`）
- [ ] 3. 修改 `frontend/.env.production` 中的 `VITE_API_BASE_URL`
- [ ] 4. 提交代码到 GitHub：`git add . && git commit -m "..." && git push`
- [ ] 5. 在 Vercel 中连接 GitHub 仓库并部署
- [ ] 6. 测试前端是否能正常调用后端 API

---

## 📞 需要帮助？

如果遇到问题，请提供：
1. Vercel 部署日志截图
2. 浏览器控制台的错误信息
3. Railway 后端的日志

祝部署顺利！🎉
