import { defineStore } from 'pinia'
import { login as loginService, getProfile } from '@/services/authService'
import axios from 'axios'
import { decodePayloadToken } from '@/utils/jwt'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    access_token: null,
    error: null,
    loading: false,
  }),
  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null
      try {
        const res = await loginService(username, password)
        const { success, message, data } = res.data;
        this.access_token = data.access_token
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.access_token}`
        const payload = decodePayloadToken(this.access_token)
        this.user = {
            id: payload.id,
            username: payload.username,
            role_id: payload.role_id,
            role_name: payload.role_name,
            permissions: payload.permissions || [],
        }
        localStorage.setItem('access_token', this.access_token)
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Login failed';
      } finally {
        this.loading = false
      }
    },
    async logout() {
        this.access_token = null
        this.user = null
        localStorage.removeItem('access_token')
        delete axios.defaults.headers.common['Authorization']
    },
    async fetchProfile() {
      this.loading = true
      this.error = null
      try {
        const res = await getProfile()
        const { success, message, data } = res.data
        this.user = data
        return data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to fetch profile';
      } finally {
        this.loading = false
      }
    },
  },
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