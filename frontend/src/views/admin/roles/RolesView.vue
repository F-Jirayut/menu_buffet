<template>
    <Layout>
      <div class="container-fluid">
        <div class="row mb-4">
          <div class="col-12">
            <h1 class="text-left">Roles Management</h1>
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
              placeholder="Search roles by name..."
            />
          </div>
        </div>
        <div class="col-md-4 text-md-end text-start mt-2 mt-md-0" v-if="permissionSet.has('Role.Create')">
          <router-link to="/admin/roles/edit" class="btn btn-primary shadow-sm">
            <i class="bi bi-plus-lg me-1"></i> Add Role
          </router-link>
        </div>
      </div>
  
        <!-- Section: Table -->
        <div class="row">
          <div class="col-12">
            <div class="card shadow p-4">
              <table class="table table-bordered">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="role in filteredRoles"
                    :key="role.id"
                  >
                    <td>{{ role.id }}</td>
                    <td>{{ role.name }}</td>
                    <td>
                        <router-link
                        v-if="permissionSet.has('Role.Update')"
                        :to="`/admin/roles/edit/${role.id}`"
                        class="btn btn-warning btn-sm me-2"
                        >
                        Edit
                        </router-link>
                        <button
                        v-if="permissionSet.has('Role.Update')"
                        class="btn btn-danger btn-sm"
                        @click="deleteRole(role.id)"
                        >
                        Delete
                        </button>
                    </td>
                  </tr>
                  <tr v-if="filteredRoles.length === 0">
                    <td colspan="3" class="text-center">Data not found.</td>
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
  import { useRoleStore } from '@/stores/roleStore'
  import { showSuccessOk, showLoading, closeSwal, showConfirm } from '@/utils/swal'
  import { useAuthStore } from '@/stores/authStore';
  
  const auth = useAuthStore()
  const rolesStore = useRoleStore()
  const search = ref('')
  const permissionSet = computed(() => {
    return new Set(auth.user?.permissions)
  })
  
  onMounted(async () => {
    await rolesStore.fetchData()
  })
  
  const filteredRoles = computed(() => {
    return rolesStore.roles.filter((role) =>
        role.name.toLowerCase().includes(search.value.toLowerCase())
    )
  })
  
  const deleteRole = async (id) => {
    const confirmed = await showConfirm('คุณต้องการลบข้อมูลนี้หรือไม่?')

    if (confirmed.isConfirmed) {
        showLoading()
        await rolesStore.deleteData(id)
        if (rolesStore.error) {
            closeSwal()
            showError('ลบข้อมูลไม่สำเร็จ', rolesStore.error)
            return
        }
        closeSwal()
        await auth.fetchProfile()
        showSuccessOk('ลบข้อมูลสำเร็จ')
    }
  }
  </script>
  