<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">คำสั่งซื้อ</h1>
        </div>
      </div>
      <Breadcrumbs />
      <!-- Search & Add Button -->
      <div class="row align-items-center mb-4">
        <div class="col-md-2">
          <select id="orderStatus" class="form-select" required v-model="searchStatus" @change="fetchOrders">
            <option value="">ทั้งหมด</option>
            <option
              v-for="status in ordersStore.listStatus"
              :key="status"
              :value="status"
            >
              {{ status }}
            </option>
          </select>
        </div>

        <div class="col-md-4">
          <SearchBox
            v-model="search"
            placeholder="Search Orders by ID or Name..."
            @search="handleSearch"
          />
        </div>

        <div
          class="col-md-4 d-flex justify-content-md-end justify-content-start mt-2 mt-md-0 ms-md-auto"
          v-if="permissionSet.has('Order.Create')"
        >
          <router-link
            to="/admin/orders/edit"
            class="btn btn-primary shadow-sm"
          >
            <i class="bi bi-plus-lg me-1"></i> เพิ่มคำสั่งซื้อ
          </router-link>
        </div>
      </div>

      <!-- Table Section -->
      <div class="row">
        <div class="col-12">
          <DataTable 
            :data="ordersStore.items"
            :columns="columns"
            :pagination="ordersStore.pagination"
            :current-page="currentPage"
            resource-type="admin/orders"
            :can-edit="permissionSet.has('Order.Update')"
            :can-delete="false"
            :loading="ordersStore.loading"
            @page-changed="handlePageChange"
            @delete-item="deleteOrder">
            <template #column-status="{ value }">
            <span :style="getStatusStyle(value)">
              {{ value }}
            </span>
          </template>
          </DataTable>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import Layout from "@/components/admin/Layout.vue";
import DataTable from "@/components/admin/DataTable.vue";
import SearchBox from "@/components/admin/SearchBox.vue";
import { useOrderStore } from "@/stores/orderStore";
import { useAuthStore } from "@/stores/authStore";
import {
  showSuccessOk,
  showError,
  showLoading,
  closeSwal,
  showConfirm,
} from "@/utils/swal";
import Breadcrumbs from "@/components/Breadcrumbs.vue";

const auth = useAuthStore();
const ordersStore = useOrderStore();
const permissionSet = computed(() => new Set(auth.user?.permissions));

const searchStatus = ref("");
const search = ref("");
const currentPage = ref(1);
const pageSize = ref(10);

const columns = [
  { label: "ID", key: "id" },
  { label: "Table ID", key: "table_id" },
  { label: 'สถานะ', key: 'status', slot: true },
  { label: "เวลาที่จอง", key: "reserved_at" },
  { label: "เวลาเริ่ม", key: "started_at" },
  { label: "เวลาสิ้นสุด", key: "ended_at" },
  { label: "ราคา", key: "total_price" },
];

onMounted(async () => {
  await fetchOrders();
});

watch(currentPage, async () => {
  await fetchOrders();
});

const fetchOrders = async () => {
  await ordersStore.fetchData({
    page: currentPage.value,
    per_page: pageSize.value,
    search: search.value,
    status: searchStatus.value,
  });
};

const handleSearch = async () => {
  currentPage.value = 1;
  await fetchOrders();
};

const handlePageChange = async (page) => {
  currentPage.value = page;
};

const getStatusStyle = (status) => {
  switch ((status || '').toLowerCase()) {
    case 'pending':
      return `color: #ffc107; font-weight: bold;`;
    case 'reserved':
      return `color: #17a2b8; font-weight: bold;`;
    case 'active':
      return `color: #28a745; font-weight: bold;`;
    case 'completed':
      return `color: #007bff; font-weight: bold;`;
    case 'cancelled':
      return `color: #dc3545; font-weight: bold;`;
    default:
      return `color: #6c757d; font-weight: bold;`;
  }
};

const deleteOrder = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await ordersStore.deleteData(id);
    if (ordersStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", ordersStore.error);
      return;
    }
    closeSwal();
    await auth.fetchProfile();
    await fetchOrders();
    showSuccessOk("ลบข้อมูลสำเร็จ");
  }
};
</script>
