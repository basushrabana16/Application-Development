<template>
  <div class="row">
    <div class="col-sm-6 mb-3 mb-sm-0">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Click to manage categories</h5>
          <p class="card-text">
            Admin can add new categories, update existing categories and delete categories.
          </p>
          <router-link to="/category" class="btn btn-primary">Manage categories</router-link>
        </div>
      </div>
    </div>
    <div class="col-sm-6">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Click to manage users</h5>
          <p class="card-text">
            Admin can remove existing users.
          </p>
          <router-link to="/all-user" class="btn btn-primary">Manage users</router-link>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
export default {
  name: "AdminDashboard",

};
</script>
  
  <style>

</style>
  