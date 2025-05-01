<template>
  <div class="col-auto col-md-3 col-xl-2 px-sm-2 px-0 bg-dark">
    <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 text-white min-vh-100">
        <!-- <a href="/" class="d-flex align-items-center pb-3 mb-md-0 me-md-auto text-white text-decoration-none">
            <span class="fs-5 d-none d-sm-inline">Menu</span>
        </a> -->
        <ul class="nav nav-pills flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start" id="menu">
            <li class="nav-item">
                <a href="#" class="nav-link align-middle px-0">
                    <i class="fs-4 bi-speedometer2"></i> <span class="ms-1 d-none d-sm-inline">Dashboard</span>
                </a>
            </li>
            <li v-if="permissionSet.has('Role.View')">
                <router-link to="/admin/roles" class="nav-link px-0 align-middle">
                    <i class="fs-4 bi bi-person-workspace"></i>
                    <span class="ms-1 d-none d-sm-inline">บทบาท</span>
                </router-link>
            </li>
            <li v-if="permissionSet.has('Permission.View')">
                <router-link to="/admin/permissions" class="nav-link px-0 align-middle">
                    <i class="fs-4 bi bi-key-fill"></i>
                    <span class="ms-1 d-none d-sm-inline">สิทธิ์การใช้งาน</span>
                </router-link>
            </li>
            <li v-if="permissionSet.has('User.View')">
                <router-link to="/admin/users" class="nav-link px-0 align-middle">
                    <i class="fs-4 bi bi-person"></i>
                    <span class="ms-1 d-none d-sm-inline">ผู้ใช้งาน</span>
                </router-link>
            </li>
            <li v-if="permissionSet.has('Table.View')">
                <router-link to="/admin/tables" class="nav-link px-0 align-middle">
                    <i class="fs-4 bi bi-table"></i>
                    <span class="ms-1 d-none d-sm-inline">โต๊ะ</span>
                </router-link>
            </li>
            <li v-if="permissionSet.has('Menu.View') || permissionSet.has('Category.View')">
                <a href="#foods" data-bs-toggle="collapse" class="nav-link px-0 align-middle d-flex justify-content-between align-items-center" aria-expanded="false">
                    <span>
                    <i class="fs-4 bi-card-list"></i>
                    <span class="ms-1 d-none d-sm-inline">อาหาร</span>
                    </span>
                    <i class="bi bi-chevron-down collapse-toggle-icon ms-2 d-none d-sm-inline"></i>
                </a>
                <ul class="collapse nav ms-2" :class="{ show: isMenuActive || isCategoryActive }" id="foods" data-bs-parent="#menu">
                    <li class="w-100" v-if="permissionSet.has('Menu.View')">
                        <router-link to="/admin/foods/menus" class="nav-link px-0"> <span class="d-none d-sm-inline">เมนู</span> </router-link>
                    </li>
                    <li class="w-100" v-if="permissionSet.has('Category.View')">
                        <router-link to="/admin/foods/categories" class="nav-link px-0"> <span class="d-none d-sm-inline">ประเภท</span> </router-link>
                    </li>
                </ul>
            </li>
        </ul>
        <hr>
        <div class="dropdown pb-4">
            <a href="#" class="d-flex align-items-center text-white text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="bi bi-person-circle fs-4 me-2"></i>
                <span class="d-none d-sm-inline mx-1">{{ auth.user?.username || 'User' }}</span>
            </a>
            <ul class="dropdown-menu dropdown-menu-dark text-small shadow">
                <!-- <li><a class="dropdown-item" href="#">New project...</a></li>
                <li><a class="dropdown-item" href="#">Settings</a></li>
                <li><a class="dropdown-item" href="#">Profile</a></li>
                <li><hr class="dropdown-divider"></li> -->
                <li><a class="dropdown-item" href="#" @click.prevent="handleLogout">ออกจากระบบ</a></li>
            </ul>
        </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import router from '@/router';
const auth = useAuthStore()
const permissionSet = computed(() => {
    return new Set(auth.user?.permissions)
})

const handleLogout = async () => {
    await auth.logout()
    router.push('/admin/login')
}

const route = useRoute()

const isMenuActive = computed(() => {
  return route.path.startsWith('/admin/foods/menus')
})

const isCategoryActive = computed(() => {
  return route.path.startsWith('/admin/foods/categories')
})

const isFoodsGroupActive = computed(() => {
  return isMenuActive.value || isCategoryActive.value
})

</script>

<style scoped>
/* หมุนลูกศร */
.collapse-toggle-icon {
  transition: transform 0.3s ease;
}

/* เมนูเปิด: ลูกศรหมุนขึ้น */
a[aria-expanded="true"] .collapse-toggle-icon {
  transform: rotate(180deg);
}

</style>
