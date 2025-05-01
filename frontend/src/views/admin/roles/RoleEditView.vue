<template>
  <Layout>
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <h1 class="fw-bold">
            {{ isEditMode ? "ดู / แก้ไขบทบาท" : "เพิ่มบทบาท" }}
          </h1>
        </div>
      </div>
      <Breadcrumbs />
      <div class="card shadow-sm p-4" v-if="isOnMounted">
        <div v-if="rolesStore.error" class="alert alert-danger">
          {{ rolesStore.error }}
        </div>

        <form @submit.prevent="submitForm">
          <div class="row mb-4">
            <div class="col-12 col-md-6">
              <label for="roleName" class="form-label fw-semibold"
                >ชื่อ <span class="text-danger">*</span></label
              >
              <input
                v-model="name"
                type="text"
                id="roleName"
                class="form-control"
                required
              />
            </div>
          </div>

          <div class="mb-4">
            <h5 class="fw-semibold">สิทธิ์การใช้งาน</h5>
            <div class="table-responsive">
              <table class="table table-bordered align-middle">
                <thead class="table-secondary text-center">
                  <tr>
                    <th>Module</th>
                    <th>
                      View <br />
                      <input
                        type="checkbox"
                        v-model="checkboxHeaders.View"
                        @change="toggleAll('View', $event.target.checked)"
                      />
                    </th>
                    <th>
                      Create <br />
                      <input
                        type="checkbox"
                        v-model="checkboxHeaders.Create"
                        @change="toggleAll('Create', $event.target.checked)"
                      />
                    </th>
                    <th>
                      Update <br />
                      <input
                        type="checkbox"
                        v-model="checkboxHeaders.Update"
                        @change="toggleAll('Update', $event.target.checked)"
                      />
                    </th>
                    <th>
                      Delete <br />
                      <input
                        type="checkbox"
                        v-model="checkboxHeaders.Delete"
                        @change="toggleAll('Delete', $event.target.checked)"
                      />
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(actions, module) in permissionGroups"
                    :key="module"
                    class="text-center"
                  >
                    <td class="fw-medium">{{ module }}</td>
                    <td>
                      <input
                        v-if="actions.includes('View')"
                        type="checkbox"
                        :value="`${module}.View`"
                        v-model="selectedPermissions"
                      />
                    </td>
                    <td>
                      <input
                        v-if="actions.includes('Create')"
                        type="checkbox"
                        :value="`${module}.Create`"
                        v-model="selectedPermissions"
                      />
                    </td>
                    <td>
                      <input
                        v-if="actions.includes('Update')"
                        type="checkbox"
                        :value="`${module}.Update`"
                        v-model="selectedPermissions"
                      />
                    </td>
                    <td>
                      <input
                        v-if="actions.includes('Delete')"
                        type="checkbox"
                        :value="`${module}.Delete`"
                        v-model="selectedPermissions"
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div>
            <FormActionButtons
              :isEditMode="isEditMode"
              :loading="rolesStore.loading"
              :id="id"
              :deleteItem="deleteRole"
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
import { useRoleStore } from "@/stores/roleStore";
import { usePermissionStore } from "@/stores/permissionStore";
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

const rolesStore = useRoleStore();
const permissionStore = usePermissionStore();
const router = useRouter();
const route = useRoute();
const checkboxHeaders = {
  View: false,
  Create: false,
  Update: false,
  Delete: false,
};

const id = route.params.id;
const isEditMode = computed(() => !!id);

const name = ref("");
const selectedPermissions = ref(new Set());
const isOnMounted = ref(false);

const permissionGroups = computed(() => {
  return permissionStore.permissionGroups || {};
});

const toggleAll = (action, isChecked) => {
  const keys = Object.keys(permissionGroups.value);

  keys.forEach((module) => {
    const permission = `${module}.${action}`;

    if (isChecked) {
      selectedPermissions.value.add(permission);
    } else {
      selectedPermissions.value.delete(permission);
    }
  });
};

onMounted(async () => {
  await permissionStore.fetchPermissionGroups();
  if (isEditMode.value) {
    const role = await rolesStore.fetchDataById(id, {
      params: { include: "permissions" },
    });
    if (role) {
      name.value = role.name;
      selectedPermissions.value = new Set(
        role.permissions?.map((p) => p.name) || []
      );
      await updateHeaderCheckboxes();
    } else {
      showError("Error", "Role not found");
      router.push("/admin/roles");
    }
  }
  isOnMounted.value = true;
});

const updateHeaderCheckboxes = async () => {
  const actions = ["View", "Create", "Update", "Delete"];
  const modules = Object.keys(permissionGroups.value);
  actions.forEach((action) => {
    const isAllChecked = modules.every((module) =>
      permissionGroups.value[module].includes(action)
        ? selectedPermissions.value.has(`${module}.${action}`)
        : true
    );
    checkboxHeaders[action] = isAllChecked;
  });
};

const submitForm = async () => {
  const payload = {
    name: name.value,
    permission_names: Array.from(selectedPermissions.value),
  };
  showLoading();
  if (isEditMode.value) {
    await rolesStore.editData(id, payload);
  } else {
    await rolesStore.createData(payload);
  }

  if (!rolesStore.error) {
    closeSwal();
    showSuccess(
      `Role ${isEditMode.value ? "updated" : "created"} successfully`
    );
    router.push("/admin/roles");
  } else {
    closeSwal();
    showError("Error", rolesStore.error);
  }
};

const deleteRole = async (id) => {
  const confirmed = await showConfirm("คุณต้องการลบข้อมูลนี้หรือไม่?");
  if (confirmed.isConfirmed) {
    showLoading();
    await rolesStore.deleteData(id);
    if (rolesStore.error) {
      closeSwal();
      showError("ลบข้อมูลไม่สำเร็จ", rolesStore.error);
      return;
    }
    closeSwal();
    showSuccessOk("ลบข้อมูลสำเร็จ");
    router.push("/admin/roles");
  }
};
</script>
