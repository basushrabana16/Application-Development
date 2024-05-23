<template>
  <div>
    <h2>Search Results</h2>
    <div class="row row-cols-1 row-cols-md-5 g-4">
      <div v-for="item in searchResults" :key="item.id" class="card">
        <img :src="item.iimg" alt="Item Image" style="width: 100px" />
        <h3>{{ item.name }}</h3>
        <p class="price">${{ item.price }}</p>
        <p>{{ item.description }}</p>
        

      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  name: "SearcH",
  data() {
    return {
      searchResults: [],
    };
  },
  created() {
    this.fetchSearchResults();
  },
  methods: {
    async fetchSearchResults() {
      try {
        const searchQuery = this.$route.query.q;
        if (!searchQuery) {
          // Redirect or show error message if search query is missing
          return;
        }

        const response = await axios.post("/search", {
          search_query: searchQuery,
        });

        this.searchResults = response.data;
      } catch (error) {
        console.error("Axios error:", error);
      }
    },
    async addToCart(item_id) {
      try {
        const response = await axios.post(`/add_to_cart/${item_id}`);
        console.log(response.data.message); // Display success message
      } catch (error) {
        console.error("Axios error:", error);
      }
    },
  },
};
</script>

<style scoped>
.search-result {
  display: flex;
  align-items: center;
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
}

.item-details {
  margin-left: 20px;
}
</style>

  