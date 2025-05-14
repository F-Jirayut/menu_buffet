<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">
            {{ isEditMode ? "ดู / แก้ไขคำสั่งซื้อ" : "เพิ่มคำสั่งซื้อ" }}
          </h1>
        </div>
      </div>
      <Breadcrumbs />
      <div class="card shadow-sm p-4" v-if="isOnMounted">
        <div v-if="ordersStore.error" class="alert alert-danger">
          {{ ordersStore.error }}
        </div>

        <form @submit.prevent="submitForm">
          <div class="row mb-4">
            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="table" class="form-label">โต๊ะ <span class="text-danger">*</span></label>
              <select
                v-model="form.table_id"
                id="table"
                class="form-select"
                required
              >
                <option disabled value="">-- เลือกโต๊ะ --</option>
                <option
                  v-for="table in tableSelectOption"
                  :key="table.id"
                  :value="table.id"
                >
                  {{ table.name }}
                </option>
              </select>
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="customer" class="form-label">ลูกค้า</label>
              <select
                v-model="form.customer_id"
                id="customer"
                class="form-select"
              >
                <option></option>
                <option
                  v-for="customer in customerSelectOption"
                  :key="customer.id"
                  :value="customer.id"
                >
                  {{ customer.id }} : {{ customer.name }}
                </option>
              </select>
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderReservedAt" class="form-label">เวลาจอง</label>
              <input
                v-model="form.reserved_at"
                type="datetime-local"
                id="orderReservedAt"
                class="form-control"
              />
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderStartedAt" class="form-label">เวลาเริ่ม <span class="text-danger">*</span></label>
              <input
                v-model="form.started_at"
                type="datetime-local"
                id="orderStartedAt"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderEndedAt" class="form-label">เวลาสิ้นสุด <span class="text-danger">*</span></label>
              <input
                v-model="form.ended_at"
                type="datetime-local"
                id="orderEndedAt"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderStatus" class="form-label">สถานะ <span class="text-danger">*</span></label>
              <input
                v-model="form.status"
                type="text"
                id="orderStatus"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderDepositAmount" class="form-label">ค่ามัดจำ</label>
              <input
                v-model="form.deposit_amount"
                type="text"
                id="orderDepositAmount"
                class="form-control"
              />
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderTotalPrice" class="form-label">ราคารวม <span class="text-danger">*</span></label>
              <input
                v-model="form.total_price"
                type="text"
                id="orderTotalPrice"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderNote" class="form-label">โน๊ต</label>
              <textarea
                v-model="form.note"
                type="text"
                id="orderNote"
                class="form-control"
              ></textarea>
            </div>
          </div>

          <div>
            <FormActionButtons
              :isEditMode="isEditMode"
              :loading="ordersStore.loading"
              :id="id"
              :deleteItem="deleteOrder"
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
import { useOrderStore } from "@/stores/orderStore";
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
import { getOptions } from "@/services/optionService";

const ordersStore = useOrderStore();
const router = useRouter();
const route = useRoute();

const id = route.params.id;
const isEditMode = computed(() => !!id);
const tableSelectOption = ref([]);
const customerSelectOption = ref([]);

const form = ref({
  table_id: null,
  customer_id: null,
  reserved_at: null,
  started_at: null,
  ended_at: null,
  status: null,
  deposit_amount: null,
  total_price: null,
  note: null,
  email_sent: null,
});

const isOnMounted = ref(false);

onMounted(async () => {
  if (isEditMode.value) {
    const order = await ordersStore.fetchDataById(id);
    if (order) {
      name.value = order.name;
      email.value = order.email;
      phone.value = order.phone;
    } else {
      showError("Error", "Order not found");
      router.push("/admin/orders");
    }
  }
  const tablesResponse = await getOptions({ type: "tables" });
  var { data } = tablesResponse.data;
  tableSelectOption.value = data;

  const Customersresponse = await getOptions({ type: "customers" });
  var { data } = Customersresponse.data;
  customerSelectOption.value = data;
  isOnMounted.value = true;
});

const submitForm = async () => {
  const payload = { ...form.value };
  console.log(payload)
  showLoading();
  if (isEditMode.value) {
    await ordersStore.editData(id, payload);
  } else {
    await ordersStore.createData(payload);
  }

  if (!ordersStore.error) {
    closeSwal();
    showSuccess(
      `Order ${isEditMode.value ? "updated" : "created"} successfully`
    );
    router.push("/admin/orders");
  } else {
    closeSwal();
    showError("Error", ordersStore.error);
  }
};

const deleteOrder = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await ordersStore.deleteData(id);
    if (ordersStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", ordersStore.error);
      return;
    }
    closeSwal();
    showSuccessOk("ลบข้อมูลสำเร็จ");
    router.push("/admin/orders");
  }
};
</script>
