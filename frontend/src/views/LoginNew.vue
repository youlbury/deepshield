<template>
  <div class="select-none">
    <div class="login-container">
      <div class="img">
        <!-- 使用科技感登录背景图 -->
        <img src="../assets/login.png" alt="DeepShield Background" class="background-img" />
      </div>
      <div class="login-box">
        <div class="login-form">
          <div class="avatar-container">
            <!-- Element Plus 实心人头图标头像 -->
            <el-avatar size="60" style="background: linear-gradient(135deg, #00D4FF, #00FF88);">
              <el-icon size="34" color="#fff">
                <UserFilled />
              </el-icon>
            </el-avatar>
          </div>
          <Motion :delay="0">
            <h2 class="outline-hidden brand-title">
              影盾
            </h2>
          </Motion>

          <el-form
            ref="ruleFormRef"
            :model="ruleForm"
            :rules="loginRules"
            size="large"
          >
            <Motion :delay="100">
              <el-form-item
                :rules="[
                  {
                    required: true,
                    message: '请输入用户名',
                    trigger: 'blur'
                  }
                ]"
                prop="username"
              >
                <el-input
                  v-model="ruleForm.username"
                  clearable
                  placeholder="请输入用户名"
                  :prefix-icon="UserIcon"
                />
              </el-form-item>
            </Motion>

            <Motion :delay="150">
              <el-form-item prop="password">
                <el-input
                  v-model="ruleForm.password"
                  clearable
                  show-password
                  placeholder="请输入密码"
                  :prefix-icon="LockIcon"
                />
              </el-form-item>
            </Motion>

            <Motion :delay="250">
              <!-- 表单项弹性布局，实现登录按钮右移 -->
              <el-form-item style="display:flex;flex-direction:column;align-items:flex-end;">
                <div class="w-full h-5 flex-bc">
                  <el-checkbox v-model="checked">
                    <span class="flex">
                      <select
                        v-model="loginDay"
                        :style="{
                          width: loginDay < 10 ? '10px' : '16px',
                          outline: 'none',
                          background: 'none',
                          appearance: 'none',
                          border: 'none'
                        }"
                      >
                        <option value="1">1</option>
                        <option value="7">7</option>
                        <option value="30">30</option>
                      </select>
                      记住我
                    </span>
                  </el-checkbox>
                </div>
                <!-- 缩小宽度靠右展示 -->
                <el-button
                  style="width:80%"
                  class="mt-4!"
                  size="default"
                  type="primary"
                  :loading="loading"
                  :disabled="disabled"
                  @click="onLogin(ruleFormRef)"
                >
                  登录
                </el-button>
              </el-form-item>
            </Motion>
          </el-form>

          <Motion :delay="350">
            <el-form-item>
              <el-divider>
                <p class="text-gray-500 text-xs">
                  测试账号: admin / admin123
                </p>
              </el-divider>
            </el-form-item>
          </Motion>

          <div class="back-home">
            <a href="#" @click.prevent="$router.push('/')">← 返回首页</a>
          </div>
        </div>
      </div>
    </div>
    <div
      class="w-full flex-c absolute bottom-3 text-sm text-[rgba(0,0,0,0.6)] dark:text-[rgba(220,220,242,0.8)]"
    >
      Copyright © 2020-present
      <a
        class="hover:text-primary!"
        href="#"
        target="_blank"
      >
        &nbsp;影盾 深度伪造检测平台
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import Motion from './utils/motion'
// 导入实心人头图标 UserFilled
import { User, Lock, UserFilled } from '@element-plus/icons-vue'
import { login } from '../store/auth'

// 图标组件
const UserIcon = User
const LockIcon = Lock

const router = useRouter()
const loading = ref(false)
const disabled = ref(false)
const checked = ref(false)
const loginDay = ref(7)
const ruleFormRef = ref()

const ruleForm = reactive({
  username: 'admin',
  password: 'admin123'
})

const loginRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
})

const onLogin = async (formEl) => {
  if (!formEl) return
  await formEl.validate(valid => {
    if (valid) {
      loading.value = true
      // 模拟登录请求
      setTimeout(() => {
        if (ruleForm.username === 'admin' && ruleForm.password === 'admin123') {
          login(ruleForm.username)
          ElMessage.success('登录成功')
          router.push('/')
        } else {
          ElMessage.error('用户名或密码错误')
        }
        loading.value = false
      }, 1000)
    } else {
      loading.value = false
    }
  })
}
</script>

<style scoped>
/* 登录容器样式 */
.login-container {
  width: 100vw;
  height: 100vh;
  max-width: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-gap: 18rem;
  padding: 0 2rem;
}

.img {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.background-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.9;
}

.login-box {
  display: flex;
  align-items: center;
  text-align: center;
  overflow: hidden;
}

.login-form {
  width: 360px;
}

.avatar-container {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

/* 品牌标题渐变文字 */
.brand-title {
  background: linear-gradient(90deg, #00D4FF, #00FF88);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: bold;
  margin: 15px 0;
  font-size: 28px;
}

/* 登录按钮渐变主题 */
:deep(.el-button--primary) {
  background: linear-gradient(135deg, #00D4FF 0%, #06b6d4 50%, #0891b2 100%);
  border: none;
  box-shadow: 0 0 24px rgba(0, 212, 255, 0.2);
}

:deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 50%, #0e7490 100%);
  box-shadow: 0 8px 32px rgba(0, 212, 255, 0.35);
}

/* 输入框深色样式 */
:deep(.el-input__wrapper) {
  background: rgba(4, 10, 22, 0.7);
  border: 1px solid rgba(0, 212, 255, 0.15);
  box-shadow: none;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: rgba(0, 212, 255, 0.5);
  background: rgba(4, 10, 22, 0.85);
  box-shadow: 0 0 16px rgba(0, 212, 255, 0.1);
}

:deep(.el-input__inner) {
  color: #e2e8f0;
}

:deep(.el-input__inner::placeholder) {
  color: rgba(100, 116, 139, 0.6);
}

:deep(.el-input-group__append, .el-input-group__prepend) {
  padding: 0;
}

/* 分割线测试账号底色 */
:deep(.el-divider__text) {
  background: rgba(4, 10, 22, 0.92);
  padding: 0 12px;
  border-radius: 4px;
}
:deep(.el-divider--horizontal) {
  border-color: rgba(0, 212, 255, 0.2);
}

/* 大屏响应式 */
.back-home {
  text-align: center;
  margin-top: 12px;
}

.back-home a {
  color: #00D4FF;
  font-size: 13px;
  text-decoration: none;
  transition: color 0.2s;
}

.back-home a:hover {
  color: #00FF88;
}

@media screen and (max-width: 1180px) {
  .login-container {
    grid-gap: 9rem;
  }

  .login-form {
    width: 290px;
  }

  .brand-title {
    font-size: 2.4rem;
    margin: 8px 0;
  }

  .img img {
    width: 360px;
  }

  .background-img {
    object-fit: contain;
  }
}

/* 移动端隐藏左侧图片，居中表单 */
@media screen and (max-width: 968px) {
  .img {
    display: none;
  }

  .login-container {
    grid-template-columns: 1fr;
  }

  .login-box {
    justify-content: center;
  }
}
</style>