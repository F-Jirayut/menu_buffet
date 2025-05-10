<template>
  <Layout>
    <div class="container-fluid">
      <!-- หัวเรื่อง -->
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">โต๊ะ</h1>
        </div>
      </div>
      <Breadcrumbs />

      <!-- Search & Add -->
      <div class="row mb-4 align-items-center">
        <div class="col-md-8">
          <SearchBox
            v-model="search"
            placeholder="Search Tables by ID or Name..."
            @search="handleSearch"
          />
        </div>
        <div
          class="col-md-4 text-md-end text-start mt-2 mt-md-0"
          v-if="permissionSet.has('Table.Create')"
        >
          <router-link to="/admin/tables/edit" class="btn btn-primary">
            <i class="bi bi-plus-lg me-1"></i> เพิ่มโต๊ะ
          </router-link>
        </div>
      </div>

      <LoadingOverlay v-if="tablesStore.loading" />
      <!-- ตารางแสดงโต๊ะอาหาร -->
      <div class="row" v-else>
        <router-link
          :to="`/admin/tables/edit/${table.id}`"
          class="col-sm-6 col-md-4 col-lg-4 mb-4 col-xl-3 col-xxl-2 text-decoration-none"
          v-for="table in tablesStore.items"
          :key="table.name"
        >
          <div
            class="card h-100 text-white border-0 shadow-lg rounded-4 overflow-hidden"
            :style="
              table.is_active
                ? 'background-color: #16a085'
                : 'background-color: #80827d'
            "
          >
            <div class="card-body p-4">
              <div
                class="d-flex justify-content-between align-items-center mb-3"
              >
                <h5 class="card-title m-0">ID: {{ table.id }}</h5>
              </div>
              <div
                class="d-flex justify-content-between align-items-center mb-3"
              >
                <h5 class="card-title m-0">{{ table.name }}</h5>
              </div>
              <p class="card-text mb-2">
                <strong>Capacity:</strong> {{ table.capacity }}
              </p>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import Layout from "@/components/admin/Layout.vue";
import SearchBox from "@/components/admin/SearchBox.vue";
import { useTableStore } from "@/stores/tableStore";
import { useAuthStore } from "@/stores/authStore";
import LoadingOverlay from "@/components/LoadingOverlay.vue";
import Breadcrumbs from "@/components/Breadcrumbs.vue";

const auth = useAuthStore();
const tablesStore = useTableStore();
const permissionSet = computed(() => new Set(auth.user?.permissions));

const search = ref("");

onMounted(async () => {
  await fetchTables();
});

const fetchTables = async () => {
  await tablesStore.fetchData({ search : search.value });
};

const handleSearch = async () => {
  await fetchTables();
};

</script>

<style scoped></style>
