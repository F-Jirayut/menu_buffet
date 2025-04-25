<template>
    <Layout>
      <div class="container-fluid">
        <div class="row mb-4">
          <div class="col-12">
            <h1 class="text-left">Categories Management</h1>
          </div>
        </div>
  
        <!-- Search & Add Button -->
        <div class="row align-items-center mb-4">
          <div class="col-md-8">
            <div class="input-group shadow-sm">
              <span class="input-group-text bg-white">
                <i class="bi bi-search"></i>
              </span>
              <input
                v-model="search"
                type="text"
                class="form-control"
                placeholder="Search categoriess by name..."
              />
            </div>
          </div>
          <div class="col-md-4 text-md-end text-start mt-2 mt-md-0" v-if="permissionSet.has('Category.Create')">
            <router-link to="/admin/foods/categories/edit" class="btn btn-primary shadow-sm">
              <i class="bi bi-plus-lg me-1"></i> Add Categories
            </router-link>
          </div>
        </div>
  
        <!-- Section: Table -->
        <div class="row">
          <div class="col-12">
            <div class="card shadow p-4">
              <!-- <h2 class="text-center mb-4">Users</h2> -->
              <table class="table table-bordered">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="menucategory in filteredMenuCategories" :key="menucategory.id">
                    <td>{{ menucategory.id }}</td>
                    <td>{{ menucategory.name }}</td>
                    <td>
                      <div v-if="menucategory.name !== 'root' && menucategory.name !== 'admin'">
                        <router-link v-if="permissionSet.has('Category.Update')" :to="`/admin/foods/categories/edit/${menucategory.id}`" class="btn btn-warning btn-sm me-2">Edit</router-link>
                        <button v-if="permissionSet.has('Category.Delete')" class="btn btn-danger btn-sm" @click="deleteMenuCategory(menucategory.id)">Delete</button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="filteredMenuCategories.length === 0">
                    <td colspan="5" class="text-center">Data not found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  </template>
  

<script setup>
  import Layout from '@/components/admin/Layout.vue';
  import { ref, computed, onMounted } from 'vue'
  import { useMenuCategoriestore } from '@/stores/menuCategoryStore'
  import { showSuccessOk, showError, showLoading, closeSwal, showConfirm } from '@/utils/swal'
  import { useAuthStore } from '@/stores/authStore'

  const auth = useAuthStore()

  const menuCategoriesStore = useMenuCategoriestore()
  const search = ref('')
  const permissionSet = computed(() => {
    return new Set(auth.user?.permissions)
  })
  
  onMounted(async () => {
    await menuCategoriesStore.fetchData()
  })
  
  const filteredMenuCategories = computed(() => {
    return menuCategoriesStore.menuCategories.filter((menucategory) =>
        menucategory.name.toLowerCase().includes(search.value.toLowerCase())
    )
  })
  
  const deleteMenuCategory = async (id) => {
    const confirmed = await showConfirm('คุณต้องการลบข้อมูลนี้หรือไม่?')

    if (confirmed.isConfirmed) {
        showLoading()
        await menuCategoriesStore.deleteData(id)
        if (menuCategoriesStore.error) {
            closeSwal()
            showError('ลบข้อมูลไม่สำเร็จ', menuCategoriesStore.error)
            return
        }
        closeSwal()
        showSuccessOk('ลบข้อมูลสำเร็จ')
    }
  }
</script>