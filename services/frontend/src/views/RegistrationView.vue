<template>
  <div class="registration-container">
    <div class="registration-box">
      <h1>Registration</h1>
      <form>
        <div>
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="username" />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" />
        </div>
        <button type="button" @click="register">Register</button>
        <p>Already have an account? <a href="/login">Login</a></p>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        username: '',
        password: '',
        backend_response: null,
        error: null,
        user_info: null,
      };
    },
    methods: {
      async register() {
        try {
          const response = await fetch('http://localhost:8000/auth/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${this.username}&password=${this.password}`,
            credentials: 'include',
          });

          this.backend_response = await response.json();
          this.error = this.backend_response.error;
      
          this.$router.push('/login');

        } catch (error) {
          console.error('Error registering user:', error);
          this.error = 'An error occurred during registration.';
        }
      },

      async fetchUserInfo() {
        try {
          const response = await fetch('http://localhost:8000/auth/get_user', {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
            },
            credentials: 'include',
          });

          if (response.ok) {
            const userInfo = await response.text();
            this.user_info = userInfo;
            console.log('User Info:', userInfo);
          } else {
            console.error('Failed to fetch user info:', response.status, response.statusText);
            this.user_info = null;
          }
        } catch (error) {
          console.error('Error fetching user info:', error);
          this.user_info = null;
        }
      },
    },
  };
</script>

<style scoped>
  html, body {
    height: 100%;
    margin: 0;
    overflow: hidden;
  }

  .registration-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    height: 50vh;
    padding-top: 50px;
  }

  .registration-box {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 300px;
  }

  h1 {
    text-align: center;
    font-size: 24px;
    margin-bottom: 1rem;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  label {
    font-size: 16px;
    margin-bottom: 5px;
  }

  input {
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  button {
    padding: 10px;
    font-size: 16px;
    background-color: #0480b6;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #007bb5;
  }

  p {
    text-align: center;
    font-size: 14px;
  }

  a {
    color: #0480b6;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }

  .error {
    color: red;
    font-size: 14px;
    text-align: center;
  }
</style>
