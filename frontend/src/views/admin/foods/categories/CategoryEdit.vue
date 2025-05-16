<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">
            {{ isEditMode ? "รายละเอียดประเภท" : "เพิ่มประเภท" }}
          </h1>
        </div>
      </div>
      <Breadcrumbs />
      <div class="card shadow p-4" v-if="isOnMounted">
        <div v-if="menuCategoriesStore.error" class="alert alert-danger mt-3">
          {{ menuCategoriesStore.error }}
        </div>
        <form @submit.prevent="submitForm">
          <div class="row">
            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="menuCategoryName" class="form-label"
                >ชื่อ <span class="text-danger">*</span></label
              >
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
            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="menuCategorySortOrder" class="form-label"
                >Sort Order</label
              >
              <input
                v-model="sort_order"
                type="number"
                id="menuCategorySortOrder"
                class="form-control"
                placeholder="Enter menu category sort order"
                autocomplete="off"
              />
            </div>
            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="menuCategoryName" class="form-label"
                >รายละเอียด</label
              >
              <textarea
                v-model="description"
                id="menuCategoryDescription"
                class="form-control"
                placeholder="Enter menu category description"
                autocomplete="off"
              ></textarea>
            </div>
          </div>

          <div>
            <FormActionButtons
              :isEditMode="isEditMode"
              :loading="menuCategoriesStore.loading"
              :id="id"
              :deleteItem="deleteMenuCategory"
            />
          </div>

        </form>
      </div>
      <LoadingOverlay v-else />
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import Layout from "@/components/admin/Layout.vue";
import { useMenuCategoryStore } from "@/stores/menuCategoryStore";
import { useRouter, useRoute } from "vue-router";
import { showSuccess, showError, showLoading, closeSwal, showConfirm, showSuccessOk } from "@/utils/swal";
import { useAuthStore } from "@/stores/authStore";
import LoadingOverlay from "@/components/LoadingOverlay.vue";
import Breadcrumbs from "@/components/Breadcrumbs.vue";
import FormActionButtons from "@/components/FormActionButtons.vue";

const auth = useAuthStore();
const menuCategoriesStore = useMenuCategoryStore();
const router = useRouter();
const route = useRoute();

const id = route.params.id;
const isEditMode = computed(() => !!id);
const isOnMounted = ref(false);

const name = ref("");
const description = ref("");
const sort_order = ref();

onMounted(async () => {
  if (isEditMode.value) {
    let menu_category = menuCategoriesStore.items.find(
      (r) => r.id == id
    );

    if (!menu_category) {
      menu_category = await menuCategoriesStore.fetchDataById(id);
    }

    if (menu_category) {
      name.value = menu_category.name;
      description.value = menu_category.description;
      sort_order.value = menu_category.sort_order;
    } else {
      showError("Error", "Menu category not found");
      router.push("/admin/foods/categories");
    }
  }
  isOnMounted.value = true
});

const submitForm = async () => {
  const payload = {
    name: name.value,
    description: description.value,
    sort_order: sort_order.value,
  };

  showLoading();
  if (isEditMode.value) {
    await menuCategoriesStore.editData(id, payload);
  } else {
    await menuCategoriesStore.createData(payload);
  }
  if (!menuCategoriesStore.error) {
    await auth.fetchProfile();
    closeSwal();
    showSuccess(
      `Menu category ${isEditMode.value ? "updated" : "created"} successfully`
    );
    router.push("/admin/foods/categories");
  } else {
    closeSwal();
    showError("Error", menuCategoriesStore.error);
    return;
  }
};

const deleteMenuCategory = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await menuCategoriesStore.deleteData(id);
    if (menuCategoriesStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", menuCategoriesStore.error);
      return;
    }
    closeSwal();
    router.push('/admin/foods/categories')
    showSuccessOk("ลบข้อมูลสำเร็จ");
  }
};
</script>
