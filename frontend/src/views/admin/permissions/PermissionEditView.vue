<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">{{ isEditMode ? 'ดู / แก้ไขสิทธิ์การใช้งาน' : 'เพิ่มสิทธิ์การใช้งาน' }}</h1>
        </div>
      </div>
      <Breadcrumbs />
      <div class="card shadow p-4" v-if="isOnMounted">
        <div v-if="permissionsStore.error" class="alert alert-danger mt-3">
          {{ permissionsStore.error }}
        </div>
        <form @submit.prevent="submitForm">
          <div class="row">
            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="permissionName" class="form-label">ชื่อ <span class="text-danger">*</span></label>
              <input
                v-model="name"
                type="text"
                id="permissionName"
                class="form-control"
                required
              />
            </div>
            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="permissionName" class="form-label">รายละเอียด</label>
              <textarea
                v-model="description"
                id="permissionDescription"
                class="form-control"
              ></textarea>
            </div>
          </div>

          <div>
            <FormActionButtons
              :isEditMode="isEditMode"
              :loading="permissionsStore.loading"
              :id="id"
              :deleteItem="deletePermission"
            />
          </div>

        </form>
      </div>
      <LoadingOverlay v-else />
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import Layout from '@/components/admin/Layout.vue'
import { usePermissionStore } from '@/stores/permissionStore'
import { useRouter, useRoute } from 'vue-router'
import { showSuccess, showError, showLoading, closeSwal, showConfirm, showSuccessOk } from '@/utils/swal'
import FormActionButtons from '@/components/FormActionButtons.vue';
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import Breadcrumbs from '@/components/Breadcrumbs.vue'

const permissionsStore = usePermissionStore()
const router = useRouter()
const route = useRoute()

const id = route.params.id
const isEditMode = computed(() => !!id)

const name = ref('')
const description = ref('')
const isOnMounted = ref(false);

onMounted(async() => {
  if (isEditMode.value) {
    let permission = permissionsStore.permissions.find(r => r.id == id)

    if (!permission) {
      permission = await permissionsStore.fetchDataById(id)
    }


    if (permission) {
      name.value = permission.name
      description.value = permission.description
    } else {
      showError('Error', 'Permission not found')
      router.push('/admin/permissions')
    }
  }
  isOnMounted.value = true
})

const validateName = (name) => {
  const pattern = /\.(View|Create|Update|Delete)$/ // ต้องลงท้ายด้วย .View, .Create, .Update, .Delete
  return pattern.test(name)
}

const submitForm = async () => {
  const payload = {
    name: name.value,
    description: description.value,
  }

  if (!validateName(name.value)) {
    showError('Invalid Name', 'Name must end with .View, .Create, .Update, or .Delete')
    return
  }

  showLoading()
  if (isEditMode.value) {
    await permissionsStore.editData(id, payload)
  } else {
    await permissionsStore.createData(payload)
  }
  if (!permissionsStore.error) {
    closeSwal()
    showSuccess(`Permission ${isEditMode.value ? 'updated' : 'created'} successfully`)
    router.push('/admin/permissions')
  } else {
    closeSwal()
    showError('Error', permissionsStore.error)
    return
  }
}

const deletePermission = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await permissionsStore.deleteData(id);
    if (permissionsStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", permissionsStore.error);
      return;
    }
    closeSwal();
    router.push('/admin/permissions')
    showSuccessOk("ลบข้อมูลสำเร็จ");
  }
};

</script>
