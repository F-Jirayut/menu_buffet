<!-- Layout.vue -->
<template>
    <Navbar />
    <div class="container-fluid">
      <div class="row flex-nowrap">
        <MainContent><slot /></MainContent>
      </div>
    </div>
  </template>
  
  <script setup>
import MainContent from './MainContent.vue';
import Navbar from './Navbar.vue';


  </script>
  