<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">
            {{ isEditMode ? "ดู / แก้ไขลูกค้า" : "เพิ่มลูกค้า" }}
          </h1>
        </div>
      </div>
      <Breadcrumbs />
      <div class="card shadow-sm p-4" v-if="isOnMounted">
        <div v-if="customersStore.error" class="alert alert-danger">
          {{ customersStore.error }}
        </div>

        <form @submit.prevent="submitForm">
          <div class="row mb-4">
            <div class="mb-3 col-12 col-md-6">
              <label for="customerName" class="form-label"
                >ชื่อ <span class="text-danger">*</span></label
              >
              <input
                v-model="name"
                type="text"
                id="customerName"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3 col-12 col-md-6">
              <label for="customerEmail" class="form-label"
                >อีเมล์ <span class="text-danger">*</span></label
              >
              <input
                v-model="email"
                type="text"
                id="customerEmail"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3 col-12 col-md-6">
              <label for="customerPhone" class="form-label"
                >เบอร์โทร <span class="text-danger">*</span></label
              >
              <input
                v-model="phone"
                type="text"
                id="customerPhone"
                class="form-control"
                required
              />
            </div>
          </div>

          <div>
            <FormActionButtons
              :isEditMode="isEditMode"
              :loading="customersStore.loading"
              :id="id"
              :deleteItem="deleteCustomer"
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
import { useCustomerStore } from "@/stores/customerStore";
import { useRouter, useRoute } from "vue-router";
import {
  showSuccess,
  showError,
  showLoading,
  closeSwal,
  showSuccessOk,
  showConfirm,
} from "@/utils/swal";
import FormActionButtons from "@/components/FormActionButtons.vue";
import LoadingOverlay from "@/components/LoadingOverlay.vue";
import Breadcrumbs from "@/components/Breadcrumbs.vue";
import { validateEmail, validatePhone } from "@/utils/validators";

const customersStore = useCustomerStore();
const router = useRouter();
const route = useRoute();

const id = route.params.id;
const isEditMode = computed(() => !!id);

const name = ref("");
const email = ref("");
const phone = ref("");
const isOnMounted = ref(false);

onMounted(async () => {
  if (isEditMode.value) {
    const customer = await customersStore.fetchDataById(id);
    if (customer) {
      name.value = customer.name;
      email.value = customer.email;
      phone.value = customer.phone;
    } else {
      showError("Error", "Customer not found");
      router.push("/admin/customers");
    }
  }
  isOnMounted.value = true;
});

const submitForm = async () => {
  const payload = {
    name: name.value,
    email: email.value,
    phone: phone.value,
  };

  if (!validateEmail(payload.email)) {
    showError("รูปแบบอีเมล์ไม่ถูกต้อง");
    return;
  }

  if (!validatePhone(payload.phone)) {
    showError("หมายเลขโทรศัพท์ต้องมี 10 หลัก");
    return;
  }

  showLoading();
  if (isEditMode.value) {
    await customersStore.editData(id, payload);
  } else {
    await customersStore.createData(payload);
  }

  if (!customersStore.error) {
    closeSwal();
    showSuccess(
      `Customer ${isEditMode.value ? "updated" : "created"} successfully`
    );
    router.push("/admin/customers");
  } else {
    closeSwal();
    showError("Error", customersStore.error);
  }
};

const deleteCustomer = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await customersStore.deleteData(id);
    if (customersStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", customersStore.error);
      return;
    }
    closeSwal();
    showSuccessOk("ลบข้อมูลสำเร็จ");
    router.push("/admin/customers");
  }
};
</script>
