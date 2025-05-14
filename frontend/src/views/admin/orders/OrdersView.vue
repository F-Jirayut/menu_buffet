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
        <div class="col-md-8">
          <SearchBox
            v-model="search"
            placeholder="Search Orders by ID or Name..."
            @search="handleSearch"
          />
        </div>
        <div
          class="col-md-4 text-md-end text-start mt-2 mt-md-0"
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
            :can-delete=false
            :loading="ordersStore.loading"
            @page-changed="handlePageChange"
            @delete-item="deleteOrder"
          />
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

const search = ref("");
const currentPage = ref(1);
const pageSize = ref(10);

const columns = [
  { label: "ID", key: "id" },
  { label: "Table ID", key: "table_id" },
  { label: "สถานะ", key: "status" },
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
    search: search.value
  });
  console.log(ordersStore.items)
};

const handleSearch = async () => {
  currentPage.value = 1;
  await fetchOrders();
};

const handlePageChange = async (page) => {
  currentPage.value = page;
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
