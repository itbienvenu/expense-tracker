<template>
  <div class="card bg-dark text-white border-secondary mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h4 class="mb-0">Transactions</h4>
      <button @click="showAddForm = true" class="btn btn-warning">+ Add New Transaction</button>
    </div>

    <div v-if="showAddForm || editingTransaction" class="card-body">
      <form @submit.prevent="saveTransaction">
        <div class="mb-3">
          <label for="title" class="form-label">Title</label>
          <input id="title" v-model="title" class="form-control bg-dark text-light border-secondary" placeholder="Title" required />
        </div>
        <div class="mb-3">
          <label for="type" class="form-label">Type</label>
          <select id="type" v-model="type" class="form-select bg-dark text-light border-secondary" required>
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="amount" class="form-label">Amount</label>
          <input id="amount" v-model="amount" type="number" step="0.01" class="form-control bg-dark text-light border-secondary" placeholder="Amount" required />
        </div>
        <div class="mb-3">
          <label for="date" class="form-label">Date</label>
          <input id="date" v-model="date" type="date" class="form-control bg-dark text-light border-secondary" required />
        </div>
        <div class="mb-3">
          <label for="category" class="form-label">Category</label>
          <select id="category" v-model="selectedCategory" class="form-select bg-dark text-light border-secondary" required>
            <option disabled value="">Please select a category</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>
        
        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-warning">{{ editingTransaction ? 'Update' : 'Create' }}</button>
          <button @click="cancelEdit" type="button" class="btn btn-outline-light">Cancel</button>
        </div>
      </form>
    </div>

    <ul class="list-group list-group-flush">
      <li v-for="transaction in transactions" :key="transaction.id" class="list-group-item d-flex justify-content-between align-items-center bg-dark text-white border-secondary">
        <div>
          <h6 class="mb-1">{{ transaction.title }}</h6>
          <small class="text-muted">{{ new Date(transaction.date).toLocaleDateString() }}</small>
          <div>
            <span v-for="cat in transaction.categories" :key="cat.id" class="badge rounded-pill bg-secondary me-1">{{ cat.name }}</span>
          </div>
        </div>
        <div class="d-flex align-items-center gap-2">
          <span class="fw-bold fs-5" :class="{'text-danger': transaction.amount < 0, 'text-success': transaction.amount >= 0}">
            ${{ Math.abs(transaction.amount).toFixed(2) }}
          </span>
          <div class="btn-group">
            <button @click="editTransaction(transaction)" class="btn btn-sm btn-outline-info">Edit</button>
            <button @click="deleteTransaction(transaction.id)" class="btn btn-sm btn-outline-danger">Delete</button>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const transactions = ref([]);
const categories = ref([]); // To store fetched categories for the dropdown
const showAddForm = ref(false);
const editingTransaction = ref(null);
const title = ref('');
const amount = ref(0);
const date = ref('');
const selectedCategory = ref('');
const type = ref('expense'); // New state variable for transaction type

const getHeaders = () => {
  const token = localStorage.getItem('accessToken');
  return { Authorization: `Bearer ${token}` };
};

const fetchTransactions = async () => {
  try {
    const response = await axios.get('http://localhost:8000/tracker/transactions', { headers: getHeaders() });
    transactions.value = response.data;
  } catch (error) {
    console.error('Failed to fetch transactions:', error);
  }
};

const fetchCategories = async () => {
  try {
    const response = await axios.get('http://localhost:8000/tracker/categories', { headers: getHeaders() });
    categories.value = response.data;
  } catch (error) {
    console.error('Failed to fetch categories:', error);
  }
};

const saveTransaction = async () => {
  // Determine the final amount based on the type
  const finalAmount = type.value === 'expense' ? -Math.abs(amount.value) : Math.abs(amount.value);

  const payload = {
    title: title.value,
    amount: parseFloat(finalAmount), // Use the determined final amount
    date: new Date(date.value).toISOString(),
    category_ids: [selectedCategory.value],
  };

  try {
    if (editingTransaction.value) {
      // PATCH request to update
      await axios.patch(`http://localhost:8000/tracker/transactions/${editingTransaction.value.id}`, payload, { headers: getHeaders() });
      editingTransaction.value = null;
    } else {
      // POST request to create
      await axios.post('http://localhost:8000/tracker/transactions', payload, { headers: getHeaders() });
      showAddForm.value = false;
    }
    resetForm();
    fetchTransactions(); // Refresh the list
  } catch (error) {
    console.error('Failed to save transaction:', error);
  }
};

const editTransaction = (transaction) => {
  editingTransaction.value = transaction;
  title.value = transaction.title;
  date.value = new Date(transaction.date).toISOString().split('T')[0];
  selectedCategory.value = transaction.categories[0]?.id || '';
  
  // Set the amount and type based on the transaction's sign
  amount.value = Math.abs(transaction.amount);
  type.value = transaction.amount < 0 ? 'expense' : 'income';
  showAddForm.value = true; // Show the form for editing
};

const cancelEdit = () => {
  editingTransaction.value = null;
  showAddForm.value = false;
  resetForm();
};

const resetForm = () => {
  title.value = '';
  amount.value = 0;
  date.value = '';
  selectedCategory.value = '';
  type.value = 'expense'; // Reset type to default
};

const deleteTransaction = async (id) => {
  if (confirm('Are you sure you want to delete this transaction?')) {
    try {
      await axios.delete(`http://localhost:8000/tracker/transactions/${id}`, { headers: getHeaders() });
      fetchTransactions(); // Refresh the list
    } catch (error) {
      console.error('Failed to delete transaction:', error);
    }
  }
};

onMounted(() => {
  fetchTransactions();
  fetchCategories();
});
</script>