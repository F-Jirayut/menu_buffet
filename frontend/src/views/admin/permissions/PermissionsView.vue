<template>
    <Layout>
      <div class="container-fluid">
        <div class="row mb-4">
          <div class="col-12">
            <h1 class="text-left">Permissions Management</h1>
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
              placeholder="Search Permissions by name..."
            />
          </div>
        </div>
        <div class="col-md-4 text-md-end text-start mt-2 mt-md-0" v-if="permissionSet.has('Permission.Create')">
          <router-link to="/admin/permissions/edit" class="btn btn-primary shadow-sm">
            <i class="bi bi-plus-lg me-1"></i> Add Permissions
          </router-link>
        </div>
      </div>
  
        <!-- Section: Table -->
        <div class="row">
          <div class="col-12">
            <div class="card shadow p-4">
              <!-- <h2 class="text-center mb-4">Permissions</h2> -->
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
                    v-for="permission in filteredPermissions"
                    :key="permission.id"
                  >
                    <td>{{ permission.id }}</td>
                    <td>{{ permission.name }}</td>
                    <td>
                      <div v-if="permission.name !== 'root' && permission.name !== 'admin'">
                        <router-link v-if="permissionSet.has('Permission.Update')" :to="`/admin/permissions/edit/${permission.id}`" class="btn btn-warning btn-sm me-2">Edit</router-link>
                        <button v-if="permissionSet.has('Permission.Delete')" class="btn btn-danger btn-sm" @click="deletePermission(permission.id)">Delete</button>
                      </div>
                    </td>
                  </tr>
                  <!-- <tr v-if="filteredPermissions.length === 0">
                    <td colspan="3" class="text-center">Data not found.</td>
                  </tr> -->
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
  import { usePermissionStore } from '@/stores/permissionStore'
  import { showSuccessOk, showError, showLoading, closeSwal, showConfirm } from '@/utils/swal'
  import { useAuthStore } from '@/stores/authStore'

  const auth = useAuthStore()
  const permissionsStore = usePermissionStore()
  const permissionSet = computed(() => {
    return new Set(auth.user?.permissions)
  })
  const search = ref('')
  
  onMounted(async () => {
    await permissionsStore.fetchData()
  })
  
  const filteredPermissions = computed(() => {
    return permissionsStore.permissions.filter((permission) =>
        permission.name.toLowerCase().includes(search.value.toLowerCase())
    )
  })
  
  const deletePermission = async (id) => {
    const confirmed = await showConfirm('คุณต้องการลบข้อมูลนี้หรือไม่?')

    if (confirmed.isConfirmed) {
        showLoading()
        await permissionsStore.deleteData(id)
        if (permissionsStore.error) {
            closeSwal()
            showError('ลบข้อมูลไม่สำเร็จ', permissionsStore.error)
            return
        }
        closeSwal()
        await auth.fetchProfile()
        showSuccessOk('ลบข้อมูลสำเร็จ')
    }
  }
  </script>
  