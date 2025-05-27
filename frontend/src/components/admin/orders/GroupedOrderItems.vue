<template>
  <div
    v-for="(group, groupIndex) in groupOrderItems"
    :key="groupIndex"
    class="mb-4 border rounded p-3 mt-4"
  >
    <div class="mb-2">
      <strong>รอบเวลา:</strong> {{ group.created_at }}
    </div>
    <div class="mb-2" v-if="group.order_id">
      <strong>รหัสออเดอร์:</strong> {{ group.order_id }},
      <strong>โต๊ะ:</strong> {{ group.table_name }} (ID: {{ group.table_id }})
    </div>

    <div class="mb-2 d-flex align-items-center gap-2">
      <label class="mb-0 fw-bold">เปลี่ยนสถานะทั้งหมดในรอบนี้:</label>
      <select
        class="form-select form-select-sm w-auto"
        @change="$emit('group-status-change', group, $event.target.value)"
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

    <div class="table-responsive">
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>เมนู</th>
            <th>จำนวน</th>
            <th>ราคา</th>
            <th>สถานะ</th>
            <th>หมายเหตุ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in group.order_items" :key="item.id">
            <td>{{ item.id }}</td>
            <td>
              <a
                :href="`/admin/foods/menus/edit/${item.menu_id}`"
                class="text-decoration-none text-primary"
                target="_blank"
                rel="noopener"
              >
                {{ item.menu_name }}
              </a>
            </td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.price }}</td>
            <td>
              <select
                v-model="item.status"
                class="form-select form-select-sm"
                @change="$emit('item-status-change', item)"
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
</template>

<script setup>
defineProps({
  groupOrderItems: {
    type: Array,
    required: true,
  },
  orderItemStatusOptions: {
    type: Array,
    required: true,
  },
});

defineEmits(["group-status-change", "item-status-change"]);
</script>
