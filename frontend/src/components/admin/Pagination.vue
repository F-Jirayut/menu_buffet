<template>
  <nav v-if="pagination" class="mt-3">
    <ul class="pagination justify-content-end">
      <li class="page-item" :class="{ disabled: currentPage === 1 }">
        <button class="page-link" @click="onPageChange(currentPage - 1)">
          Previous
        </button>
      </li>

      <li
        v-for="page in pageNumbers"
        :key="page"
        class="page-item"
        :class="{ active: page === currentPage }"
      >
        <button class="page-link" @click="onPageChange(page)">
          {{ page }}
        </button>
      </li>

      <li class="page-item" :class="{ disabled: currentPage === totalPages }">
        <button class="page-link" @click="onPageChange(currentPage + 1)">
          Next
        </button>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  pagination: Object,
  currentPage: Number,
  pageSize: Number,
});

const emit = defineEmits(["page-changed"]);

const totalPages = computed(() => {
  const total = props.pagination?.total ?? 0;
  const perPage = props.pageSize ?? 10;
  return Math.ceil(total / perPage);
});

const pageNumbers = computed(() => {
  const pages = [];

  const total = totalPages.value;
  const current = props.currentPage ?? 1;
  const maxButtons = 5;
  let startPage = Math.max(1, current - Math.floor(maxButtons / 2));
  let endPage = startPage + maxButtons - 1;

  if (endPage > total) {
    endPage = total;
    startPage = Math.max(1, endPage - maxButtons + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return pages;
});

const onPageChange = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    emit("page-changed", page);
  }
};
</script>
