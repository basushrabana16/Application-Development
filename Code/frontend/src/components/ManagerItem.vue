<template>
  <div>
    <div class="card text-center">
      <div class="card-header">Latest items</div>
      <img src="" class="card-img" alt="..." />
      <div class="card-body">
        <h5 class="card-title">All items are displayed here</h5>
        <p class="card-text">
          By clicking the button below manager will be able to add new items
        </p>
        <router-link to="/add-item" class="btn btn-primary"
          >Add New item</router-link
        >
      </div>
    </div>
    <div class="row row-cols-1 row-cols-md-5 g-4">
      <div v-for="item in items" :key="item.id" class="card">
        <img :src="item.iimg" alt="Item Image" style="width: 100%" />
        <h1>{{ item.name }}</h1>
        <p class="price">${{ item.price }}</p>
        <p>{{ item.description }}</p>
        <button @click="editItem(item.id)">Edit</button>
        <button @click="deleteItem(item.id)">Delete</button>
      </div>
    </div>
  </div>
</template>
  
  
  
<script>
import axios from "@/axios";

export default {
  name: "ManagerItem",
  data() {
    return {
      items: [],
    };
  },
  created() {
    this.fetchItems();
  },
  methods: {
    async fetchItems() {
      try {
        const response = await axios.get("/items"); // Adjust the API endpoint
        this.items = response.data;
      } catch (error) {
        console.error("Axios error:", error);
      }
    },

    async editItem(itemId) {
      this.$router.push(`/edit-item/${itemId}`);
    },

    async deleteItem(itemId) {
      try {
        const response = await axios.delete(`/items/${itemId}`);
        if (response.status === 204) {
          this.fetchItems();
        }
      } catch (error) {
        console.error("Axios error:", error);

        if (error.response) {
          console.log("Response data:", error.response.data);
        }
      }
    },
  },
};
</script>

  
<style>
</style>