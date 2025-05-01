<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">อาหาร - ประเภท</h1>
        </div>
      </div>
      <Breadcrumbs />

      <!-- Search & Add Button -->
      <div class="row align-items-center mb-4">
        <div class="col-md-8">
          <SearchBox
            v-model="search"
            placeholder="Search Categories by ID or Name..."
            @search="handleSearch"
          />
        </div>
        <div
          class="col-md-4 text-md-end text-start mt-2 mt-md-0"
          v-if="permissionSet.has('Category.Create')"
        >
          <router-link
            to="/admin/foods/categories/edit"
            class="btn btn-primary shadow-sm"
          >
            <i class="bi bi-plus-lg me-1"></i> เพิ่มประเภท
          </router-link>
        </div>
      </div>

      <!-- Table Section -->
      <div class="row">
        <div class="col-12">
          <DataTable
            :data="menuCategoriesStore.menuCategories"
            :columns="columns"
            :pagination="menuCategoriesStore.pagination"
            :current-page="currentPage"
            resource-type="admin/foods/categories"
            :can-edit="permissionSet.has('Category.Update')"
            :can-delete="permissionSet.has('Category.Delete')"
            :loading="menuCategoriesStore.loading"
            @page-changed="handlePageChange"
            @delete-item="deleteMenuCategory"
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
import { useMenuCategoriestore } from "@/stores/menuCategoryStore";
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
const menuCategoriesStore = useMenuCategoriestore();
const permissionSet = computed(() => new Set(auth.user?.permissions));

const search = ref("");
const currentPage = ref(1);
const pageSize = ref(10);

const columns = [
  { label: "ID", key: "id" },
  { label: "Name", key: "name" },
];

onMounted(async () => {
  await fetchMenuCategories();
});

watch(currentPage, async () => {
  await fetchMenuCategories();
});

const fetchMenuCategories = async () => {
  await menuCategoriesStore.fetchData(
    currentPage.value,
    pageSize.value,
    search.value
  );
};

const handleSearch = async () => {
  currentPage.value = 1;
  await fetchMenuCategories();
};

const handlePageChange = async (page) => {
  currentPage.value = page;
};

const deleteMenuCategory = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await menuCategoriesStore.deleteData(id);
    if (menuCategoriesStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", menuCategoriesStore.error);
      return;
    }
    closeSwal();
    await auth.fetchProfile();
    await fetchMenuCategories();
    showSuccessOk("ลบข้อมูลสำเร็จ");
  }
};
</script>
