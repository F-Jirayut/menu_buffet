<template>
  <div class="input-group shadow-sm">
    <span class="input-group-text bg-white">
      <i class="bi bi-search"></i>
    </span>
    <input
      type="text"
      class="form-control"
      v-model="searchTerm"
      :placeholder="placeholder"
      @keydown.enter="onSearch"
    />
    <button class="btn btn-outline-primary" @click="onSearch">Search</button>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";

const props = defineProps({
  modelValue: String,
  placeholder: String,
});

const emit = defineEmits(["update:modelValue", "search"]);

const searchTerm = ref(props.modelValue);

// ตอบสนองการค้นหา
const onSearch = () => {
  emit("update:modelValue", searchTerm.value);
  emit("search");
};
</script>