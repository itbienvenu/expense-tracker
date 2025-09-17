<template>
  <div class="card bg-dark text-white border-secondary mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h4 class="mb-0">Categories</h4>
      <button @click="showAddForm = true" class="btn btn-warning">+ Add New Category</button>
    </div>

    <div v-if="showAddForm || editingCategory" class="card-body">
      <form @submit.prevent="saveCategory">
        <div class="mb-3">
          <label for="categoryName" class="form-label">Category Name</label>
          <input 
            id="categoryName"
            v-model="categoryName" 
            class="form-control bg-dark text-light border-secondary" 
            placeholder="e.g., Groceries, Rent, Salary" 
            required 
          />
        </div>
        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-warning">{{ editingCategory ? 'Update' : 'Create' }}</button>
          <button @click="cancelEdit" type="button" class="btn btn-outline-light">Cancel</button>
        </div>
      </form>
    </div>

    <ul class="list-group list-group-flush">
      <li v-for="category in categories" :key="category.id" class="list-group-item d-flex justify-content-between align-items-center bg-dark text-white border-secondary">
        <span class="me-auto">{{ category.name }}</span>
        <div class="btn-group">
          <button @click="editCategory(category)" class="btn btn-sm btn-outline-info">Edit</button>
          <button @click="deleteCategory(category.id)" class="btn btn-sm btn-outline-danger">Delete</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
const BASE_API_URL = import.meta.env.VITE_APP_API_URL;

const categories = ref([]);
const showAddForm = ref(false);
const editingCategory = ref(null);
const categoryName = ref('');

const getHeaders = () => {
  const token = localStorage.getItem('accessToken');
  return { Authorization: `Bearer ${token}` };
};

const fetchCategories = async () => {
  try {
    const response = await axios.get(`${BASE_API_URL}/tracker/categories`, { headers: getHeaders() });
    categories.value = response.data;
  } catch (error) {
    console.error('Failed to fetch categories:', error);
  }
};

const saveCategory = async () => {
  const payload = {
    name: categoryName.value,
  };

  try {
    if (editingCategory.value) {
      // PATCH request to update
      await axios.put(`${BASE_API_URL}/tracker/categories/${editingCategory.value.id}`, payload, { headers: getHeaders() });
      editingCategory.value = null;
    } else {
      // POST request to create
      await axios.post(`${BASE_API_URL}/tracker/categories`, payload, { headers: getHeaders() });
      showAddForm.value = false;
    }
    resetForm();
    fetchCategories(); // Refresh the list
  } catch (error) {
    console.error('Failed to save category:', error);
  }
};

const editCategory = (category) => {
  editingCategory.value = category;
  categoryName.value = category.name;
  showAddForm.value = true;
};

const cancelEdit = () => {
  editingCategory.value = null;
  showAddForm.value = false;
  resetForm();
};

const resetForm = () => {
  categoryName.value = '';
};

const deleteCategory = async (id) => {
  if (confirm('Are you sure you want to delete this category?')) {
    try {
      await axios.delete(`${BASE_API_URL}/tracker/categories/${id}`, { headers: getHeaders() });
      fetchCategories(); // Refresh  list
    } catch (error) {
      console.error('Failed to delete category:', error);
    }
  }
};

onMounted(() => {
  fetchCategories();
});
</script>