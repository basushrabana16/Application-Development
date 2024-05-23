<template>
  <div class="main-w3layouts wrapper">
    <h1>EDIT ITEM</h1>
    <div class="main-agileinfo">
      <div class="agileits-top">
        <form @submit.prevent="editItem">
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

          <input
            class="text"
            v-model="manufactureDate"
            type="date"
            name="manufacture_date"
            placeholder="Manufacture Date"
            required=""
          />

          <input
            class="text"
            v-model="expiryDate"
            type="date"
            name="expiry_date"
            placeholder="Expiry Date"
            required=""
          />

          <input
            class="text"
            v-model="price"
            type="number"
            name="price"
            placeholder="Price"
            required=""
          />

          <input
            class="text"
            v-model="ratePerUnit"
            type="number"
            name="rate_per_unit"
            placeholder="Rate per Unit"
            required=""
          />

          <input
            class="text"
            v-model="tags"
            type="text"
            name="tags"
            placeholder="Tags"
          />

          <input
            class="text"
            v-model="iimg"
            type="text"
            name="iimg"
            placeholder="Image URL"
          />

          <input
            class="text"
            v-model="itemInStock"
            type="number"
            name="item_in_stock"
            placeholder="Items in Stock"
            required=""
          />

          <div class="wthree-text">
            <div class="clear"></div>
          </div>
          <input type="submit" value="UPDATE ITEM" />
        </form>
      </div>
    </div>
  </div>
</template>
    
    <script>
import axios from "@/axios";

export default {
  name: "EditItem",
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
    this.fetchItemDetails();
  },
  methods: {
    async fetchItemDetails() {
      try {
        const itemId = this.$route.params.id;
        const response = await axios.get(`/items/${itemId}`);

        this.name = response.data.name;
        this.description = response.data.description;
        this.manufactureDate = new Date(response.data.manufacture_date).toISOString().substring(0, 10);
        this.expiryDate = new Date(response.data.expiry_date).toISOString().substring(0, 10);
        this.price = response.data.price;
        this.ratePerUnit = response.data.rate_per_unit;
        this.tags = response.data.tags;
        this.iimg = response.data.iimg;
        this.itemInStock = response.data.item_in_stock;
        this.categoryId = response.data.category_id;
      } catch (error) {
        console.error("Axios error:", error);
      }
    },
    async editItem() {
      try {
        const itemId = this.$route.params.id;
        const data = {
          name: this.name,
          description: this.description,
          manufacture_date: this.manufactureDate,
          expiry_date: this.expiryDate,
          price: this.price,
          rate_per_unit: parseFloat(this.ratePerUnit), // Convert to number
          tags: this.tags,
          iimg: this.iimg,
          item_in_stock: this.itemInStock,
          category_id: this.categoryId,
        };
        const response = await axios.put(`/items/${itemId}`, data, {
          headers: {
            "Content-Type": "application/json", // Set the correct content type
          },
        });
        console.log("Response data:", response.data);
        this.$router.push("/manager-item");
      } catch (error) {
        console.error("Axios error:", error);

        if (error.response) {
          console.log("Response data:", error.response.data);
        }
      }
    },
    async deleteItem() {
      try {
        const itemId = this.$route.params.id;
        const response = await axios.delete(`/items/${itemId}`);
        console.log("Response data:", response.data);
        this.$router.push("/manager-item");
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
    