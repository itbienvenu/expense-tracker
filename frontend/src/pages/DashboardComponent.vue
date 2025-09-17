<template>
  <div class="dashboard-container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand d-flex align-items-center" href="#">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 22H22L12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="#E7A428"/>
          </svg>
          <span class="ms-2 fw-bold text-light">Expense Tracker</span>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a 
                class="nav-link" 
                :class="{ 'active': activeComponent === 'Transactions' }"
                @click.prevent="setActiveComponent('Transactions')"
                href="#"
              >
                Transactions
              </a>
            </li>
            <li class="nav-item">
              <a 
                class="nav-link" 
                :class="{ 'active': activeComponent === 'Categories' }"
                @click.prevent="setActiveComponent('Categories')"
                href="#"
              >
                Categories
              </a>
            </li>
          </ul>
          <button @click="logout" class="btn btn-outline-warning">Logout</button>
        </div>
      </div>
    </nav>

    <main class="container-fluid mt-4">
      <div v-if="activeComponent === 'Transactions'">
        <Transactions />
      </div>
      <div v-else-if="activeComponent === 'Categories'">
        <Categories />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Transactions from './TransactionsView.vue';
import Categories from './CategoriesView.vue';

const router = useRouter();
const activeComponent = ref('Transactions'); // Default view

const setActiveComponent = (componentName) => {
  activeComponent.value = componentName;
};

const logout = () => {
  localStorage.removeItem('accessToken');
  router.push('/auth');
};
</script>

<style scoped>
.dashboard-container {
  background-color: #000000;
  min-height: 100vh;
}
.navbar-brand svg {
  fill: #E7A428;
}
.nav-link.active {
  color: #E7A428 !important;
  border-bottom: 2px solid #E7A428;
}
.nav-link {
  color: #fff !important;
}
.nav-link:hover {
  color: #E7A428 !important;
}
</style>