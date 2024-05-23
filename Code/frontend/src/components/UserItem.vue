<template>
    <div>
      <div class="card text-center">
        <div class="card-header">Latest items</div>
        <img src="" class="card-img" alt="..." />
        <div class="card-body">
          <h5 class="card-title">All items are displayed here</h5>
          <p class="card-text">
            User can add items of their choice to cart.
          </p>
        </div>
      </div>
      <div class="row row-cols-1 row-cols-md-5 g-4">

        <div v-for="item in items" :key="item.id" class="card">
          <img :src="item.iimg" alt="Item Image" style="width: 100%" />
          <h1>{{ item.name }}</h1>
          <p class="price">${{ item.price }}</p>
          <p>{{ item.description }}</p>
          <button @click="addToCart(item)">Add to Cart</button>
        </div>
      </div>
    </div>
  </template>

<script>
import axios from "@/axios";

export default {
  name: "UserItem",
  data() {
    return {
      items: [],
      cart: []
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

    async addToCart(item) {
      try {
        const response = await axios.post(`/add-to-cart/${item.id}`, {
          item_id: item.id,
          quantity: 1,
        });
        console.log(response.data.message);
      } catch (error) {
        console.error("Axios error:", error);
      }
    }

  },
};
</script>

  
<style>

</style>