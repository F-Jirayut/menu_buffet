<template>
    <Layout>
      <div class="container-fluid">
        <div class="row mb-4">
          <div class="col-12">
            <h1 class="text-center">{{ isEditMode ? 'Edit Menu Category' : 'Create Menu Category' }}</h1>
          </div>
        </div>
        <div class="card shadow p-4">
          <div v-if="menuCategoriesStore.error" class="alert alert-danger mt-3">
            {{ menuCategoriesStore.error }}
          </div>
          <form @submit.prevent="submitForm">
            <div class="row">
              <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
                <label for="menuCategoryName" class="form-label">Name <span class="text-danger">*</span></label>
                <input
                  v-model="name"
                  type="text"
                  id="menuCategoryName"
                  class="form-control"
                  placeholder="Enter menu category name"
                  required
                  autocomplete="off"
                />
              </div>
              <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
                <label for="menuCategorySortOrder" class="form-label">Sort Order</label>
                <input
                  v-model="sort_order"
                  type="number"
                  id="menuCategorySortOrder"
                  class="form-control"
                  placeholder="Enter menu category sort order"
                  autocomplete="off"
                />
              </div>
              <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
                <label for="menuCategoryName" class="form-label">Description</label>
                <textarea
                  v-model="description"
                  id="menuCategoryDescription"
                  class="form-control"
                  placeholder="Enter menu category description"
                  autocomplete="off"
                ></textarea>
              </div>
            </div>
  
            <div class="text-end">
              <button type="submit" class="btn btn-success" :disabled="menuCategoriesStore.loading">
                <span v-if="menuCategoriesStore.loading">Saving...</span>
                <span v-else>Save</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import Layout from '@/components/admin/Layout.vue'
  import { useMenuCategoriestore } from '@/stores/menuCategoryStore'
  import { useRouter, useRoute } from 'vue-router'
  import { showSuccess, showError, showLoading, closeSwal } from '@/utils/swal'
  import { useAuthStore } from '@/stores/authStore'
  
  const auth = useAuthStore()
  const menuCategoriesStore = useMenuCategoriestore()
  const router = useRouter()
  const route = useRoute()
  
  const id = route.params.id
  const isEditMode = computed(() => !!id)
  
  const name = ref('')
  const description = ref('')
  const sort_order = ref()
  
  onMounted(async() => {
    if (isEditMode.value) {
      let menu_category = menuCategoriesStore.menuCategories.find(r => r.id == id)
  
      if (!menu_category) {
        menu_category = await menuCategoriesStore.fetchDataById(id)
      }
  
      if (menu_category) {
        name.value = menu_category.name
        description.value = menu_category.description
        sort_order.value = menu_category.sort_order
      } else {
        showError('Error', 'Menu category not found')
        router.push('/admin/foods/categories')
      }
    }
  })
  
  const submitForm = async () => {
    const payload = {
      name: name.value,
      description: description.value,
      sort_order: sort_order.value,
    }
  
    showLoading()
    if (isEditMode.value) {
      await menuCategoriesStore.editData(id, payload)
    } else {
      await menuCategoriesStore.createData(payload)
    }
    if (!menuCategoriesStore.error) {
      await auth.fetchProfile()
      closeSwal()
      showSuccess(`Menu category ${isEditMode.value ? 'updated' : 'created'} successfully`)
      router.push('/admin/foods/categories')
    } else {
      closeSwal()
      showError('Error', menuCategoriesStore.error)
      return
    }
  }
  
  </script>
  