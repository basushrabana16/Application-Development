<template>
  <div id="app">
    <Navbar />
    
    <div class="auth-wrapper">
      <div class="auth-inner">
        <router-view/>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    Navbar,
    Footer,
  },
};
</script>

<style>
</style>
