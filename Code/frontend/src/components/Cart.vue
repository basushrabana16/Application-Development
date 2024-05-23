<template>
  <div>
    <div v-if="isLoading">
      <p>Loading cart items...</p>
    </div>
    <div v-else-if="cartItems.length === 0">
      <p>Your cart is empty.</p>
    </div>
    <div v-else>
      <div class="row row-cols-1 row-cols-md-5 g-4">
        <div v-for="(cartItem, index) in cartItems" :key="index" class="card">
          <img :src="cartItem.iimg" alt="Item Image" style="width: 100%" />
          <p>Item ID: {{ cartItem.item_id }}</p>
          <h1>{{ cartItem.item_name }}</h1>
          <p>Quantity: {{ cartItem.quantity }}</p>
          <p>Total Price: ${{ cartItem.total_price }}</p>
          <button @click="addToCart(cartItem.item_id, 1)">Add more</button>
          <button @click="removeFromCart(cartItem.item_id)">
            Remove from Cart
          </button>
        </div>
      </div>
      <p>Total Amount: ${{ totalAmount.toFixed(2) }}</p>
      <router-link to="/payment">
        <button>Proceed to Buy</button>
      </router-link>
    </div>
  </div>
</template>



<script>
import axios from "@/axios";

export default {
  name: "CartItem",
  data() {
    return {
      cartItems: [],
      isLoading: false, // Initialize isLoading to true
    };
  },
  computed: {
    totalAmount() {
      return this.cartItems.reduce(
        (total, cartItem) => total + parseFloat(cartItem.total_price),
        0
      );
    },
  },
  created() {
    this.fetchCartItems();
  },
  methods: {
    async fetchCartItems() {
      try {
        const response = await axios.get("/user-cart-items");
        this.cartItems = response.data;
      } catch (error) {
        console.error("Axios error:", error);
      }
    },


    async addToCart(item_id, quantityToAdd) {
      try {
        const response = await axios.post(`/add-to-cart/${item_id}`, {
          quantity: quantityToAdd,
        });
        console.log(response.data.message);
        this.updateCartItemQuantity(item_id, quantityToAdd);
      } catch (error) {
        console.error("Axios error:", error);
      }
    },

    updateCartItemQuantity(item_id, quantityToAdd) {
      const cartItem = this.cartItems.find((item) => item.item_id === item_id);
      if (cartItem) {
        cartItem.quantity += quantityToAdd;
        cartItem.total_price = (
          parseFloat(cartItem.total_price) +
          parseFloat(cartItem.item_price) * quantityToAdd
        ).toFixed(2);
      }
    },

    async removeFromCart(itemId) {
      try {
        const response = await axios.delete(`/remove-from-cart/${itemId}`);
        console.log(response.data.message);
        this.fetchCartItems();
      } catch (error) {
        console.error("Axios error:", error);
      }
    },
  },
};
</script>