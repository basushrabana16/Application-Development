<template>
    <div class="main-w3layouts wrapper">
      <h1>ADD NEW CATEGORY</h1>
      <div class="main-agileinfo">
        <div class="agileits-top">
          <form @submit.prevent="addCategory">
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
            <input type="submit" value="ADD CATEGORY" />
          </form>
        </div>
      </div>
      
    </div>
  </template>
  
<script>
import axios from "@/axios";

export default {
  name: "AddCategory",
  data() {
    return {
      name: "",
      description: "",
    };
  },
  methods: {
    async addCategory() {
      try {
        const data = {
          name: this.name,
          description: this.description,
        };
        const response = await axios.post("/add-category", data);
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
  