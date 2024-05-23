<template>
  <div class="main-w3layouts wrapper">
    <h1>ADD NEW ITEM</h1>
    <div class="main-agileinfo">
      <div class="agileits-top">
        <form @submit.prevent="addItem">
          <input
            class="text"
            v-model="name"
            type="text"
            name="name"
            placeholder="Item name"
            required=""
          />

          <input
            class="text email"
            v-model="description"
            type="text"
            name="description"
            placeholder="Item Description"
            required=""
          />

          <label for="manufacture_date">Manufacture Ddate</label>
          <input
            class="text"
            v-model="manufactureDate"
            type="date"
            name="manufacture_date"
            placeholder="Manufacture Date"
            required=""
          />
          <br>

          <label for="expiry_date">Expiry Date</label>
          <input
            class="text"
            v-model="expiryDate"
            type="date"
            name="expiry_date"
            placeholder="Expiry Date"
            required=""
          />
          <br>

          <label for="price">Price</label>
          <input
            class="text"
            v-model="price"
            type="number"
            name="price"
            placeholder="Price"
            required=""
          />
          <br>

          <label for="rate_per_unit">Rate Per Unit</label>
          <input
            class="text"
            v-model="ratePerUnit"
            type="number"
            name="rate_per_unit"
            placeholder="Rate per Unit"
            required=""
          />
          <br>

          <label for="tags">Tags</label>
          <input
            class="text"
            v-model="tags"
            type="text"
            name="tags"
            placeholder="Tags"
          />
          <br>

          <label for="iimg">Image</label>
          <input
            class="text"
            v-model="iimg"
            type="text"
            name="iimg"
            placeholder="Image URL"
          />
          <br>

          <label for="item_in_stock">item_in_stock</label>
          <input
            class="text"
            v-model="itemInStock"
            type="number"
            name="item_in_stock"
            placeholder="Items in Stock"
            required=""
          />
          <br>

          
          <select v-model="categoryId" name="category_id" required="">
            <option value="" disabled>Select Category</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>

          <div class="wthree-text">
            <div class="clear"></div>
          </div>
          <input type="submit" value="ADD ITEM" />
        </form>
      </div>
    </div>
  </div>
</template>



<script>
import axios from "@/axios";

export default {
  name: "AddItem",
  data() {
    return {
      name: "",
      description: "",
      manufactureDate: "",
      expiryDate: "",
      price: 0,
      ratePerUnit: 0,
      tags: "",
      iimg: "",
      itemInStock: 0,
      categoryId: "",
      categories: [],
    };
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    async addItem() {
      try {
        const data = {
          name: this.name,
          description: this.description,
          manufacture_date: new Date(this.manufactureDate)
            .toISOString()
            .split("T")[0],
          expiry_date: new Date(this.expiryDate).toISOString().split("T")[0],
          price: this.price,
          rate_per_unit: this.ratePerUnit,
          tags: this.tags,
          iimg: this.iimg,
          item_in_stock: this.itemInStock,
          category_id: this.categoryId,
        };
        const response = await axios.post("/add-item", data);
        console.log("Response data:", response.data);
        this.$router.push("/manager-item");
      } catch (error) {
        console.error("Axios error:", error);

        if (error.response) {
          console.log("Response data:", error.response.data);
        }
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get("/categories"); // Adjust the API endpoint
        this.categories = response.data;
      } catch (error) {
        console.error("Axios error:", error);
      }
    },
  },
};
</script>
