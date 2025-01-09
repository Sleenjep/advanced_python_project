<template>
  <div class="cart-view">
    <div v-if="isLoading">Loading...</div>
    <div v-else>
      <h2>Cart</h2>
      <div v-if="error" class="error-message">
        <p>{{ error }}</p>
      </div>
      <div v-else-if="cart.length" class="cart-items">
        <div v-for="item in cart" :key="item.product_id" class="cart-item">
          <h3>{{ item.product_name }}</h3>
          <p><strong>Price:</strong> ${{ item.price ? item.price.toFixed(2) : '0.00' }}</p>
          <p><strong>Quantity:</strong>
            <button @click="decrementQuantity(item.product_id)" :disabled="item.quantity <= 1">-</button>
            {{ item.quantity }}
            <button @click="incrementQuantity(item.product_id)">+</button>
          </p>
          <p><strong>Total:</strong> ${{ item.price && item.quantity ? (item.price * item.quantity).toFixed(2) : '0.00' }}</p>
          <button @click="removeFromCart(item.product_id)">Remove</button>
        </div>
        <div class="cart-total">
          <h2>Total: ${{ totalPrice.toFixed(2) }}</h2>
          <button class="checkout-button" @click="checkout">Checkout</button>
        </div>
      </div>
      <div v-else>
        <p>Your cart is empty.</p>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        cart: [],
        error: null,
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
          await this.fetchCart();
        } catch (error) {
          console.error("Error fetching data:", error);
        }
        setTimeout(() => {
          this.isLoading = false;
        }, 500);
      },
      async fetchCart() {
        try {
          const response = await fetch("http://localhost:8000/cart/get_cart", {
            method: "GET",
            credentials: "include",
          });
          const data = await response.json();
          if (response.ok) {
            this.cart = data.cart.map(item => ({
              ...item,
              price: item.price || 0,
              quantity: item.quantity || 1,
            }));
          } else {
            this.error = data.error || "Error loading cart.";
          }
        } catch (error) {
          this.error = "Connection error.";
        }
      },
      async incrementQuantity(productId) {
        try {
          const formData = new FormData();
          formData.append("product_id", productId);
          const response = await fetch("http://localhost:8000/cart/increment_quantity", {
            method: "POST",
            body: formData,
            credentials: "include",
          });
          if (response.ok) {
            const updatedItem = this.cart.find(item => item.product_id === productId);
            if (updatedItem) {
              updatedItem.quantity += 1;
            }
          }
        } catch {
          console.log("Connection error.");
        }
      },
      async decrementQuantity(productId) {
        try {
          const formData = new FormData();
          formData.append("product_id", productId);
          const response = await fetch("http://localhost:8000/cart/decrement_quantity", {
            method: "POST",
            body: formData,
            credentials: "include",
          });
          if (response.ok) {
            const updatedItem = this.cart.find(item => item.product_id === productId);
            if (updatedItem && updatedItem.quantity > 1) {
              updatedItem.quantity -= 1;
            }
          }
        } catch {
          console.log("Connection error.");
        }
      },
      async removeFromCart(productId) {
        try {
          const formData = new FormData();
          formData.append("product_id", productId);
          const response = await fetch("http://localhost:8000/cart/delete_from_cart", {
            method: "POST",
            body: formData,
            credentials: "include",
          });
          if (response.ok) {
            this.cart = this.cart.filter(item => item.product_id !== productId);
          }
        } catch {
          console.log("Connection error.");
        }
      },
      async checkout() {
        try {
          const response = await fetch("http://localhost:8000/cart/generate_receipt", {
            method: "GET",
            credentials: "include",
          });
          if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            window.open(url, "_blank");
          }
        } catch (error) {
          console.log("Connection error.", error);
        }
      },
    },
    computed: {
      totalPrice() {
        return this.cart.reduce((total, item) => total + item.price * item.quantity, 0);
      },
    },
  };
</script>

<style scoped>
  .cart-view {
    margin: 20px;
  }
  .cart-items {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  .cart-item {
    border: 1px solid #ccc;
    padding: 15px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 300px;
  }
  .cart-total {
    margin-top: 20px;
    text-align: right;
  }
  .checkout-button {
    background-color: #28a745;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .checkout-button:hover {
    background-color: #218838;
  }
  .error-message {
    color: red;
    font-weight: bold;
    text-align: center;
    margin: 20px 0;
  }
  button {
    font-size: 14px;
    padding: 5px 10px;
    margin: 1px 5px;
  }
  button:disabled {
    background-color: #e0e0e0;
    cursor: not-allowed;
  }
</style>