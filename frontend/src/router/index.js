import { createRouter, createWebHistory } from 'vue-router'
import LoginNew from '../views/LoginNew.vue'
import Home from '../views/Home.vue'
import ImageDetect from '../views/ImageDetect.vue'
import VideoDetect from '../views/VideoDetect.vue'
import AudioDetect from '../views/AudioDetect.vue'
import Forensics from '../views/Forensics.vue'
import RiskAnalysis from '../views/RiskAnalysis.vue'
import ModelLab from '../views/ModelLab.vue'
import PerformanceEvaluation from '../views/PerformanceEvaluation.vue'
import EvidenceVerify from '../views/EvidenceVerify.vue'
import About from '../views/About.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: LoginNew },
  { path: '/image', name: 'ImageDetect', component: ImageDetect, meta: { requiresAuth: true } },
  { path: '/video', name: 'VideoDetect', component: VideoDetect, meta: { requiresAuth: true } },
  { path: '/audio', name: 'AudioDetect', component: AudioDetect, meta: { requiresAuth: true } },
  { path: '/forensics', name: 'Forensics', component: Forensics, meta: { requiresAuth: true } },
  { path: '/risk', name: 'RiskAnalysis', component: RiskAnalysis, meta: { requiresAuth: true } },
  { path: '/models', name: 'ModelLab', component: ModelLab, meta: { requiresAuth: true } },
  { path: '/benchmark', name: 'PerformanceEvaluation', component: PerformanceEvaluation, meta: { requiresAuth: true } },
  { path: '/verify', name: 'EvidenceVerify', component: EvidenceVerify, meta: { requiresAuth: true } },
  { path: '/about', name: 'About', component: About, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router