<template>
  <div class="card text-center">
    <div class="card-header">Latest items</div>
    <img src="" class="card-img" alt="..." />
    <div class="card-body">
      <h5 class="card-title">Find your grocery</h5>
      <p class="card-text">
        By clicking on the button below an user is able to see all the items available.
      </p>
      <router-link to="/user-item" class="btn btn-primary">See all items</router-link>
    </div>
  </div>
</template>
  
<script>
  export default {
    name: "UserDashboard",
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  