<script setup lang="ts">
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
</script>

<template>
  <div class="app">
    <!-- Navbar selalu tampil di semua halaman -->
    <Navbar title="Nutrisense"/>
    
    <!-- Router View - konten halaman berubah sesuai route -->
    <router-view />
    
    <!-- Footer selalu tampil di semua halaman -->
    <Footer />
  </div>
</template>

<style scoped></style>
