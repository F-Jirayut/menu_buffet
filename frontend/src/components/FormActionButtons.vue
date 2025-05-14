<template>
  <div :class="isEditMode ? 'd-flex justify-content-between' : 'text-end'">
    <button
      type="button"
      class="btn btn-danger px-4 py-2"
      :disabled="loading"
      v-if="isEditMode"
      @click="handleDelete"
    >
      <span>ลบ</span>
    </button>

    <button type="submit" class="btn btn-success px-4 py-2" :disabled="loading">
      <span>บันทึก</span>
    </button>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  isEditMode: Boolean,
  loading: Boolean,
  id: String,
  deleteItem: Function,
});

const handleDelete = async () => {
  if (props.deleteItem) {
    await props.deleteItem(props.id);
  }
};
</script>
