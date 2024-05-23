<template>
    <div>
      <table class="table table-success table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>User Type</th>
            <th>Action</th>
            <!-- Add more table headers as needed -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.userType }}</td>
            <td><button @click="removeUser(user.id)" class="btn btn-danger">Remove</button></td>
            <!-- Display additional user attributes as needed -->
          </tr>
        </tbody>
      </table>
    </div>
  </template>

<script>
import axios from "@/axios";

export default {
  name: "AllUser",
  data() {
    return {
      users: [],
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get("/all-user"); // Adjust the API endpoint
        this.users = response.data;
      } catch (error) {
        console.error("Axios error:", error);
      }
    },

    async removeUser(userId) {
      try {
        const response = await axios.delete(`/all-user/${userId}`);
        if (response.status === 204) {
          this.fetchUsers();
        }
      } catch (error) {
        console.error("Axios error:", error);
      }
    },
  },
};
</script>

<style>
</style>