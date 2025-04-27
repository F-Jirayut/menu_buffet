<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12 text-center">
          <h1 class="fw-bold">{{ isEditMode ? 'Edit Role' : 'Create Role' }}</h1>
        </div>
      </div>

      <div class="card shadow-sm p-4">
        <div v-if="rolesStore.error" class="alert alert-danger">
          {{ rolesStore.error }}
        </div>

        <form @submit.prevent="submitForm">
          <div class="row mb-4">
            <div class="col-12 col-md-6">
              <label for="roleName" class="form-label fw-semibold">Role Name</label>
              <input
                v-model="name"
                type="text"
                id="roleName"
                class="form-control"
                placeholder="Enter role name"
                required
                autocomplete="off"
              />
            </div>
          </div>

          <div class="mb-4">
            <h5 class="fw-semibold">Permissions</h5>
            <div class="table-responsive">
              <table class="table table-bordered align-middle">
                <thead class="table-secondary text-center">
                  <tr>
                    <th>Module</th>
                    <th>View</th>
                    <th>Create</th>
                    <th>Update</th>
                    <th>Delete</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(actions, module) in permissionGroups"
                    :key="module"
                    class="text-center"
                  >
                    <td class="fw-medium">{{ module }}</td>
                    <td>
                      <input
                        v-if="actions.includes('View')"
                        type="checkbox"
                        :value="`${module}.View`"
                        v-model="selectedPermissions"
                      />
                    </td>
                    <td>
                      <input
                        v-if="actions.includes('Create')"
                        type="checkbox"
                        :value="`${module}.Create`"
                        v-model="selectedPermissions"
                      />
                    </td>
                    <td>
                      <input
                        v-if="actions.includes('Update')"
                        type="checkbox"
                        :value="`${module}.Update`"
                        v-model="selectedPermissions"
                      />
                    </td>
                    <td>
                      <input
                        v-if="actions.includes('Delete')"
                        type="checkbox"
                        :value="`${module}.Delete`"
                        v-model="selectedPermissions"
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="text-end">
            <button type="submit" class="btn btn-success px-4 py-2" :disabled="rolesStore.loading">
              <span v-if="rolesStore.loading">Saving...</span>
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
import { useRoleStore } from '@/stores/roleStore'
import { usePermissionStore } from '@/stores/permissionStore'
import { useRouter, useRoute } from 'vue-router'
import { showSuccess, showError, showLoading, closeSwal } from '@/utils/swal'
import { useAuthStore } from '@/stores/authStore';
const auth = useAuthStore()

const rolesStore = useRoleStore()
const permissionStore = usePermissionStore()
const router = useRouter()
const route = useRoute()

const id = route.params.id
const isEditMode = computed(() => !!id)

const name = ref('')
const selectedPermissions = ref([])

const permissionGroups = computed(() => {
  return permissionStore.permissionGroups || {}
})

onMounted(async () => {
  await permissionStore.fetchPermissionGroups()
  if (isEditMode.value) {
    const role = await rolesStore.fetchDataById(id, { params: { include: 'permissions' } });
    if (role) {
      name.value = role.name
      selectedPermissions.value = role.permissions?.map(p => p.name) || []
    } else {
      showError('Error', 'Role not found')
      router.push('/admin/roles')
    }
  }
})

const submitForm = async () => {
  const payload = {
    name: name.value,
    permission_names: selectedPermissions.value,
  }
  showLoading()
  if (isEditMode.value) {
    await rolesStore.editData(id, payload)
  } else {
    await rolesStore.createData(payload)
  }
  
  if (!rolesStore.error) {
    closeSwal()
    showSuccess(`Role ${isEditMode.value ? 'updated' : 'created'} successfully`)
    router.push('/admin/roles')
  } else {
    closeSwal()
    showError('Error', rolesStore.error)
  }
}
</script>
