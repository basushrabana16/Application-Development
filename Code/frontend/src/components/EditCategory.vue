<template>
  <div class="main-w3layouts wrapper">
    <h1>EDIT CATEGORY</h1>
    <div class="main-agileinfo">
      <div class="agileits-top">
        <form @submit.prevent="editCategory">
          <input
            class="text"
            v-model="name"
            type="text"
            name="name"
            placeholder="Category name"
            required=""
          />

          <input
            class="text email"
            v-model="description"
            type="text"
            name="description"
            placeholder="Category Description"
            required=""
          />
          <div class="wthree-text">
            <div class="clear"></div>
          </div>
          <input type="submit" value="UPDATE CATEGORY" />
        </form>
      </div>
    </div>
  </div>
</template>
  
  <script>
import axios from "@/axios";

export default {
  name: "EditCategory",
  data() {
    return {
      name: "",
      description: "",
    };
  },
  created() {
    this.fetchCategoryDetails();
  },
  methods: {
    async fetchCategoryDetails() {
      try {
        const categoryId = this.$route.params.id;
        const response = await axios.get(`/categories/${categoryId}`);
        this.name = response.data.name;
        this.description = response.data.description;
      } catch (error) {
        console.error("Axios error:", error);
      }
    },
    async editCategory() {
      try {
        const categoryId = this.$route.params.id;
        const data = {
          name: this.name,
          description: this.description,
        };
        const response = await axios.put(`/categories/${categoryId}`, data, {
          headers: {
            "Content-Type": "application/json", // Set the correct content type
          },
        });
        console.log("Response data:", response.data);
        this.$router.push("/category");
      } catch (error) {
        console.error("Axios error:", error);

        if (error.response) {
          console.log("Response data:", error.response.data);
        }
      }
    },
    async deleteCategory() {
      try {
        const categoryId = this.$route.params.id;
        const response = await axios.delete(`/categories/${categoryId}`);
        console.log("Response data:", response.data);
        this.$router.push("/category");
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
  