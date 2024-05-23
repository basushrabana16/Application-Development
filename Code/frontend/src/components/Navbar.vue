<template>
  <nav class="navbar navbar-expand-lg custom-bg-color">
    <div class="container-fluid">
      <a class="navbar-brand" >Grocery</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item" v-if="showHome">
            <router-link to="/" class="nav-link active" aria-current="page">Home</router-link>
          </li>
          <li class="nav-item" v-if="showAdminHome">
            <router-link to="/admin-dashboard" class="nav-link active" aria-current="page">Home</router-link>
          </li>
          <li class="nav-item" v-if="showManagerHome">
            <router-link to="/manager-dashboard" class="nav-link active" aria-current="page">Home</router-link>
          </li>
          <li class="nav-item" v-if="showUserHome">
            <router-link to="/user-dashboard" class="nav-link active" aria-current="page">Home</router-link>
          </li>
          <li class="nav-item" v-if="showAccountLink">
            <router-link to="/login" class="nav-link">Account</router-link>
          </li>
          <li class="nav-item" v-if="showCartLink">
            <router-link to="/cart" class="nav-link">Cart</router-link>
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Menu
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="#">Action</a></li>
              <li><a class="dropdown-item" href="#">Another action</a></li>
              <li><hr class="dropdown-divider" /></li>
              <li><a class="dropdown-item" href="#">Something else here</a></li>
            </ul>
          </li>
          <li>
            <button v-if="showLogoutButton" class="btn btn-outline-danger" @click="logout">Logout</button>
          </li>
        </ul>
        <form class="d-flex" role="search" @submit.prevent="handleSearch">
        <input
          class="form-control me-2"
          type="search"
          placeholder="Search"
          aria-label="Search"
          v-model="searchQuery"
        />
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
      </div>
    </div>
  </nav>
</template>
  
<script>
import axios from "@/axios";

export default {
  name: "AppNavbar",
  data() {
    return {
      searchQuery: ""
    };
  },

  computed:{
    showHome() {
      const allowedPaths = ['/', '/search','/login', '/register'];
      return allowedPaths.includes(this.$route.path);
    },
    showAdminHome() {
      const excludedPaths = ['/', '/search','/cart', '/register', '/login', '/manager-dashboard', '/user-dashboard', '/user-item', '/manager-item', '/add-item', '/edit-item',];
      return !excludedPaths.includes(this.$route.path);
    },
    showManagerHome() {
      const excludedPaths = ['/', '/search','/cart', '/register', '/login', '/admin-dashboard', '/user-dashboard','/category', '/user-item', '/add-category', '/all-user', '/edit-category'];
      return !excludedPaths.includes(this.$route.path);
    },
    showUserHome() {
      const excludedPaths = ['/', '/search','/register', '/login', '/admin-dashboard', '/manager-dashboard','/category', '/add-category', '/add-item', '/all-user','/edit-category', '/edit-item', '/manager-item'];
      return !excludedPaths.includes(this.$route.path);
    },
    showAccountLink() {
      return this.$route.path === '/';
    },
    showCartLink() {
      const allowedPaths = ['/user-dashboard', '/user-item'];
      return allowedPaths.includes(this.$route.path);
    },
    showLogoutButton() {
      const excludedPaths = ['/', '/search','/register', '/login',];
      return !excludedPaths.includes(this.$route.path);
    },
  },

  methods: {
    async logout() {
      try {
        await axios.get("/logout");
        this.$router.push('/');
        }catch (error) {
        console.error("Logout error:", error);
      }
    },
    navigateToHome() {
      this.$router.push('/');
    },
    navigateToLogin() {
      this.$router.push('/login');
    },
    async handleSearch() {
      try {
        if (!this.searchQuery) {
          return; // Don't perform empty searches
        }

        const response = await axios.post("/search", {
          search_query: this.searchQuery
        });

        // Handle the search results (e.g., update a component with the results)
        this.$router.push({ name: "search", query: { q: this.searchQuery } });
        console.log(response.data); // Display the search results
      } catch (error) {
        console.error("Axios error:", error);
      }
    }
  },
};
</script>
  
<style>
.navbar {
  background-color: #b5fc65;
  color: white;
}
</style>