<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">{{ isEditMode ? "ดู / แก้ไขโต๊ะ" : "เพิ่มโต๊ะ" }}</h1>
        </div>
      </div>
      <Breadcrumbs />
      <div class="card shadow p-4" v-if="isOnMounted">
        <div v-if="tablesStore.error" class="alert alert-danger mt-3">
          {{ tablesStore.error }}
        </div>
        <form @submit.prevent="submitForm">
          <div class="row">
            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="tableName" class="form-label"
                >ชื่อ <span class="text-danger">*</span></label
              >
              <input
                v-model="name"
                type="text"
                id="tableName"
                class="form-control"
                required
              />
            </div>
            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="tableCapacity" class="form-label"
                >จำนวนที่นั่ง <span class="text-danger">*</span></label
              >
              <input
                v-model="capacity"
                type="number"
                id="tableCapacity"
                class="form-control"
                required
              />
            </div>
            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="tableSortOrder" class="form-label">ลำดับ</label>
              <input
                v-model="sort_order"
                type="text"
                id="tableSortOrder"
                class="form-control"
              />
            </div>
            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="tableIs_active" class="form-label"
                >สถานะ <span class="text-danger">*</span></label
              >
              <select
                id="tableIsActive"
                class="form-control"
                v-model="is_active"
                required
              >
                <option :value="true">เปิดใช้งาน</option>
                <option :value="false">ปิดใช้งาน</option>
              </select>
            </div>

            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="tableNote" class="form-label">โน๊ต</label>
              <textarea
                v-model="note"
                id="tableNote"
                class="form-control"
              ></textarea>
            </div>
          </div>

          <div class="text-end">
            <button
              type="submit"
              class="btn btn-success"
              :disabled="tablesStore.loading"
            >
              <span v-if="tablesStore.loading">กำลังบันทึก...</span>
              <span v-else>บันทึก</span>
            </button>
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
  import { useTableStore } from '@/stores/tableStore'
  import { useRouter, useRoute } from 'vue-router'
  import { showSuccess, showError, showLoading, closeSwal } from '@/utils/swal'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import Breadcrumbs from '@/components/Breadcrumbs.vue'

  const tablesStore = useTableStore()
  const router = useRouter()
  const route = useRoute()

  const id = route.params.id
  const isEditMode = computed(() => !!id)
  const isOnMounted = ref(false);

  const name = ref('')
  const capacity = ref('')
  const is_active = ref(true)
  const sort_order = ref()
  const note = ref('')

  onMounted(async() => {
    if (isEditMode.value) {
      let table = tablesStore.tables.find(r => r.id == id)

      if (!table) {
        table = await tablesStore.fetchDataById(id)
      }


      if (table) {
        name.value = table.name
        note.value = table.note
      } else {
        showError('Error', 'Table not found')
        router.push('/admin/tables')
      }
    }
    isOnMounted.value = true
  })

  const submitForm = async () => {
  if (capacity.value <= 0) {
    showError('Error', 'กรุณากรอกจำนวนที่นั่งให้มากกว่า 0')
    return
  }

  const payload = {
    name: name.value,
    capacity: capacity.value,
    is_active: is_active.value,
    sort_order: sort_order.value,
    note: note.value,
  }

  showLoading()
  if (isEditMode.value) {
    await tablesStore.editData(id, payload)
  } else {
    await tablesStore.createData(payload)
  }

  if (!tablesStore.error) {
    closeSwal()
    showSuccess(`Table ${isEditMode.value ? 'updated' : 'created'} successfully`)
    router.push('/admin/tables')
  } else {
    closeSwal()
    showError('Error', tablesStore.error)
    return
  }
}
</script>
