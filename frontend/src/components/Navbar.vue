<script setup lang="ts">
import { ref } from 'vue';

interface NavbarProps {
  title: string;
}

const props = withDefaults(defineProps<NavbarProps>(), {
  title: 'Nutrisense'
});

const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};
</script>

<template>
  <div>
    <nav class="bg-white border-gray-200 py-2.5 shadow-sm">
      <div class="flex flex-wrap items-center justify-between max-w-screen-xl px-4 mx-auto">
        <RouterLink to="/" class="flex items-center">
          <img src="../assets/leap_website.png" alt="Website Logo" class="h-8 mr-3" />
          <span
            class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-500 to-green-600">Nutrisense</span>
        </RouterLink>
        <div class="flex items-center lg:order-2">
          <RouterLink to="/auth"
            class="inline-flex items-center px-4 py-2 ml-1 text-sm font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 transition-colors duration-200">
            Login
          </RouterLink>
          
          <!-- Mobile menu button -->
          <button @click="toggleMobileMenu" type="button"
            class="inline-flex items-center p-2 ml-1 text-sm text-gray-500 rounded-lg lg:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200"
            aria-controls="mobile-menu-2" :aria-expanded="isMobileMenuOpen">
            <span class="sr-only">Open main menu</span>
            <svg class="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>
        <div
          :class="['items-center justify-between w-full lg:flex lg:w-auto lg:order-1', { 'hidden': !isMobileMenuOpen }]"
          id="mobile-menu-2">
          <ul class="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-8 lg:mt-0">
            <li>
              <a href="#"
                class="block py-2 pl-3 pr-4 text-white bg-green-500 rounded lg:bg-transparent lg:text-green-600 lg:p-0"
                aria-current="page">Home</a>
            </li>

            <li>
              <a href="#"
                class="block py-2 pl-3 pr-4 text-gray-700 border-b border-gray-100 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-green-600 lg:p-0">Nutrition
                Guide</a>
            </li>
            <li>
              <a href="#"
                class="block py-2 pl-3 pr-4 text-gray-700 border-b border-gray-100 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-green-600 lg:p-0">Recipes</a>
            </li>
            <li>
              <a href="#"
                class="block py-2 pl-3 pr-4 text-gray-700 border-b border-gray-100 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-green-600 lg:p-0">Article</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<style scoped></style>