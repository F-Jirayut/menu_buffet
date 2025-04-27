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
          <SearchBox
            v-model="search"
            placeholder="Search Permissions by ID or Name..."
            @search="handleSearch"
          />
        </div>
        <div
          class="col-md-4 text-md-end text-start mt-2 mt-md-0"
          v-if="permissionSet.has('Permission.Create')"
        >
          <router-link
            to="/admin/permissions/edit"
            class="btn btn-primary shadow-sm"
          >
            <i class="bi bi-plus-lg me-1"></i> Add Permissions
          </router-link>
        </div>
      </div>

      <!-- Table Section -->
      <div class="row">
        <div class="col-12">
          <DataTable
            :data="permissionsStore.permissions"
            :columns="columns"
            :pagination="permissionsStore.pagination"
            :current-page="currentPage"
            resource-type="admin/permissions"
            :can-edit="permissionSet.has('Permission.Update')"
            :can-delete="permissionSet.has('Permission.Delete')"
            @page-changed="handlePageChange"
            @delete-item="deletePermission"
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
import { usePermissionStore } from "@/stores/permissionStore";
import { useAuthStore } from "@/stores/authStore";
import {
  showSuccessOk,
  showError,
  showLoading,
  closeSwal,
  showConfirm,
} from "@/utils/swal";

const auth = useAuthStore();
const permissionsStore = usePermissionStore();
const permissionSet = computed(() => new Set(auth.user?.permissions));

const search = ref("");
const currentPage = ref(1);
const pageSize = ref(10);

const columns = [
  { label: "ID", key: "id" },
  { label: "Name", key: "name" },
];

onMounted(async () => {
  await fetchPermissions();
});

watch(currentPage, async () => {
  await fetchPermissions();
});

const fetchPermissions = async () => {
  await permissionsStore.fetchData(
    currentPage.value,
    pageSize.value,
    search.value
  );
};

const handleSearch = async () => {
  currentPage.value = 1;
  await fetchPermissions();
};

const handlePageChange = async (page) => {
  currentPage.value = page;
};

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
    await auth.fetchProfile();
    await fetchPermissions();
    showSuccessOk("ลบข้อมูลสำเร็จ");
  }
};
</script>
