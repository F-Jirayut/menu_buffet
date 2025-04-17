<!-- Layout.vue -->
<template>
  <div class="container-fluid">
    <div class="row flex-nowrap">
      <Sidebar />
      <MainContent><slot /></MainContent>
    </div>
  </div>
</template>

<script setup>
  import MainContent from './MainContent.vue';
  import Sidebar from './Sidebar.vue'
</script>
