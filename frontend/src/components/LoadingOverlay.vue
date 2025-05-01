<template>
    <div class="loading-overlay">
      <div class="text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">กำลังโหลด...</span>
        </div>
        <div class="mt-2">{{ message }}</div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    message: {
      type: String,
      default: 'กำลังโหลด...',
    },
  });
  </script>
  
  <style scoped>
  .loading-overlay {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 70vh;
  }
  .spinner-border {
    width: 3rem;
    height: 3rem;
  }
  </style>
  