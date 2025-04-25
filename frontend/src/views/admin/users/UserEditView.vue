<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="text-center">{{ isEditMode ? 'Edit User' : 'Create User' }}</h1>
        </div>
      </div>

      <div class="card shadow p-4">
        <div v-if="usersStore.error" class="alert alert-danger mt-3">
          {{ usersStore.error }}
        </div>

        <form @submit.prevent="submitForm">
          <div class="row">
            <!-- Name -->
            <div class="mb-3 col-12 col-xl-6">
              <label for="name" class="form-label">Name</label>
              <input
                v-model="name"
                type="text"
                id="name"
                class="form-control"
                placeholder="Enter user name"
                required
                autocomplete="off"
              />
            </div>

            <!-- Username -->
            <div class="mb-3 col-12 col-xl-6">
              <label for="username" class="form-label">Username</label>
              <input
                v-model="username"
                type="text"
                id="username"
                class="form-control"
                placeholder="Enter unique username"
                required
                autocomplete="off"
              />
            </div>

            <div class="mb-3 col-12 col-xl-6">
              <label for="password" class="form-label">Password</label>
              <input
                v-model="password"
                type="password"
                id="password"
                class="form-control"
                :required="!isEditMode"
                placeholder="Enter password"
              />
            </div>

            <div class="mb-3 col-12 col-xl-6">
              <label for="confirmPassword" class="form-label">Confirm Password</label>
              <input
                v-model="confirmPassword"
                type="password"
                id="confirmPassword"
                class="form-control"
                :required="!isEditMode"
                placeholder="Re-enter password"
              />
            </div>

            <!-- Role -->
            <div class="mb-3 col-12 col-xl-6">
              <label for="role" class="form-label">Role</label>
              <select
                v-model="role_id"
                id="role"
                class="form-select"
                required
              >
                <option disabled value="">-- Select Role --</option>
                <option
                  v-for="role in roleSelectOption"
                  :key="role.id"
                  :value="role.id"
                >
                  {{ role.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="text-end mt-4">
            <button
              type="submit"
              class="btn btn-success"
              :disabled="usersStore.loading"
            >
              <span v-if="usersStore.loading">Saving...</span>
              <span v-else>Save</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import Layout from '@/components/admin/Layout.vue'
import { useUserStore } from '@/stores/userStore'
import { useRouter, useRoute } from 'vue-router'
import { showSuccess, showError } from '@/utils/swal'
import { getRoles } from '@/services/roleService'

const usersStore = useUserStore()
const router = useRouter()
const route = useRoute()

const id = route.params.id
const isEditMode = computed(() => !!id)

const roleSelectOption = ref([])

const name = ref('')
const username = ref('')
const role_id = ref('')
const password = ref('')
const confirmPassword = ref('')

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

onMounted(async () => {

  if (isEditMode.value) {
    let user = usersStore.users.find(u => u.id == id)
    if (!user) {
      user = await usersStore.fetchDataById(id)
    }

    if (user) {
      name.value = user.name
      username.value = user.username
      role_id.value = user.role?.id || ''
    } else {
      showError('Error', 'User not found')
      router.push('/admin/users')
    }
  }

  const response = await getRoles()
  const { data } = response.data
  roleSelectOption.value = data
})

const submitForm = async () => {
  if (!isEditMode.value && password.value !== confirmPassword.value) {
    showError('Error', 'Passwords do not match')
    return
  }

  const payload = {
    name: name.value,
    username: username.value,
    role_id: role_id.value,
  }

  if (password.value) {
    payload.password = password.value
  }

  if (isEditMode.value) {
    await usersStore.editData(id, payload)
  } else {
    await usersStore.createData(payload)
  }

  if (!usersStore.error) {
    showSuccess(`User ${isEditMode.value ? 'updated' : 'created'} successfully`)
    router.push('/admin/users')
  } else {
    showError('Error', usersStore.error)
  }
}

</script>
