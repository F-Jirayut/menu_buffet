<template>
    <Layout>
      <div class="container-fluid">
        <div class="row mb-4">
          <div class="col-12">
            <h1 class="text-left">Menus Management</h1>
          </div>
        </div>
  
        <!-- Search & Add Button -->
        <div class="row align-items-center mb-4">
          <div class="col-md-8">
            <div class="input-group shadow-sm">
              <span class="input-group-text bg-white">
                <i class="bi bi-search"></i>
              </span>
              <input
                v-model="search"
                type="text"
                class="form-control"
                placeholder="Search menus by name..."
              />
            </div>
          </div>
          <div class="col-md-4 text-md-end text-start mt-2 mt-md-0">
            <router-link to="/admin/users/edit" class="btn btn-primary shadow-sm">
              <i class="bi bi-plus-lg me-1"></i> Add Menu
            </router-link>
          </div>
        </div>
  
        <!-- Section: Table -->
        <div class="row">
          <div class="col-12">
            <div class="card shadow p-4">
              <!-- <h2 class="text-center mb-4">Users</h2> -->
              <table class="table table-bordered">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Menu</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                  </tr>
                  <!-- <tr v-if="filteredUsers.length === 0">
                    <td colspan="5" class="text-center">Data not found.</td>
                  </tr> -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  </template>
  

<script setup>
import Layout from '@/components/admin/Layout.vue';
</script>