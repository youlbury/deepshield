import { reactive } from 'vue'

export const authState = reactive({
  isLoggedIn: localStorage.getItem('isLoggedIn') === 'true'
})

export function login(username) {
  localStorage.setItem('isLoggedIn', 'true')
  localStorage.setItem('username', username)
  authState.isLoggedIn = true
}

export function logout() {
  localStorage.removeItem('isLoggedIn')
  localStorage.removeItem('username')
  authState.isLoggedIn = false
}
