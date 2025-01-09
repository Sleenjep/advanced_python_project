<template>
  <div id="app">
    <NavigBarComp />
    <router-view></router-view>
  </div>
</template>

<script>
  import NavigBarComp from './components/NavigBarComp.vue';

  export default {
    name: 'App',
    components: {
      NavigBarComp
    },
    created() {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        this.$store.dispatch('setUser', storedUser);
      }
    },
    data() {
      return {
        user: 'User'
      };
    }
  };
</script>

<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    background-color: #e0f7fa;
    color: #003366;
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    padding: 20px;
  }

  a {
    color: #003366;
    text-decoration: none;
  }

  a:hover {
    color: #80deea;
  }

  h1, h2, h3, h4, h5, h6 {
    color: #003366;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
    margin-bottom: 10px;
  }

  h1 {
    font-size: 2.5em;
    color: #003366;
  }

  h2 {
    font-size: 2em;
  }

  h3 {
    font-size: 1.75em;
  }

  button {
    background-color: #4dd0e1;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }

  button:hover {
    background-color: #00bcd4;
    transform: translateY(-2px);
  }

  button:active {
    background-color: #0097a7;
  }

  .card {
    background-color: #ffffff;
    color: #003366;
    padding: 20px;
    margin: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .card:hover {
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  }

  input, textarea {
    background-color: #ffffff;
    color: #003366;
    border: 1px solid #003366;
    border-radius: 5px;
    padding: 10px;
    font-size: 1em;
    width: 100%;
  }

  input:focus, textarea:focus {
    outline: none;
    border-color: #4dd0e1;
  }

  input::placeholder, textarea::placeholder {
    color: #b2ebf2;
  }

  nav {
    background-color: #00bcd4;
    padding: 15px;
  }

  nav ul {
    list-style-type: none;
    text-align: center;
  }

  nav ul li {
    display: inline-block;
    margin: 0 20px;
  }

  nav ul li a {
    color: white;
    font-size: 1.2em;
  }

  nav ul li a:hover {
    color: #80deea;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
  }

  section {
    margin-bottom: 40px;
  }
</style>
