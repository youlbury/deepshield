// API 配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

// 确保 URL 格式正确
export const getApiUrl = (path) => {
  // 如果 path 已经以 /api 开头
  if (path.startsWith('/api')) {
    // 如果配置了完整的基础 URL（生产环境）
    if (API_BASE_URL && !API_BASE_URL.startsWith('/')) {
      return `${API_BASE_URL}${path.replace('/api', '')}`
    }
    // 否则使用相对路径（开发环境代理）
    return path
  }
  // 其他路径
  if (API_BASE_URL && !API_BASE_URL.startsWith('/')) {
    return `${API_BASE_URL}${path}`
  }
  return path
}

// 通用请求函数
export const apiRequest = async (url, options = {}) => {
  const fullUrl = getApiUrl(url)
  
  try {
    const response = await fetch(fullUrl, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('API Request Error:', error)
    throw error
  }
}
