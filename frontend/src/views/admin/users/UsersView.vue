<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="text-left">Users Management</h1>
        </div>
      </div>

      <!-- Search & Add Button -->
      <div class="row align-items-center mb-4">
        <div class="col-md-8">
          <div class="input-group shadow-sm">
            <span class="input-group-text bg-white">
              <i class="bi bi-search"></i>
            </span>
            <input
              v-model="search"
              type="text"
              class="form-control"
              placeholder="Search users by name..."
            />
          </div>
        </div>
        <div class="col-md-4 text-md-end text-start mt-2 mt-md-0" v-if="permissionSet.has('User.Create')">
          <router-link to="/admin/users/edit" class="btn btn-primary shadow-sm">
            <i class="bi bi-plus-lg me-1"></i> Add User
          </router-link>
        </div>
      </div>

      <!-- Section: Table -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow p-4">
            <!-- <h2 class="text-center mb-4">Users</h2> -->
            <table class="table table-bordered">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Role</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="user in filteredUsers"
                  :key="user.id"
                >
                  <td>{{ user.id }}</td>
                  <td>{{ user.name }}</td>
                  <td>{{ user.role?.name || '-' }}</td>
                  <td>
                    <router-link
                      v-if="user.name !== 'Root' && user.username !== 'root' && permissionSet.has('User.Update')"
                      :to="`/admin/users/edit/${user.id}`"
                      class="btn btn-warning btn-sm me-1"
                    >
                      Edit
                    </router-link>
                    <button
                      v-if="user.name !== 'Root' && user.username !== 'root' && permissionSet.has('User.Delete')"
                      class="btn btn-danger btn-sm"
                      @click="deleteUser(user.id)"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
                <tr v-if="filteredUsers.length === 0">
                  <td colspan="5" class="text-center">Data not found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Layout from '@/components/admin/Layout.vue'
import { useUserStore } from '@/stores/userStore'
import { showSuccessOk, showConfirm, showLoading, closeSwal } from '@/utils/swal'
import { useAuthStore } from '@/stores/authStore';

const auth = useAuthStore()
const usersStore = useUserStore()
const search = ref('')
const permissionSet = computed(() => {
  return new Set(auth.user?.permissions)
})

onMounted(async () => {
  await usersStore.fetchData()
})

const filteredUsers = computed(() => {
  return usersStore.users.filter((user) => {
    const q = search.value.toLowerCase()
    return (
      String(user.id).includes(q) ||
      user.name.toLowerCase().includes(q) ||
      user.username.toLowerCase().includes(q) ||
      user.role?.name?.toLowerCase().includes(q)
    )
  })
})


const deleteUser = async (id) => {
  const confirmed = await showConfirm('คุณต้องการลบข้อมูลนี้หรือไม่?')

  if (confirmed.isConfirmed) {
    showLoading()
    await usersStore.deleteData(id)
    if (usersStore.error) {
      closeSwal()
      showError('ลบข้อมูลไม่สำเร็จ', usersStore.error)
      return
    }
    closeSwal()
    showSuccessOk('ลบข้อมูลสำเร็จ')
  }
}
</script>
