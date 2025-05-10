<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">
            {{ isEditMode ? "ดู / แก้ไขเมนู" : "เพิ่มเมนู" }}
          </h1>
        </div>
      </div>
      <Breadcrumbs />
      <div class="card shadow p-4" v-if="isOnMounted">
        <div v-if="menuStore.error" class="alert alert-danger mt-3">
          {{ menuStore.error }}
        </div>
        <form @submit.prevent="submitForm" enctype="multipart/form-data">
          <div class="row">
            <!-- Name -->
            <div class="mb-3 col-xl-6">
              <label for="menuName" class="form-label"
                >Name <span class="text-danger">*</span></label
              >
              <input
                v-model="name"
                type="text"
                id="menuName"
                class="form-control"
                required
              />
            </div>

            <!-- Sort Order -->
            <div class="mb-3 col-xl-6">
              <label for="menuSortOrder" class="form-label">Sort Order</label>
              <input
                v-model="sort_order"
                type="number"
                id="menuSortOrder"
                class="form-control"
              />
            </div>

            <!-- Description -->
            <div class="mb-3 col-xl-6">
              <label for="menuDescription" class="form-label"
                >Description</label
              >
              <textarea
                v-model="description"
                id="menuDescription"
                class="form-control"
              ></textarea>
            </div>

            <!-- Category -->
            <div class="mb-3 col-xl-6">
              <label for="categorySelect" class="form-label"
                >Category <span class="text-danger">*</span></label
              >
              <select
                v-model="category_id"
                id="categorySelect"
                class="form-select"
                required
              >
                <option disabled value="">-- Select category --</option>
                <option
                  v-for="cat in CategorySelectOption"
                  :key="cat.id"
                  :value="cat.id"
                >
                  {{ cat.name }}
                </option>
              </select>
            </div>

            <!-- Image -->
            <div class="mb-3 col-xl-6">
              <label class="form-label">Image</label>
              <input
                type="file"
                class="form-control"
                accept="image/*"
                @change="onFileChange"
              />
            </div>

            <!-- Image Preview -->
            <div class="mb-3 col-xl-6" v-if="imagePreview">
              <label class="form-label">Image Preview</label><br />
              <a :href="imagePreview" target="_blank">
                <img
                  :src="imagePreview"
                  class="img-thumbnail"
                  style="max-height: 200px"
                />
              </a>
            </div>
          </div>

          <div>
            <FormActionButtons
              :isEditMode="isEditMode"
              :loading="menuStore.loading"
              :id="id"
              :deleteItem="deleteMenu"
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
import { useMenuStore } from "@/stores/menuStore";
import { useRouter, useRoute } from "vue-router";
import { showSuccess, showError, showLoading, closeSwal, showConfirm, showSuccessOk } from "@/utils/swal";
import { useAuthStore } from "@/stores/authStore";
import { getOptions } from "@/services/optionService";
import LoadingOverlay from "@/components/LoadingOverlay.vue";
import Breadcrumbs from "@/components/Breadcrumbs.vue";
import FormActionButtons from "@/components/FormActionButtons.vue";
const auth = useAuthStore();
const menuStore = useMenuStore();
const router = useRouter();
const route = useRoute();

const id = route.params.id;
const isEditMode = computed(() => !!id);
const isOnMounted = ref(false);

const name = ref("");
const description = ref("");
const sort_order = ref();
const category_id = ref("");
const CategorySelectOption = ref([]);

const imageFile = ref(null);
const imagePreview = ref("");

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    imagePreview.value = URL.createObjectURL(file);
  }
};

onMounted(async () => {
  if (isEditMode.value) {
    let menu = menuStore.items.find((r) => r.id == id);
    if (!menu) menu = await menuStore.fetchDataById(id);

    if (menu) {
      name.value = menu.name;
      description.value = menu.description;
      sort_order.value = menu.sort_order;
      category_id.value = menu.category_id;
      imagePreview.value = menu.image_url || "";
    } else {
      showError("Error", "Menu not found");
      router.push("/admin/foods/");
    }
  }

  const response = await getOptions({ type: "categories" });
  const { data } = response.data;
  CategorySelectOption.value = data;
  isOnMounted.value = true;
});

const submitForm = async () => {
  const formData = new FormData();
  formData.append("name", name.value);
  if (
    description.value !== null &&
    description.value !== undefined &&
    description.value !== ""
  ) {
    formData.append("description", description.value || null);
  }
  if (
    sort_order.value !== null &&
    sort_order.value !== undefined &&
    sort_order.value !== ""
  ) {
    formData.append("sort_order", sort_order.value);
  }
  formData.append("category_id", category_id.value);
  if (imageFile.value) {
    formData.append("image", imageFile.value);
  }

  showLoading();
  if (isEditMode.value) {
    await menuStore.editData(id, formData);
  } else {
    await menuStore.createData(formData);
  }

  if (!menuStore.error) {
    await auth.fetchProfile();
    closeSwal();
    showSuccess(
      `Menu ${isEditMode.value ? "updated" : "created"} successfully`
    );
    router.push("/admin/foods/menus");
  } else {
    closeSwal();
    showError("Error", menuStore.error);
  }
};

const deleteMenu = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await menuStore.deleteData(id);
    if (menuStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", menuStore.error);
      return;
    }
    closeSwal();
    router.push('/admin/foods/menus')
    showSuccessOk("ลบข้อมูลสำเร็จ");
  }
};

</script>
