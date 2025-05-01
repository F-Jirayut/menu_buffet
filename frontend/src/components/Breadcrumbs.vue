<template>
  <nav style="--bs-breadcrumb-divider: '>'" aria-label="breadcrumb">
    <ol class="breadcrumb">
      <li
        v-for="(item, index) in breadcrumb"
        :key="index"
        class="breadcrumb-item"
        :class="{ active: index === breadcrumb.length - 1 }"
      >
        <RouterLink
          v-if="item.to && index !== breadcrumb.length - 1"
          :to="item.to"
        >
          {{ item.name }}
        </RouterLink>
        <span v-else>{{ item.name }}</span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { useRoute } from "vue-router";
import { computed } from "vue";

const route = useRoute();

const breadcrumb = computed(() => {
  const meta = route.meta;
  const breadcrumbMeta = meta.breadcrumb;
  if (typeof breadcrumbMeta === "function") {
    return breadcrumbMeta(route);
  }
  return breadcrumbMeta || [];
});
</script>

<style scoped>
.breadcrumb {
  background-color: transparent;
  padding: 0;
  margin-bottom: 1rem;
}
</style>
