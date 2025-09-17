<template>
  <div>
  <div class="card bg-dark text-white border-secondary mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h4 class="mb-0">Categories</h4>
      <button @click="openAddModal" class="btn btn-warning">+ Add New Category</button>
    </div>

    <div class="card-body">
      <div v-if="categories.length === 0" class="text-center text-muted py-4">
          No categories found. Click "Add New Category" to get started!
      </div>
      <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div class="col" v-for="category in categories" :key="category.id">
          <div class="category-card card h-100 bg-dark text-white border-secondary shadow-sm">
            <div class="card-body d-flex flex-column align-items-center justify-content-center">
              <h5 class="card-title text-center mb-3">{{ category.name }}</h5>
              <div class="btn-group mt-auto">
                <button @click="openEditModal(category)" class="btn btn-sm btn-outline-info">Edit</button>
                <button @click="deleteCategory(category.id)" class="btn btn-sm btn-outline-danger">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="categoryModal" tabindex="-1" aria-labelledby="categoryModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark text-white border-secondary">
        <div class="modal-header border-secondary">
          <h5 class="modal-title" id="categoryModalLabel">{{ editingCategory ? 'Edit Category' : 'Add New Category' }}</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form @submit.prevent="saveCategory">
          <div class="modal-body">
            <div class="mb-3">
              <label for="modalCategoryName" class="form-label">Category Name</label>
              <input 
                id="modalCategoryName"
                v-model="categoryName" 
                class="form-control bg-dark text-light border-secondary" 
                placeholder="e.g., Groceries, Rent, Salary" 
                required 
              />
            </div>
          </div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Cancel</button>
            <button type="submit" class="btn btn-warning">{{ editingCategory ? 'Update' : 'Create' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>  
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { Modal } from 'bootstrap'; 

const BASE_API_URL = import.meta.env.VITE_APP_API_URL;

const categories = ref([]);
const editingCategory = ref(null);
const categoryName = ref('');

let categoryModalInstance = null; 

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

const openAddModal = () => {
  editingCategory.value = null; 
  resetForm(); 
  categoryModalInstance.show(); 
};

const openEditModal = (category) => {
  editingCategory.value = category;
  categoryName.value = category.name;
  categoryModalInstance.show(); 
};

const saveCategory = async () => {
  const payload = {
    name: categoryName.value,
  };

  try {
    if (editingCategory.value) {
      await axios.put(`${BASE_API_URL}/tracker/categories/${editingCategory.value.id}`, payload, { headers: getHeaders() }); // Assuming PATCH for update
    } else {
      await axios.post(`${BASE_API_URL}/tracker/categories`, payload, { headers: getHeaders() });
    }
    
    categoryModalInstance.hide(); 
    resetForm(); 
    fetchCategories(); 
  } catch (error) {
    console.error('Failed to save category:', error);
  }
};

const resetForm = () => {
  categoryName.value = '';
};

const deleteCategory = async (id) => {
  if (confirm('Are you sure you want to delete this category? This will also affect related transactions.')) {
    try {
      await axios.delete(`${BASE_API_URL}/tracker/categories/${id}`, { headers: getHeaders() });
      fetchCategories(); 
    } catch (error) {
      console.error('Failed to delete category:', error);
    }
  }
};

onMounted(() => {
  fetchCategories();
  const modalElement = document.getElementById('categoryModal');
  if (modalElement) {
    categoryModalInstance = new Modal(modalElement);
    modalElement.addEventListener('hidden.bs.modal', () => {
      if (!editingCategory.value) { 
        resetForm();
      }
      editingCategory.value = null; 
    });
  }
});
</script>

<style scoped>
.category-card {
  /* Add subtle styling for category cards */
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  /* Adjust min-height to give enough space for content */
  min-height: 150px; /* Example min-height, adjust as needed */
}
.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.card-title {
  font-size: 1.5rem; /* Larger font for category name */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%; /* Ensure text truncation works */
}

/* To vertically center content and allow buttons to be at the bottom */
.category-card .card-body {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center content horizontally */
  justify-content: center; /* Center content vertically */
}
.category-card .btn-group {
    margin-top: auto; /* Push buttons to the bottom */
}
</style>