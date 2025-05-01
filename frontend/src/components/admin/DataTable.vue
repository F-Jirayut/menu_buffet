<template>
  <div class="card shadow p-4">
    <LoadingOverlay v-if="loading" />
    <!-- แสดง loading -->

    <template v-else>
      <table class="table table-bordered table-responsive">
        <thead class="table-light">
          <tr>
            <th v-for="(column, index) in columns" :key="index">
              {{ column.label }}
            </th>
            <th v-if="!noActions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in data" :key="index">
            <td v-for="(column, columnIndex) in columns" :key="columnIndex">
              {{ item[column.key] }}
            </td>
            <td v-if="!noActions">
              <div>
                <router-link
                  v-if="canEdit"
                  :to="`/${resourceType}/edit/${item.id}`"
                  class="btn btn-warning btn-sm me-2"
                >
                  ดู / แก้ไข
                </router-link>
                <button
                  v-if="canDelete"
                  class="btn btn-danger btn-sm"
                  @click="deleteItem(item.id)"
                >
                  ลบ
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="data.length === 0">
            <td
              :colspan="columns.length + (noActions ? 0 : 1)"
              class="text-center"
            >
              ไม่พบข้อมูล
            </td>
          </tr>
        </tbody>
      </table>

      <Pagination
        v-if="pagination"
        :pagination="pagination"
        :current-page="computedCurrentPage"
        :page-size="computedPageSize"
        @page-changed="onPageChanged"
      />
    </template>
  </div>
</template>

<script setup>
import { computed } from "vue";
import Pagination from "@/components/admin/Pagination.vue";
import LoadingOverlay from "@/components/LoadingOverlay.vue";

const props = defineProps({
  data: { type: Array, required: true },
  columns: { type: Array, required: true },
  resourceType: { type: String, required: true },
  pagination: { type: Object },
  currentPage: { type: Number },
  canEdit: { type: Boolean, default: false },
  canDelete: { type: Boolean, default: false },
  noActions: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
});

const emit = defineEmits(["page-changed", "delete-item"]);

const computedCurrentPage = computed(
  () => props.currentPage ?? props.pagination?.current_page ?? 1
);
const computedPageSize = computed(() => props.pagination?.page_size ?? 10);

const deleteItem = (id) => {
  emit("delete-item", id);
};

const onPageChanged = (page) => {
  emit("page-changed", page);
};
</script>
