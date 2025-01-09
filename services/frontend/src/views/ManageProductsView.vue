<template>
  <div class="manage-products-view">
    <div v-if="isLoading">Loading...</div>
    <div v-else>
      <h3 style="margin-top: 20px;">Product List</h3>
      <table v-if="products.length" class="product-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Department</th>
            <th>Aisle</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>
              <a :href="`/product/${product.id}`">{{ product.name }}</a>
            </td>
            <td>{{ product.price }}</td>
            <td>{{ product.department_id }}</td>
            <td>{{ product.aisle_id }}</td>
            <td class="action-buttons">
              <button @click="editProduct(product)" class="edit-button">Edit</button>
              <button @click="deleteProduct(product.id)" class="delete-button">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No products found.</p>
      <h3>Add New Product</h3>
      <form @submit.prevent="addProduct" class="add-product-form">
        <input type="text" v-model="name" placeholder="Name" required>
        <input type="text" v-model="price" placeholder="Price" required>
        <input type="text" v-model="department" placeholder="Department" required>
        <input type="text" v-model="aisle" placeholder="Aisle" required>
        <button type="submit">Add</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        name: '',
        price: '',
        department: '',
        aisle: '',
        products: [],
        backend_response: null,
        error: null,
        successMessage: null,
        user_info: null,
        editingProduct: null,
        sliderValue: 50,
        isLoading: true,
      };
    },
    mounted() {
      this.fetchUserInfo();
      this.fetchProducts();
      setTimeout(() => {
        this.isLoading = false;
      }, 500);
    },
    methods: {
      async fetchUserInfo() {
        try {
          const response = await fetch('http://localhost:8000/auth/get_user', {
            method: 'GET',
            headers: { 'Accept': 'application/json' },
            credentials: 'include',
          });

          const data = await response.json();
          this.user_info = data.username;
        } catch (error) {
          this.user_info = 'Error fetching user information';
        }
      },
      async fetchProducts() {
        try {
          const response = await fetch('http://localhost:8000/products/get_all_products');
          const data = await response.json();

          if (response.ok && data.products) {
            console.log(data.products[0])
            this.products = data.products;
          } else {
            this.error = data.error || 'Error loading products.';
          }
        } catch (error) {
          this.error = 'Connection error with server.';
        }
      },
      async addProduct() {
        try {
          const response = await fetch('http://localhost:8000/products/add_product', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `name=${this.name}&price=${this.price}&department=${this.department}&aisle=${this.aisle}`,
          });

          const backend_response = await response.json();

          if (response.ok) {
            this.successMessage = 'Product successfully added!';
            this.error = null;
            this.resetForm();
            this.fetchProducts();
          } else {
            this.error = backend_response.error || 'Error adding product.';
            this.successMessage = null;
          }
        } catch (error) {
          this.error = 'Connection error with server.';
          this.successMessage = null;
        }
      },
      async deleteProduct(productId) {
        try {
          const response = await fetch('http://localhost:8000/products/delete_product', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `product_id=${productId}`,
          });

          const data = await response.json();

          if (response.ok) {
            this.successMessage = data.message || 'Product successfully deleted!';
            this.error = null;
            this.fetchProducts();
          } else {
            this.error = data.error || 'Error deleting product.';
            this.successMessage = null;
          }
        } catch (error) {
          this.error = 'Connection error with server.';
          this.successMessage = null;
        }
      },
      editProduct(product) {
        this.editingProduct = product;
        this.name = product.name;
        this.price = product.price;
        this.department = product.department;
        this.aisle = product.aisle;
      },
      resetForm() {
        this.name = '';
        this.price = '';
        this.department = '';
        this.aisle = '';
        this.editingProduct = null;
      },
    },
  };
</script>

<style scoped>
  .manage-products-view {
    margin: 20px;
  }

  .product-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
  }

  .product-table th, .product-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }

  .product-table th {
    background-color: #0480b6;
    color: white;
  }

  .product-table a {
    color: #0480b6;
    text-decoration: none;
  }

  .product-table a:hover {
    text-decoration: underline;
  }

  .product-table td.action-buttons {
    text-align: center;
  }

  .edit-button, .delete-button {
    margin-left: 5px;
    padding: 5px 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .edit-button {
    background-color: #4caf50;
    color: white;
  }

  .edit-button:hover {
    background-color: #388e3c;
  }

  .delete-button {
    background-color: #ff5722;
    color: white;
  }

  .delete-button:hover {
    background-color: #e64a19;
  }

  .add-product-form {
    display: flex;
    gap: 10px;
    margin-top: 20px;
  }

  button {
    padding: 10px 15px;
    background-color: #0480b6;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:hover {
    background-color: #03699a;
  }

  .error {
    color: red;
    margin-top: 10px;
  }

  .success {
    color: green;
    margin-top: 10px;
  }

  .slider-container {
    margin-top: 20px;
  }

  input[type="range"] {
    width: 100%;
  }
</style>
