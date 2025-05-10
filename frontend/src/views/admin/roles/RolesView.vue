<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">บทบาท</h1>
        </div>
      </div>
      <Breadcrumbs />
      <!-- Search & Add Button -->
      <div class="row align-items-center mb-4">
        <div class="col-md-8">
          <SearchBox
            v-model="search"
            placeholder="Search Roles by ID or Name..."
            @search="handleSearch"
          />
        </div>
        <div
          class="col-md-4 text-md-end text-start mt-2 mt-md-0"
          v-if="permissionSet.has('Role.Create')"
        >
          <router-link
            to="/admin/roles/edit"
            class="btn btn-primary shadow-sm"
          >
            <i class="bi bi-plus-lg me-1"></i> เพิ่มบทบาท
          </router-link>
        </div>
      </div>

      <!-- Table Section -->
      <div class="row">
        <div class="col-12">
          <DataTable
            :data="rolesStore.items"
            :columns="columns"
            :pagination="rolesStore.pagination"
            :current-page="currentPage"
            resource-type="admin/roles"
            :can-edit="permissionSet.has('Role.Update')"
            :can-delete="permissionSet.has('Role.Delete')"
            :loading="rolesStore.loading"
            @page-changed="handlePageChange"
            @delete-item="deleteRole"
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
import { useRoleStore } from "@/stores/roleStore";
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
const rolesStore = useRoleStore();
const permissionSet = computed(() => new Set(auth.user?.permissions));

const search = ref("");
const currentPage = ref(1);
const pageSize = ref(10);

const columns = [
  { label: "ID", key: "id" },
  { label: "Name", key: "name" },
];

onMounted(async () => {
  await fetchRoles();
});

watch(currentPage, async () => {
  await fetchRoles();
});

const fetchRoles = async () => {
  await rolesStore.fetchData({
    page: currentPage.value,
    per_page: pageSize.value,
    search: search.value
  });
};

const handleSearch = async () => {
  currentPage.value = 1;
  await fetchRoles();
};

const handlePageChange = async (page) => {
  currentPage.value = page;
};

const deleteRole = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await rolesStore.deleteData(id);
    if (rolesStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", rolesStore.error);
      return;
    }
    closeSwal();
    await auth.fetchProfile();
    await fetchRoles();
    showSuccessOk("ลบข้อมูลสำเร็จ");
  }
};
</script>
