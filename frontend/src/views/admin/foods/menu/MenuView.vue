<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">อาหาร - เมนู</h1>
        </div>
      </div>
      <Breadcrumbs />

      <!-- Search & Add Button -->
      <div class="row align-items-center mb-4">
        <div class="col-md-8">
          <SearchBox
            v-model="search"
            placeholder="Search Menus by ID or Name..."
            @search="handleSearch"
          />
        </div>
        <div
          class="col-md-4 text-md-end text-start mt-2 mt-md-0"
          v-if="permissionSet.has('Menu.Create')"
        >
          <router-link
            to="/admin/foods/menus/edit"
            class="btn btn-primary shadow-sm"
          >
            <i class="bi bi-plus-lg me-1"></i> เพิ่มเมนู
          </router-link>
        </div>
      </div>

      <!-- Table Section -->
      <div class="row">
        <div class="col-12">
          <DataTable
            :data="menusStore.menus"
            :columns="columns"
            :pagination="menusStore.pagination"
            :current-page="currentPage"
            resource-type="admin/foods/menus"
            :can-edit="permissionSet.has('Menu.Update')"
            :can-delete="permissionSet.has('Menu.Delete')"
            :loading="menusStore.loading"
            @page-changed="handlePageChange"
            @delete-item="deleteMenu"
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
import { useMenuStore } from "@/stores/menuStore";
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
const menusStore = useMenuStore();
const permissionSet = computed(() => new Set(auth.user?.permissions));

const search = ref("");
const currentPage = ref(1);
const pageSize = ref(10);

const columns = [
  { label: "ID", key: "id" },
  { label: "Name", key: "name" },
];

onMounted(async () => {
  await fetchMenus();
});

watch(currentPage, async () => {
  await fetchMenus();
});

const fetchMenus = async () => {
  await menusStore.fetchData(
    currentPage.value,
    pageSize.value,
    search.value
  );
};

const handleSearch = async () => {
  currentPage.value = 1;
  await fetchMenus();
};

const handlePageChange = async (page) => {
  currentPage.value = page;
};

const deleteMenu = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await menusStore.deleteData(id);
    if (menusStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", menusStore.error);
      return;
    }
    closeSwal();
    await auth.fetchProfile();
    await fetchMenus();
    showSuccessOk("ลบข้อมูลสำเร็จ");
  }
};
</script>
