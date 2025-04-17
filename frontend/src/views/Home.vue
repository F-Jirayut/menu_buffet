<script setup>
import '../style.css'
import Layout from '@/components/Layout.vue'
import { useMenuStore } from '@/stores/menuStore'
const menuStore = useMenuStore()
</script>

<template>
  <Layout>
    <div class="container my-4">
    <h1 class="mb-4">เมนูอาหาร ({{ menuStore.totalMenuItems }} รายการ)</h1>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div class="col" v-for="(item, index) in menuStore.items" :key="index">
        <div class="card h-100">
          <img :src="item.image" class="card-img-top" :alt="item.name">
          <div class="card-body">
            <h5 class="card-title">{{ item.name }}</h5>
            <p class="card-text text-muted">{{ item.description }}</p>
          </div>
          <div class="card-footer">
            <span class="text-primary fw-bold">{{ item.price }} บาท</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  </Layout>
</template>

<style scoped>
.card-img-top {
  object-fit: cover;
  height: 200px;
}
</style>
