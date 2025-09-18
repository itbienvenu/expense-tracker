<template>
  <div class="split-screen-container">
    <div class="marketing-panel">
      <div class="overlay-content">
        <!-- <h1 class="sinc-logo">Sinc</h1>
        <p class="tagline">The easiest way to manage your events.</p> -->
        </div>
    </div>

    <div class="auth-panel">
      <div class="auth-card">
        <h2 class="form-title">{{ isLogin ? 'Login' : 'Register' }}</h2>
        <p class="form-subtitle">Enter your credentials below!</p>

        <form v-if="isLogin" @submit.prevent="handleLogin" class="auth-form">
          <div class="input-group">
            <i class="icon-email"></i> <input v-model="email" placeholder="Email or username" type="text" required />
          </div>
          <div class="input-group">
            <i class="icon-password"></i> <input v-model="password" placeholder="Password" type="password" required />
            <i class="icon-eye-toggle"></i> </div>
          <a href="#" class="forgot-password">Forgot password?</a>

          <button type="submit" class="primary-button">Login</button>          
          <p class="toggle-auth">
            Don't have an account yet?
            <a href="#" @click.prevent="isLogin = false" class="signup-link">Signup</a>
          </p>
        </form>

        <form v-else @submit.prevent="handleRegister" class="auth-form">
          <div class="input-group">
            <i class="icon-user"></i> <input v-model="username" placeholder="Username" type="text" required />
          </div>
          <div class="input-group">
            <i class="icon-email"></i> <input v-model="email" placeholder="Email" type="email" required />
          </div>
          <div class="input-group">
            <i class="icon-password"></i> <input v-model="password" placeholder="Password" type="password" required />
            <i class="icon-eye-toggle"></i> </div>
          
          <button type="submit" class="primary-button">Register</button>

          <p class="toggle-auth">
            Already have an account?
            <a href="#" @click.prevent="isLogin = true" class="signup-link">Login</a>
          </p>
        </form>

        <div class="footer-links">
          <a href="https://itbienvenu.github.io/expense-tracker/docs/api/authentication">Documentation</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
// environment api url variable
const BASE_API_URL = import.meta.env.VITE_APP_API_URL;

const isLogin = ref(true); // Toggle between Login and Register
const username = ref('');
const email = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = async () => {
  try {
    const response = await axios.post(`${BASE_API_URL}/auth/login`, {
      email: email.value,
      hashed_password: password.value,
    });
    const { access_token } = response.data;
    localStorage.setItem('accessToken', access_token);
    alert('Login successful!'); 
    router.push('/dashboard');
  } catch (error) {
    alert(error.response?.data?.detail || 'Login failed.'); 
  }
};

const handleRegister = async () => {
  try {
    const response = await axios.post(`${BASE_API_URL}/auth/register`, {
      username: username.value,
      email: email.value,
      password: password.value,
    });
    alert(response.data.detail || 'Registration successful! You can now log in.'); 
    isLogin.value = true; // Switch to login form after registration
  } catch (error) {
    alert(error.response?.data?.detail || 'Registration failed.'); 
  }
};
</script>

<style scoped>
.split-screen-container {
  display: flex;
  min-height: 100vh;
  background-color: #000000;
  color: #FFFFFF;
  font-family: 'Inter', sans-serif; 
  overflow: hidden;
}


.marketing-panel {
  flex: 1; 
  background: 
    linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url('../assets/hero.webp') no-repeat center center;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  min-height: 100vh;
}

.overlay-content {
  text-align: center;
  color: #FFFFFF;
  padding: 2rem;
}

.sinc-logo {
  font-size: 4rem;
  font-weight: bold;
  color: #E7A428;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5); 
}

.tagline {
  font-size: 1.8rem;
  max-width: 400px;
  line-height: 1.4;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.4);
}


.auth-panel {
  flex: 1; 
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #000000; 
  padding: 2rem;
  position: relative; 
}

.auth-card {
  width: 100%;
  max-width: 400px; 
  padding: 2rem;
  border-radius: 8px; 
  text-align: center; 
}

.logo-placeholder {
  margin-bottom: 2rem;
  display: inline-flex; /* To center it */
}

.form-title {
  font-size: 2.2rem;
  font-weight: 600;
  color: #FFFFFF;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  color: #AAAAAA; 
  margin-bottom: 2rem;
  font-size: 1rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-group i {
  position: absolute;
  left: 15px;
  color: #AAAAAA; 
  font-size: 1.1rem;
}


input {
  width: 100%;
  padding: 1rem 1rem 1rem 3.5rem;
  background-color: #1C1C1C; 
  border: 1px solid #333333; 
  border-radius: 6px;
  color: #FFFFFF;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input::placeholder {
  color: #AAAAAA;
}

input:focus {
  border-color: #E7A428; /* Gold/Orange border on focus */
  outline: none;
}

.forgot-password {
  display: block; /* To push it to its own line */
  text-align: right;
  color: #E7A428; /* Gold/Orange for links */
  text-decoration: none;
  font-size: 0.9rem;
  margin-top: -0.5rem; /* Adjust spacing */
  margin-bottom: 0.5rem;
}

.primary-button {
  width: 100%;
  padding: 1rem;
  background-color: #E7A428; /* Gold/Orange button */
  border: none;
  border-radius: 6px;
  color: #000000; /* Black text on gold button */
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.primary-button:hover {
  background-color: #D4901C; /* Slightly darker gold on hover */
}

.separator {
  color: #AAAAAA;
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
}

.separator::before,
.separator::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%; 
  height: 1px;
  background-color: #333333;
}

.separator::before {
  left: 0;
}

.separator::after {
  right: 0;
}

.google-button {
  width: 100%;
  padding: 1rem;
  background-color: #1C1C1C; /* Dark grey background */
  border: 1px solid #333333;
  border-radius: 6px;
  color: #FFFFFF;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.google-button:hover {
  background-color: #2a2a2a;
  border-color: #555555;
}

.google-icon {
  width: 20px;
  height: 20px;
}

.toggle-auth {
  color: #AAAAAA;
  margin-top: 2rem; /* Spacing for this text */
  font-size: 0.95rem;
}

.signup-link {
  color: #E7A428; /* Gold/Orange for the "Signup" or "Login" link */
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.5rem;
}

.signup-link:hover {
  text-decoration: underline;
}

.footer-links {
  position: absolute;
  bottom: 2rem; /* Position at the bottom of the auth-panel */
  width: calc(100% - 4rem); /* Adjust width to match padding */
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}

.footer-links a {
  color: #AAAAAA;
  text-decoration: none;
  font-size: 0.85rem;
}

.footer-links a:hover {
  color: #FFFFFF;
  text-decoration: underline;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .marketing-panel {
    display: none; 
  }
  .auth-panel {
    flex: none; 
    width: 100%; 
  }
  .split-screen-container {
    flex-direction: column;
  }
  .auth-panel .footer-links {
    position: static;
    margin-top: 2rem; 
  }
}
</style>