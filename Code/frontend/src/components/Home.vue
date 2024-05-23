<template>
  <div>
    <div class="card text-center">
      <div class="card-header">Shop  your favourites</div>
      <img src="" class="card-img" alt="..." />
      <div class="card-body">
        <h5 class="card-title">Welcome to the website!</h5>
        <p class="card-text">
          This website hepls to find category spacific items to buy!
        </p>
      </div>
    </div>
    <div class="row row-cols-1 row-cols-md-5 g-4">
        <div v-for="item in items" :key="item.id" class="card">
          <img :src="item.iimg" alt="Item Image" style="width: 100%" />
          <h1>{{ item.name }}</h1>
          <p class="price">${{ item.price }}</p>
          <p>{{ item.description }}</p>
        </div>
      </div>
  </div>
</template>
  
<script>
import axios from "@/axios";

export default {
  name: "HomePage",
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
        const response = await axios.get("/items");
        this.items = response.data;
      } catch (error) {
        console.error("Axios error:", error);
      }
    },
  },
};
</script>
  
<style>
</style>