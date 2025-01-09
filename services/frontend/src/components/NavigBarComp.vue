<template>
  <div>
    <nav v-if="user === ''">
      <div class="nav-left">
        <img src="@/assets/gym_bros_logo.png" alt="Logo" class="logo" />
      </div>
      <div class="nav-right">
        <router-link to="/login">Login</router-link>
      </div>
    </nav>
    <nav v-else-if="user === 'admin'">
      <div class="nav-left">
        <router-link to="/products">
          <img src="@/assets/gym_bros_logo.png" alt="Logo" class="logo" />
        </router-link>
        <router-link to="/dashboard">Admin Dashboard</router-link>
        <router-link to="/manage_users">Manage Users</router-link>
        <router-link to="/manage_products">Manage Products</router-link>
      </div>
      <div class="nav-right">
        <a href="#" @click.prevent="logout">Logout</a>
      </div>
    </nav>
    <nav v-else>
      <div class="nav-left">
        <router-link to="/products">
          <img src="@/assets/gym_bros_logo.png" alt="Logo" class="logo" />
        </router-link>
        <router-link to="/profile">Profile</router-link>
      </div>
      <div class="nav-center" v-if="$route.path === '/products'">
        <input type="text" placeholder="Search products..." class="search-input" />
      </div>
      <div class="nav-right">
        <router-link to="/cart">
          <img src="@/assets/cart_logo.png" alt="Cart Logo" class="cart-logo" />
        </router-link>
        <a href="#" @click.prevent="logout">Logout</a>
      </div>
    </nav>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    computed: {
      user() {
        return this.$store.state.user;
      }
    },
    data() {
      return {
        cart: [],
      };
    },
    methods: {
      async logout() {
        try {
          const response = await axios.get('http://localhost:8000/auth/logout', {
            withCredentials: true,
          });

          if (response.status === 200) {
            this.$store.dispatch('clearUser');
            this.$router.push('/login');
          }
        } catch (error) {
          console.error('Error during logout:', error);
        }
      },
      handleBackButton: function () {
        this.logout();
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
          }
        } catch (error) {
          console.error('Error fetching cart:', error);
        }
      }
    },
    mounted() {
      window.addEventListener('popstate', this.handleBackButton);
      this.fetchCart();
    },
    beforeUnmount() {
      window.removeEventListener('popstate', this.handleBackButton);
    }
  };
</script>

<style scoped>
  nav {
    background-color: #0480b6;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 90px;
    box-sizing: border-box;
    top: 20px;
    left: 20px;
    right: 20px;
    border-radius: 16px 16px 16px 16px;
  }

  nav .logo {
    height: 75px;
    width: auto;
    object-fit: contain;
    display: block;
    transition: transform 0.3s ease;
  }

  nav .logo:hover {
    transform: scale(1.1);
  }

  nav .nav-left {
    display: flex;
    gap: 20px;
    align-items: center;
  }

  nav .nav-right {
    display: flex;
    gap: 20px;
    align-items: center;
  }

  nav .nav-link {
    color: white;
    text-decoration: none;
    font-size: 18px;
    transition: color 0.3s ease, transform 0.2s ease;
  }

  nav .nav-link:hover {
    color: #80deea;
    transform: translateY(-2px);
  }

  .cart-logo {
    height: 50px;
    width: auto;
    object-fit: contain;
    transition: transform 0.3s ease;
  }

  .cart-logo:hover {
    transform: scale(1.1);
  }

  nav .user-name {
    color: #ff9800;
    font-size: 18px;
    font-weight: bold;
  }

  .nav-center {
    display: flex;
    justify-content: center;
    width: 100%;
  }

  .search-input {
    padding: 10px;
    width: 400px;
    font-size: 16px;
    border-radius: 8px;
    border: none;
    outline: none;
  }
</style>
