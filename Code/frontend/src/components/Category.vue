<template>
  <div>
    <div class="card text-center">
      <div class="card-header">Featured</div>
      <img src="" class="card-img" alt="..." />
      <div class="card-body">
        <h5 class="card-title">All categories are shown in here</h5>
        <p class="card-text">
          By clicking the button ADD NEW CATEGORY admin is able to add new category.
          By clicking the button GET REPORT admin is able to download report.
        </p>
        <router-link to="/add-category" class="btn btn-primary">Add New category</router-link>
        <br>
        <!--<button @click="downloadPDF" class="btn btn-primary">GET REPORT</button>-->
      </div>
    </div>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="category in categories" :key="category.id" class="col">
        <div class="card">
          <img
            :src="category.image"
            class="card-img-top"
            alt="Category Image"
          />
          <div class="card-body">
            <h5 class="card-title">{{ category.name }}</h5>
            <p class="card-text">{{ category.description }}</p>
            <button @click="editCategory(category.id)">Edit</button>
            <button @click="deleteCategory(category.id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "@/axios";

export default {
  name: "CateGory",
  data() {
    return {
      categories: [],
    };
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get("/categories");
        this.categories = response.data;
      } catch (error) {
        console.error("Axios error:", error);
      }
    },

    async editCategory(categoryId) {
      this.$router.push(`/edit-category/${categoryId}`);
    },

    async deleteCategory(categoryId) {
      try {
        const response = await axios.delete(`/categories/${categoryId}`);
        if (response.status === 204) {
          this.fetchCategories();
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