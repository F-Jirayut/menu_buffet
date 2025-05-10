import { defineStore } from 'pinia'
import { login as loginService, getProfile } from '@/services/authService'
import axios from 'axios'
import { decodePayloadToken } from '@/utils/jwt'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const access_token = ref(null)
  const error = ref(null)
  const loading = ref(false)

  const login = async (username, password) => {
    loading.value = true
    error.value = null
    try {
      const res = await loginService(username, password)
      const { data } = res.data
      access_token.value = data.access_token

      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token.value}`

      const payload = decodePayloadToken(access_token.value)
      user.value = {
        id: payload.id,
        username: payload.username,
        role_id: payload.role_id,
        role_name: payload.role_name,
        permissions: payload.permissions || [],
      }

      localStorage.setItem('access_token', access_token.value)
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Login failed'
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    access_token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    delete axios.defaults.headers.common['Authorization']
  }

  const fetchProfile = async () => {
    loading.value = true
    error.value = null
    try {
      const res = await getProfile()
      user.value = res.data.data
      return res.data.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch profile'
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    access_token,
    error,
    loading,
    login,
    logout,
    fetchProfile,
  }
}, {
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'auth',
        storage: localStorage,
        paths: ['access_token', 'user'],
      },
    ],
  },
})
