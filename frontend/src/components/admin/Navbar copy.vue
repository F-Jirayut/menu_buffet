<template>
  <nav class="navbar navbar-dark bg-dark p-2">
      <a class="navbar-brand text-light">Navbar</a>
      <div class="dropdown">
        <button
          class="btn border-0 bg-transparent text-white"
          type="button"
          id="dropdownMenuButton"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="32"
            height="32"
            fill="currentColor"
            class="bi bi-person-circle"
            viewBox="0 0 16 16"
          >
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
            <path
              fill-rule="evenodd"
              d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 
              11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 
              5.468 2.37A7 7 0 0 0 8 1"
            />
          </svg>
        </button>

        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
          <li><a class="dropdown-item" href="#">โปรไฟล์</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item text-danger" href="#">ออกจากระบบ</a></li>
        </ul>
      </div>
  </nav>
</template>

<script setup></script>

<style scoped>
/* .sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  width: 250px;
}
.main-content {
  margin-left: 250px;
} */
</style>
