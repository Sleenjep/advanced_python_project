<template>
  <div class="info-view">
    <div v-if="isLoading">Loading...</div>
    <div v-else>
      <div v-if="error" class="error-message">
        <p>{{ error }}</p>
      </div>
      <div v-else-if="products.length" class="product-list">
        <div v-for="product in products" :key="product.id" class="card">
          <h2>{{ product.name }}</h2>
          <p><strong>Price:</strong> ${{ product.price ? product.price.toFixed(2) : '0.00' }}</p>
          <button v-if="!isAdmin" @click="handleButtonClick(product)" :class="{'in-cart': isProductInCart(product.id)}">
            {{ isProductInCart(product.id) ? 'Go to Cart' : 'Add to Cart' }}
          </button>
        </div>
      </div>
      <div v-else>
        <p>No products available.</p>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        products: [],
        error: null,
        isAdmin: false,
        user_info: null,
        cart: [],
        isLoading: true,
      };
    },
    async created() {
      await this.fetchData();
    },
    methods: {
      async fetchData() {
        this.isLoading = true;
        try {
          await Promise.all([this.fetchUserInfo(), this.fetchProducts(), this.fetchCart()]);
        } catch (error) {
          console.error('Error fetching data:', error);
          this.error = 'Connection error.';
        } finally {
          setTimeout(() => {
            this.isLoading = false;
          }, 500);
        }
      },
      async fetchUserInfo() {
        try {
          const response = await fetch('http://localhost:8000/auth/get_user', {
            method: 'GET',
            headers: { 'Accept': 'application/json' },
            credentials: 'include',
          });

          const data = await response.json();
          if (response.ok) {
            this.user_info = data.username;
            this.isAdmin = data.is_admin || false;
          } else {
            this.error = data.error || 'Error fetching user information.';
          }
        } catch (error) {
          this.error = 'Connection error.';
        }
      },
      async fetchCart() {
        try {
          const response = await fetch('http://localhost:8000/cart/get_cart', {
            method: 'GET',
            credentials: 'include',
          });

          const data = await response.json();
          if (response.ok) {
            this.cart = data.cart;
          } else {
            this.error = data.error || 'Error loading cart.';
          }
        } catch (error) {
          this.error = 'Connection error.';
        }
      },
      isProductInCart(productId) {
        return this.cart.some(item => item.product_id === productId);
      },
      async handleButtonClick(product) {
        if (this.isProductInCart(product.id)) {
          this.$router.push('/cart');
        } else {
          await this.addToCart(product);
        }
      },
      async addToCart(product) {
        try {
          const formData = new FormData();
          formData.append('product_id', product.id);
          formData.append('quantity', 1);

          const response = await fetch('http://localhost:8000/cart/add_to_cart', {
            method: 'POST',
            body: formData,
            credentials: 'include',
          });

          if (response.ok) {
            await this.fetchCart();
          } else {
            const errorData = await response.json();
            this.error = `Error: ${errorData.detail || 'Failed to add product to cart.'}`;
          }
        } catch (error) {
          this.error = 'Connection error.';
        }
      },
      async fetchProducts() {
        try {
          const response = await fetch('http://localhost:8000/products/get_all_products');
          const data = await response.json();

          if (response.ok) {
            this.products = data.products;
          } else {
            this.error = data.error || 'Error loading products.';
          }
        } catch (error) {
          this.error = 'Connection error.';
        }
      },
    },
  };
</script>

<style scoped>
  .info-view {
    margin: 20px;
  }

  .product-list {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    justify-content: center;
    margin-top: 25px;
  }

  .card {
    flex: 1 1 calc(25% - 15px);
    max-width: calc(25% - 15px);
    text-align: center;
    border: 1px solid #ccc;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
  }

  .card h2 {
    font-size: 1.5em;
    margin-bottom: 10px;
  }

  .card button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .card button:hover {
    background-color: #0056b3;
  }

  .card button.in-cart {
    background-color: #023c7a;
  }

  .error-message {
    color: red;
    font-weight: bold;
    text-align: center;
    margin: 20px 0;
  }
</style>