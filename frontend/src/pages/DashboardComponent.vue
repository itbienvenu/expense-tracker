<template>
  <div class="dashboard-container">
    <nav class="navbar navbar-expand-lg" :class="isLightTheme ? 'navbar-light bg-light' : 'navbar-dark bg-dark'">
      <div class="container-fluid">
        <a class="navbar-brand d-flex align-items-center" href="#">
          <img src="../assets/logo.png" width="30" height="30">
          <span class="ms-2 fw-bold" :class="isLightTheme ? 'text-dark' : 'text-light'">Expense Tracker</span>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a 
                class="nav-link" 
                :class="{ 'active': activeComponent === 'Transactions', 'text-light': !isLightTheme, 'text-dark': isLightTheme }"
                @click.prevent="setActiveComponent('Transactions')"
                href="#"
              >
                Transactions
              </a>
            </li>
            <li class="nav-item">
              <a 
                class="nav-link" 
                :class="{ 'active': activeComponent === 'Categories', 'text-light': !isLightTheme, 'text-dark': isLightTheme }"
                @click.prevent="setActiveComponent('Categories')"
                href="#"
              >
                Categories
              </a>
            </li>
          </ul>
          <div class="d-flex align-items-center">
            <button @click="toggleTheme" class="btn btn-sm" :class="isLightTheme ? 'btn-outline-dark' : 'btn-outline-secondary'">
              <i v-if="isLightTheme" class="bi bi-moon"></i>
              <i v-else class="bi bi-sun"></i>
            </button>
            <button @click="logout" class="btn btn-outline-warning ms-2">Logout</button>
          </div>
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
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Transactions from './TransactionsView.vue';
import Categories from './CategoriesView.vue';

const router = useRouter();
const activeComponent = ref('Transactions');
const isLightTheme = ref(false);

const setActiveComponent = (componentName) => {
  activeComponent.value = componentName;
};

const toggleTheme = () => {
  isLightTheme.value = !isLightTheme.value;
  document.body.classList.toggle('light-theme', isLightTheme.value);
  localStorage.setItem('theme', isLightTheme.value ? 'light' : 'dark');
};

const logout = () => {
  localStorage.removeItem('accessToken');
  router.push('/auth');
};

onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'light') {
    isLightTheme.value = true;
    document.body.classList.add('light-theme');
  }
});
</script>

<style scoped>
/*
global styles for dark and day theme toogle
 */
.dashboard-container {
  min-height: 100vh;
}
.navbar-brand svg {
  fill: #E7A428;
}
.nav-link.active {
  border-bottom: 2px solid #E7A428;
}

/* Ensure the parent container takes full height if this is part of a full-screen layout */
.split-screen-container {
  display: flex; /* Assuming a flex or grid layout for the split screen */
  min-height: 100vh; /* Make sure it takes full viewport height */
  width: 100vw; /* Make sure it takes full viewport width */
}

.marketing-panel {
  flex: 1; 
  background-image: url('../assets/hero.webp'); 
  background-size: cover; 
  background-position: center; /* Centers the image */
  background-repeat: no-repeat; 
  display: flex; 
  align-items: center; 
  justify-content: center;
  position: relative; 
}


.marketing-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4); /* Dark semi-transparent overlay */
  z-index: 1; /* Place above the background image */
}

.overlay-content {
  position: relative; /* Place above the overlay (z-index: 2) */
  z-index: 2;
  text-align: center;
  color: white; /* Ensure text is visible over the background */
  padding: 20px;
}

.sinc-logo {
  font-size: 4em; /* Adjust as needed */
  margin-bottom: 10px;
  color: #E7A428; /* Example accent color for logo */
}

.tagline {
  font-size: 1.5em; /* Adjust as needed */
  max-width: 400px;
  margin: 0 auto;
}

</style>