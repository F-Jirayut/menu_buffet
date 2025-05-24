<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">
            {{ isEditMode ? "รายละเอียดคำสั่งซื้อ" : "เพิ่มคำสั่งซื้อ" }}
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
            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="table" class="form-label"
                >โต๊ะ <span class="text-danger">*</span></label
              >
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

            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
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

            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="orderReservedAt" class="form-label">เวลาจอง</label>
              <input
                v-model="form.reserved_at"
                type="datetime-local"
                id="orderReservedAt"
                class="form-control"
              />
            </div>

            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="orderStartedAt" class="form-label"
                >เวลาเริ่ม <span class="text-danger">*</span></label
              >
              <input
                v-model="form.started_at"
                type="datetime-local"
                id="orderStartedAt"
                class="form-control"
                required
              />
            </div>

            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="orderEndedAt" class="form-label"
                >เวลาสิ้นสุด <span class="text-danger">*</span></label
              >
              <input
                v-model="form.ended_at"
                type="datetime-local"
                id="orderEndedAt"
                class="form-control"
                required
              />
            </div>

            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="orderStatus" class="form-label"
                >สถานะ <span class="text-danger">*</span></label
              >
              <select
                v-model="form.status"
                id="orderStatus"
                class="form-select"
                required
              >
                <option disabled value="">-- เลือกสถานะ --</option>
                <option
                  v-for="status in ordersStore.listStatus"
                  :key="status"
                  :value="status"
                >
                  {{ status }}
                </option>
              </select>
            </div>

            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
              <label for="orderTotalPrice" class="form-label"
                >ราคารวม <span class="text-danger">*</span></label
              >
              <input
                v-model="form.total_price"
                type="text"
                id="orderTotalPrice"
                class="form-control"
                required
              />
            </div>

            <div
              class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6"
            >
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
              :isEditMode="false"
              :loading="ordersStore.loading"
              :id="id"
              :deleteItem="deleteOrder"
            />
          </div>
        </form>

        <!-- เพิ่มหลัง form หรือตรงไหนก็ได้ที่คุณต้องการแสดงรายการ -->
        <div
          v-for="(group, groupIndex) in groupOrderItems"
          :key="groupIndex"
          class="mb-4 border rounded p-3 mt-4"
        >
          <div class="mb-2">
            <strong>รอบเวลา:</strong> {{ group.created_at }}
          </div>

          <!-- Select สำหรับเปลี่ยนสถานะทั้งกลุ่ม -->
          <div class="mb-2 d-flex align-items-center gap-2">
            <label class="mb-0 fw-bold">เปลี่ยนสถานะทั้งหมดในรอบนี้:</label>
            <select
              class="form-select form-select-sm w-auto"
              @change="updateGroupStatus(group, $event.target.value)"
            >
              <option disabled selected value="">-- เลือกสถานะ --</option>
              <option
                v-for="statusOption in orderItemStatusOptions"
                :key="statusOption"
                :value="statusOption"
              >
                {{ statusOption }}
              </option>
            </select>
          </div>

          <!-- ตาราง -->
          <div class="table-responsive">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>ชื่อเมนู</th>
                  <th>จำนวน</th>
                  <th>ราคา</th>
                  <th>สถานะ</th>
                  <th>หมายเหตุ</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in group.order_items" :key="item.id">
                  <td>
                    <router-link
                      :to="`/admin/foods/menus/edit/${item.menu_id}`"
                      class="text-decoration-none text-primary"
                    >
                      {{ item.menu_name }}
                    </router-link>
                  </td>
                  <td>{{ item.quantity }}</td>
                  <td>{{ item.price }}</td>
                  <td>
                    <select
                      v-model="item.status"
                      class="form-select form-select-sm"
                      @change="updateItemStatus(item)"
                    >
                      <option
                        v-for="statusOption in orderItemStatusOptions"
                        :key="statusOption"
                        :value="statusOption"
                      >
                        {{ statusOption }}
                      </option>
                    </select>
                  </td>
                  <td>{{ item.note || "-" }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
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
import { getOptions } from "@/services/optionService";
import { updateOrderItems } from "@/services/orderItemService";

const ordersStore = useOrderStore();
const router = useRouter();
const route = useRoute();

const id = route.params.id;
const isEditMode = computed(() => !!id);
const tableSelectOption = ref([]);
const customerSelectOption = ref([]);
const orderItemStatusOptions = ref([
  "pending",
  "preparing",
  "served",
  "cancelled",
]);

const form = ref({
  table_id: null,
  customer_id: null,
  reserved_at: null,
  started_at: null,
  ended_at: null,
  status: null,
  total_price: null,
  note: null,
  email_sent: null,
});
const groupOrderItems = ref([]);
const isOnMounted = ref(false);

// const getStatusStyle = (status) => {
//   switch ((status || '').toLowerCase()) {
//     case 'pending':
//       return `color: #ffc107; font-weight: bold;`;
//     case 'reserved':
//       return `color: #17a2b8; font-weight: bold;`;
//     case 'active':
//       return `color: #28a745; font-weight: bold;`;
//     case 'completed':
//       return `color: #007bff; font-weight: bold;`;
//     case 'cancelled':
//       return `color: #dc3545; font-weight: bold;`;
//     default:
//       return `color: #6c757d; font-weight: bold;`;
//   }
// };

onMounted(async () => {
  if (isEditMode.value) {
    const order = await ordersStore.fetchDataById(id);
    if (order) {
      const customer = order.customer;
      groupOrderItems.value = order.group_order_items || [];
      form.value = {
        table_id: order.table_id,
        customer_id: customer ? customer.id : null,
        reserved_at: order.reserved_at,
        started_at: order.started_at,
        ended_at: order.ended_at,
        status: order.status,
        total_price: order.total_price,
        note: order.note,
        email_sent: order.email_sent,
      };
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

const updateItemStatus = async (item) => {
  console.log("Updating item status:", item);
  showLoading();
  if (!item || !item.id) {
    closeSwal();
    showError("Error", "Invalid item data");
    return;
  }
  try {
    const response = await updateOrderItems([
      { id: item.id, status: item.status },
    ]);
    console.log("Update response:", response);
    closeSwal();
    showSuccess("Item status updated successfully");
  } catch (error) {
    closeSwal();
    const errorMessage =
      error.response?.data?.detail ||
      error.message ||
      "Failed to update item status";
    console.error("Error updating item status:", errorMessage);
    showError("Error", errorMessage);
  }
};

const updateGroupStatus = async (group, newStatus) => {
  console.log("Updating group status:", group, "to", newStatus);
  showLoading();
  if (!group || !group.order_items || group.order_items.length === 0) {
    closeSwal();
    showError("Error", "Invalid group data");
    return;
  }
  try {
    const itemsToUpdate = group.order_items.map((item) => ({
      id: item.id,
      status: newStatus,
    }));
    const response = await updateOrderItems(itemsToUpdate);
    console.log("Update response:", response);
    group.order_items.forEach((item) => {
      item.status = newStatus; // Update local status
    });
    closeSwal();
    showSuccess("Group status updated successfully");
  } catch (error) {
    closeSwal();
    const errorMessage =
      error.response?.data?.detail ||
      error.message ||
      "Failed to update group status";
    console.error("Error updating group status:", errorMessage);
    showError("Error", errorMessage);
  }
};

const submitForm = async () => {
  const payload = { ...form.value };
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

// const deleteOrder = async (id) => {
//   const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
//   if (confirmed.isConfirmed) {
//     showLoading();
//     await ordersStore.deleteData(id);
//     if (ordersStore.error) {
//       closeSwal();
//       showError("ลบข้อมูลไม่สำเร็จ", ordersStore.error);
//       return;
//     }
//     closeSwal();
//     showSuccessOk("ลบข้อมูลสำเร็จ");
//     router.push("/admin/orders");
//   }
// };
</script>
