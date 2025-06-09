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

        <div class="mb-3 d-flex gap-2">
          <button type="button" class="btn" :class="visibleSection === 'all' ? 'btn-primary' : 'btn-outline-primary'
            " @click="visibleSection = 'all'">
            แสดงทั้งหมด
          </button>

          <button type="button" class="btn" :class="visibleSection === 'form' ? 'btn-primary' : 'btn-outline-primary'
            " @click="visibleSection = 'form'">
            คำสั่งซื้อ
          </button>

          <button type="button" class="btn" :class="visibleSection === 'group' ? 'btn-primary' : 'btn-outline-primary'
            " @click="visibleSection = 'group'">
            รายการอาหาร
          </button>

          <button type="button" class="btn btn-primary ms-auto" v-if="visibleSection === 'form' || visibleSection === 'all'" @click="addMenuItem">
            เพิ่มเมนู
          </button>

        </div>

        <form v-if="visibleSection === 'all' || visibleSection === 'form'" @submit.prevent="submitForm">
          <div class="row mb-4">
            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="table" class="form-label">โต๊ะ <span class="text-danger">*</span></label>
              <select v-model="form.table_id" id="table" class="form-select" required>
                <option disabled value="">-- เลือกโต๊ะ --</option>
                <option v-for="table in tableSelectOption" :key="table.id" :value="table.id">
                  {{ table.name }}
                </option>
              </select>
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="customer" class="form-label">ลูกค้า</label>
              <select v-model="form.customer_id" id="customer" class="form-select">
                <option></option>
                <option v-for="customer in customerSelectOption" :key="customer.id" :value="customer.id">
                  {{ customer.id }} : {{ customer.name }}
                </option>
              </select>
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderReservedAt" class="form-label">เวลาจอง</label>
              <input v-model="form.reserved_at" type="datetime-local" id="orderReservedAt" class="form-control" />
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderStartedAt" class="form-label">เวลาเริ่ม <span class="text-danger">*</span></label>
              <input v-model="form.started_at" type="datetime-local" id="orderStartedAt" class="form-control"
                required />
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderEndedAt" class="form-label">เวลาสิ้นสุด <span class="text-danger">*</span></label>
              <input v-model="form.ended_at" type="datetime-local" id="orderEndedAt" class="form-control" required />
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderStatus" class="form-label">สถานะ <span class="text-danger">*</span></label>
              <select v-model="form.status" id="orderStatus" class="form-select" required>
                <option disabled value="">-- เลือกสถานะ --</option>
                <option v-for="status in ordersStore.listStatus" :key="status" :value="status">
                  {{ status }}
                </option>
              </select>
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderTotalPrice" class="form-label">ราคารวม <span class="text-danger">*</span></label>
              <input v-model="form.total_price" type="text" id="orderTotalPrice" class="form-control" required />
            </div>

            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-6 col-xxl-6">
              <label for="orderNote" class="form-label">โน๊ต</label>
              <textarea v-model="form.note" type="text" id="orderNote" class="form-control"></textarea>
            </div>
          </div>

          <div class="row mb-4" v-for="(item, index) in menuItems" :key="index">
            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-2 col-xxl-2">
              <select v-model="item.menu" class="form-select" required @change="onMenuChange(item)">
                <option disabled value="">-- เลือกเมนู</option>
                <option v-for="menu in menuOptions" :key="menu.id" :value="menu.id">
                  {{ menu.name }}
                </option>
              </select>
            </div>
            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-2 col-xxl-2">
              <input v-model.number="item.quantity" type="number" min="1" class="form-control" placeholder="จำนวน"
                required />
            </div>
            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-2 col-xxl-2">
              <input v-model="item.price" type="number" class="form-control" placeholder="ราคา" />
            </div>
            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-2 col-xxl-2">
              <select v-model="item.status" class="form-select" required>
                <option disabled value="">สถานะ</option>
                <option v-for="status in orderItemStore.listStatus" :key="status" :value="status">
                  {{ status }}
                </option>
              </select>
            </div>
            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-2 col-xxl-2">
              <input v-model="item.note" type="text" class="form-control" placeholder="หมายเหตุ" />
            </div>
            <div class="mb-3 col-12 col-sm-12 col-md-12 col-lg-12 col-xl-2 col-xxl-2">
              <button class="btn btn-danger" type="button" @click="removeMenuItem(index)" v-if="menuItems.length > 0">
                ลบ
              </button>
            </div>
            <div class="mb-3 col-12 col-xl-6" v-if="item.image_url">
              <a :href="item.image_url" target="_blank">
                <img :src="item.image_url" class="img-thumbnail" style="max-height: 200px" />
              </a>
            </div>
          </div>

          <div>
            <FormActionButtons :isEditMode="false" :loading="ordersStore.loading" :id="id" :deleteItem="deleteOrder" />
          </div>
        </form>

        <GroupedOrderItems v-if="visibleSection === 'all' || visibleSection === 'group'"
          :groupOrderItems="groupOrderItems" :orderItemStatusOptions="orderItemStatusOptions"
          @group-status-change="updateGroupStatus" @item-status-change="updateItemStatus" />
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
import { getMenuOptions } from "@/services/menuService";
import { updateOrderItems } from "@/services/orderItemService";
import { useOrderItemStore } from "@/stores/orderItemStore";
import GroupedOrderItems from "@/components/admin/orders/GroupedOrderItems.vue";

const ordersStore = useOrderStore();
const orderItemStore = useOrderItemStore();
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
  order_items: [],
});
const groupOrderItems = ref([]);
const isOnMounted = ref(false);
const visibleSection = ref("all");

const MAX_ITEMS = 10
const menuItems = ref([])
const menuOptions = ref([]);

function addMenuItem() {
  if (menuItems.value.length < MAX_ITEMS) {
    menuItems.value.push({ menu: "", quantity: 1, price: "", status: "", note: "" })
  }
}

function removeMenuItem(index) {
  menuItems.value.splice(index, 1)
}

function onMenuChange(item) {
  const selected = menuOptions.value.find(m => m.id === item.menu)
  item.image_url = selected ? selected.image_url : ''
}


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

  const menuOptionsResponse = await getMenuOptions();
  var { data } = menuOptionsResponse.data;
  menuOptions.value = data;

  isOnMounted.value = true;
});

const updateItemStatus = async (item) => {
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
  payload.order_items = menuItems.value.map(item => ({
    menu_id: item.menu,
    quantity: item.quantity,
    price: item.price,
    status: item.status,
    note: item.note,
  }));
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
</script>
