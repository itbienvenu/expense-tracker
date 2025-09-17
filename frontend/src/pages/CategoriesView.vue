<template>
  <div class="card bg-dark text-white border-secondary mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h4 class="mb-0">Categories</h4>
      <button @click="showAddForm = true" class="btn btn-warning">+ Add New Category</button>
    </div>

    <div v-if="showAddForm || editingCategory" class="card-body">
      <form @submit.prevent="saveCategory">
        <div class="mb-3">
          <input v-model="categoryName" class="form-control bg-dark text-light border-secondary" placeholder="Category Name" required />
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
// The script section remains the same as before, no changes needed to the logic
import { ref, onMounted } from 'vue';
import axios from 'axios';
// ... (rest of the script)
</script>