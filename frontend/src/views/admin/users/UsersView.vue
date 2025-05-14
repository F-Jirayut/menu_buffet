<template>
  <Layout>
    <div class="container-fluid">

      <!-- Page Title -->
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">ผู้ใช้งาน</h1>
        </div>
      </div>
      <Breadcrumbs />
      <!-- Search & Add Button -->
      <div class="row align-items-center mb-4">
        <div class="col-md-8">
          <SearchBox
            v-model="search"
            placeholder="Search Users by ID or Name..."
            @search="handleSearch"
          />
        </div>
        <div
          class="col-md-4 text-md-end text-start mt-2 mt-md-0"
          v-if="permissionSet.has('User.Create')"
        >
          <router-link
            to="/admin/users/edit"
            class="btn btn-primary shadow-sm"
          >
            <i class="bi bi-plus-lg me-1"></i> เพิ่มผู้ใช้
          </router-link>
        </div>
      </div>

      <!-- Table Section -->
      <div class="row">
        <div class="col-12">
          <DataTable
            :data="usersStore.items"
            :columns="columns"
            :pagination="usersStore.pagination"
            :current-page="currentPage"
            resource-type="admin/users"
            :can-edit="permissionSet.has('User.Update')"
            :can-delete="permissionSet.has('User.Delete')"
            :loading="usersStore.loading"
            @page-changed="handlePageChange"
            @delete-item="deleteUser"
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
import { useUserStore } from "@/stores/userStore";
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
const usersStore = useUserStore();
const permissionSet = computed(() => new Set(auth.user?.permissions));

const search = ref("");
const currentPage = ref(1);
const pageSize = ref(10);

const columns = [
  { label: "ID", key: "id" },
  { label: "ชื่อ", key: "name" },
];

onMounted(async () => {
  await fetchUsers();
});

watch(currentPage, async () => {
  await fetchUsers();
});

const fetchUsers = async () => {
  await usersStore.fetchData({
    page: currentPage.value,
    per_page: pageSize.value,
    search: search.value
  });
};

const handleSearch = async () => {
  currentPage.value = 1;
  await fetchUsers();
};

const handlePageChange = async (page) => {
  currentPage.value = page;
};

const deleteUser = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await usersStore.deleteData(id);
    if (usersStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", usersStore.error);
      return;
    }
    closeSwal();
    await auth.fetchProfile();
    await fetchUsers();
    showSuccessOk("ลบข้อมูลสำเร็จ");
  }
};
</script>
