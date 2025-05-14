<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">ลูกค้า</h1>
        </div>
      </div>
      <Breadcrumbs />
      <!-- Search & Add Button -->
      <div class="row align-items-center mb-4">
        <div class="col-md-8">
          <SearchBox
            v-model="search"
            placeholder="Search Customers by ID, Name, Email, Phone..."
            @search="handleSearch"
          />
        </div>
        <div
          class="col-md-4 text-md-end text-start mt-2 mt-md-0"
          v-if="permissionSet.has('Customer.Create')"
        >
          <router-link
            to="/admin/customers/edit"
            class="btn btn-primary shadow-sm"
          >
            <i class="bi bi-plus-lg me-1"></i> เพิ่มลูกค้า
          </router-link>
        </div>
      </div>

      <!-- Table Section -->
      <div class="row">
        <div class="col-12">
          <DataTable
            :data="customersStore.items"
            :columns="columns"
            :pagination="customersStore.pagination"
            :current-page="currentPage"
            resource-type="admin/customers"
            :can-edit="permissionSet.has('Customer.Update')"
            :can-delete="permissionSet.has('Customer.Delete')"
            :loading="customersStore.loading"
            @page-changed="handlePageChange"
            @delete-item="deleteCustomer"
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
import { useCustomerStore } from "@/stores/customerStore";
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
const customersStore = useCustomerStore();
const permissionSet = computed(() => new Set(auth.user?.permissions));

const search = ref("");
const currentPage = ref(1);
const pageSize = ref(10);

const columns = [
  { label: "ID", key: "id" },
  { label: "ชื่อ", key: "name" },
  { label: "อีเมล์", key: "email" },
  { label: "เบอร์โทร", key: "phone" },
];

onMounted(async () => {
  await fetchCustomers();
});

watch(currentPage, async () => {
  await fetchCustomers();
});

const fetchCustomers = async () => {
  await customersStore.fetchData({
    page: currentPage.value,
    per_page: pageSize.value,
    search: search.value
  });
  console.log(customersStore.items)
};

const handleSearch = async () => {
  currentPage.value = 1;
  await fetchCustomers();
};

const handlePageChange = async (page) => {
  currentPage.value = page;
};

const deleteCustomer = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await customersStore.deleteData(id);
    if (customersStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", customersStore.error);
      return;
    }
    closeSwal();
    await auth.fetchProfile();
    await fetchCustomers();
    showSuccessOk("ลบข้อมูลสำเร็จ");
  }
};
</script>
