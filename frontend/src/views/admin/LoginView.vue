<template>
    <div class="d-flex align-items-center justify-content-center min-vh-100 bg-dark text-white">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-12 col-sm-12 col-md-8 col-lg-7 col-xl-6 col-xxl-6">
            <div class="card bg-secondary text-white shadow p-4">
              <h2 class="text-center mb-4">Login</h2>
              <form @submit.prevent="handleSubmit">
                <div class="mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input type="text" v-model="username" class="form-control bg-dark text-white border-secondary" id="username" required autocomplete="off">
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" v-model="password" class="form-control bg-dark text-white border-secondary" id="password" required>
                </div>
              <br>

                <button type="submit" class="btn btn-outline-light w-100" v-bind:disabled="auth.loading">
                  <span v-if="auth.loading">Loading ...</span>
                  <span v-else>Login</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
    import { ref, onMounted } from 'vue'
    import { useAuthStore } from '@/stores/authStore'
    import { useRouter } from 'vue-router'
    import { showLoading, closeSwal, showSuccess, showError } from '@/utils/swal'
  
    const router = useRouter()
    const auth = useAuthStore()
  
    const username = ref('')
    const password = ref('')

    // const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))
  
    const handleSubmit = async () => {
        showLoading()
        await auth.login(username.value, password.value)
        // await delay(2000) // Simulate a delay of 2 seconds
        closeSwal()
        if (!auth.error) {
            showSuccess('เข้าสู่ระบบสำเร็จ')
            router.push('/admin/dashboard')
        } else {
            showError('เข้าสู่ระบบล้มเหลว', auth.error)
        }
    }
</script>
  
  