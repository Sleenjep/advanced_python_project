<template>
  <div class="profile-view">
    <p>{{ user_info }}</p>
  </div>
</template>
  
<script>
  export default {
    data() {
      return {
        user_info: null,
      };
    },
    async mounted() {
      await this.fetchUserInfo();
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
        
        console.log("ProfileView", this.user_info)

      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    }

    },
  };
</script>
  
<style scoped>
  .profile-view {
    padding: 20px;
    background-color: #f4f4f9;
    border-radius: 8px;
    width: 60%;
    margin: 0 auto;
  }

  .profile-view p {
    font-size: 18px;
    color: #666;
  }
</style>
  