<template>
  <div class="dashboard-container">
    <nav class="navbar navbar-expand-lg" :class="isLightTheme ? 'navbar-light bg-light' : 'navbar-dark bg-dark'">
      <div class="container-fluid">
        <a class="navbar-brand d-flex align-items-center" href="#">
          <img src="../assets/logo.png" width="30" height="30" alt="Expense Tracker Logo">
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

            <div class="dropdown ms-3">
              <a class="d-flex align-items-center text-decoration-none dropdown-toggle" href="#" id="profileDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <div class="profile-avatar bg-warning text-dark me-2">
                  <span v-if="user">{{ user.username.charAt(0).toUpperCase() }}</span>
                  <i v-else class="bi bi-person"></i> </div>
              </a>
              <ul class="dropdown-menu dropdown-menu-end" :class="isLightTheme ? '' : 'dropdown-menu-dark'" aria-labelledby="profileDropdown">
                <li v-if="user">
                  <h6 class="dropdown-header">{{ user.username }}</h6>
                  <p class="dropdown-item-text small text-muted">{{ user.email }}</p>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li><button class="dropdown-item" @click="logout">Logout</button></li>
              </ul>
            </div>
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
import axios from 'axios';
import Transactions from './TransactionsView.vue'; // Corrected filename
import Categories from './CategoriesView.vue';     // Corrected filename

const BASE_API_URL = import.meta.env.VITE_APP_API_URL;

const router = useRouter();
const activeComponent = ref('Transactions');
const isLightTheme = ref(false);
const user = ref(null); // To store user profile data

const setActiveComponent = (componentName) => {
  activeComponent.value = componentName;
};

const toggleTheme = () => {
  isLightTheme.value = !isLightTheme.value;
  document.body.classList.toggle('light-theme', isLightTheme.value);
  localStorage.setItem('theme', isLightTheme.value ? 'light' : 'dark');
};

const getHeaders = () => {
  const token = localStorage.getItem('accessToken');
  return { Authorization: `Bearer ${token}` };
};

const fetchUserProfile = async () => {
  try {
    const response = await axios.get(`${BASE_API_URL}/auth/me`, { headers: getHeaders() });
    user.value = response.data;
  } catch (error) {
    console.error('Failed to fetch user profile:', error);
  }
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
  fetchUserProfile(); // Fetch user data when component mounts
});
</script>

<style scoped>
/*
global styles for dark and day theme toogle
*/
.dashboard-container {
  min-height: 100vh;
}
.navbar-brand img { /* Changed from svg to img for your logo */
  fill: #E7A428; /* This fill won't work on img, but keeping it for context if you switch back */
}
.nav-link.active {
  border-bottom: 2px solid #E7A428;
}

/* User Profile Avatar Styles */
.profile-avatar {
  width: 38px; /* Size of the circle */
  height: 38px;
  border-radius: 50%; /* Makes it a circle */
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1em;
  cursor: pointer;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2); /* Subtle glow */
  transition: all 0.2s ease;
}

.profile-avatar:hover {
  box-shadow: 0 0 0 3px #E7A428; /* Accent glow on hover */
}

/* Dropdown Menu styling for dark theme consistency */
.dropdown-menu-dark {
  background-color: #343a40;
  border-color: #454d55;
}
.dropdown-menu-dark .dropdown-item {
  color: #f8f9fa;
}
.dropdown-menu-dark .dropdown-item:hover {
  background-color: #495057;
  color: #fff;
}
.dropdown-menu-dark .dropdown-header {
  color: #ced4da;
}
.dropdown-menu-dark .dropdown-item-text {
  color: #adb5bd !important; /* Ensure muted text is visible */
}
.dropdown-menu-dark .dropdown-divider {
  border-top-color: #454d55;
}

/* Existing styles for banner (if still in use) */
.split-screen-container {
  display: flex;
  min-height: 100vh;
  width: 100vw;
}
.marketing-panel {
  flex: 1; 
  background-image: url('../assets/hero.webp'); 
  background-size: cover; 
  background-position: center; 
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
  background-color: rgba(0, 0, 0, 0.4); 
  z-index: 1; 
}
.overlay-content {
  position: relative; 
  z-index: 2;
  text-align: center;
  color: white; 
  padding: 20px;
}
.sinc-logo {
  font-size: 4em; 
  margin-bottom: 10px;
  color: #E7A428; 
}
.tagline {
  font-size: 1.5em; 
  max-width: 400px;
  margin: 0 auto;
}
</style>