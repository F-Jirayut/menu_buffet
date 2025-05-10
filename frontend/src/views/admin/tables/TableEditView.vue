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

          <div>
            <FormActionButtons
              :isEditMode="isEditMode"
              :loading="tablesStore.loading"
              :id="id"
              :deleteItem="deleteTable"
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
  import { useTableStore } from '@/stores/tableStore'
  import { useRouter, useRoute } from 'vue-router'
  import { showSuccess, showError, showLoading, closeSwal, showSuccessOk, showConfirm } from '@/utils/swal'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import Breadcrumbs from '@/components/Breadcrumbs.vue'
import FormActionButtons from '@/components/FormActionButtons.vue'

  const tablesStore = useTableStore()
  const router = useRouter()
  const route = useRoute()

  const id = route.params.id
  const isEditMode = computed(() => !!id)
  const isOnMounted = ref(false);

  const name = ref('')
  const capacity = ref()
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
        capacity.value = table.capacity
        sort_order.value = table.sort_order
        is_active.value = table.is_active
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
    note: note.value,
  }

  if (
    sort_order.value !== null &&
    sort_order.value !== undefined &&
    sort_order.value !== ""
  ) {
    payload['sort_order'] = sort_order.value
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

const deleteTable = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await tablesStore.deleteData(id);
    if (tablesStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", tablesStore.error);
      return;
    }
    closeSwal();
    showSuccessOk("ลบข้อมูลสำเร็จ");
    router.push("/admin/tables");
  }
};

</script>
