<template>
  <div class="main-w3layouts wrapper">
    <h1>LOGIN!</h1>
    <div class="main-agileinfo">
      <div class="agileits-top">
        <form @submit.prevent="login">
          <select v-model="userType">
            <option value="admin">Admin</option>
            <option value="user">User</option>
            <option value="manager">Manager</option>
          </select>

          <input
            class="text"
            v-model="email"
            type="text"
            name="email"
            placeholder="Email"
            required=""
          />

          <input
            class="text"
            v-model="password"
            type="password"
            name="password"
            placeholder="Password"
            required=""
          />
          <div class="wthree-text">
            <div class="clear"></div>
          </div>
          <input type="submit" value="LOGIN" />
        </form>
        <p>
          Don't have an Account?
          <router-link to="/register"> Register Now!</router-link>
        </p>
      </div>
    </div>
  </div>
</template>


<script>
import instance from '@/axios';

export default {
  name: "LogIn",
  data() {
    return {
      userType: "",
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        await instance.post("/login", {
          userType: this.userType,
          email: this.email,
          password: this.password,
        });

        // Redirect the user to the appropriate dashboard page based on userType
        if (this.userType === "admin") {
          this.$router.push("/admin-dashboard");
        } else if (this.userType === "manager") {
          this.$router.push("/manager-dashboard");
        } else if (this.userType === "user") {
          this.$router.push("/user-dashboard");
        }
      } catch (error) {
        console.error("Axios error:", error);

        if (error.response) {
          console.log("Login error response:", error.response.data);
          if (error.response.status === 401) {
            this.errorMessage = "Invalid credentials. Please try again.";
          } else {
            this.errorMessage = "An error occurred. Please try again later.";
          }
        } else {
          this.errorMessage = "Network error. Please check your connection.";
        }
      }
    },
  },
};
</script>
