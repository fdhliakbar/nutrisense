<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';

// Variables untuk event listeners
let mouseMoveHandler: ((e: MouseEvent) => void) | null = null;

onMounted(() => {
  // Update copyright year dengan Vue reactive way
  const yearElement = document.getElementById('year');
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear().toString();
  }

  // Mouse follow orb effect
  mouseMoveHandler = (e: MouseEvent) => {
    const orb = document.querySelector('.orb') as HTMLElement;
    if (orb) {
      orb.style.left = `${e.clientX}px`;
      orb.style.top = `${e.clientY}px`;
    }
  };

  document.addEventListener('mousemove', mouseMoveHandler);
});

// Cleanup event listeners
onUnmounted(() => {
  if (mouseMoveHandler) {
    document.removeEventListener('mousemove', mouseMoveHandler);
  }
});

// Current year reactive
const currentYear = new Date().getFullYear();

// Newsletter submit handler
function handleNewsletterSubmit() {
  alert('Thank you for subscribing!');
}
</script>

<template>
  <footer class="relative bg-gradient-to-br from-white to-green-50 text-gray-800 overflow-hidden">
    <!-- Animated background elements -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden opacity-10">
      <div class="absolute top-20 left-10 w-32 h-32 bg-green-400 rounded-full filter blur-3xl animate-float1"></div>
      <div class="absolute top-40 right-20 w-40 h-40 bg-green-500 rounded-full filter blur-3xl animate-float2"></div>
      <div class="absolute bottom-10 left-1/2 w-48 h-48 bg-green-300 rounded-full filter blur-3xl animate-float3"></div>
    </div>

    <!-- Main footer content -->
    <div class="relative max-w-7xl mx-auto px-6 py-16 sm:py-20 lg:px-8">
      <!-- Grid layout -->
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-12">
        
        <!-- Logo/Brand section - Updated untuk Nutrisense -->
        <div class="group">
          <div class="flex items-center space-x-2 mb-6">
            <div class="w-10 h-10 rounded-lg flex items-center justify-center transform group-hover:rotate-12 transition duration-500">
              <img src="../assets/leap_website.png" alt="Website Logo" class="h-8 w-8">
            </div>
            <h2 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-600 to-green-800">
              Nutrisense
            </h2>
          </div>
          <p class="text-gray-600 mb-6">Smart nutrition recommendations for a healthier lifestyle.</p>
          
          <!-- Social media with hover glow -->
          <div class="flex space-x-4">
            <a href="https://github.com/fdhliakbar/nutrisense" class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center hover:bg-black hover:text-white hover:shadow-lg hover:shadow-green-500/30 transition-all duration-300" aria-label="GitHub">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>
            <a href="#" class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center hover:bg-red-500 hover:text-white hover:shadow-lg hover:shadow-red-500/30 transition-all duration-300" aria-label="YouTube">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/>
              </svg>
            </a>
            <a href="#" class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center hover:bg-blue-600 hover:text-white hover:shadow-lg hover:shadow-blue-600/30 transition-all duration-300" aria-label="LinkedIn">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- Quick links dengan grup class untuk hover effect -->
        <div class="group">
          <h3 class="text-lg font-semibold mb-6 relative text-gray-800">
            <span class="relative z-10">Quick Links</span>
            <span class="absolute bottom-0 left-0 w-full h-1 bg-green-500 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-300"></span>
          </h3>
          <ul class="space-y-3">
            <li class="link-item">
              <a href="#home" class="text-gray-600 hover:text-green-600 hover:pl-2 transition-all duration-300 flex items-center">
                <span class="w-1 h-1 bg-green-500 rounded-full mr-2 opacity-0 hover:opacity-100 transition duration-300"></span>
                Home
              </a>
            </li>
            <li class="link-item">
              <a href="#nutrition" class="text-gray-600 hover:text-green-600 hover:pl-2 transition-all duration-300 flex items-center">
                <span class="w-1 h-1 bg-green-500 rounded-full mr-2 opacity-0 hover:opacity-100 transition duration-300"></span>
                Nutrition Guide
              </a>
            </li>
            <li class="link-item">
              <a href="#recipes" class="text-gray-600 hover:text-green-600 hover:pl-2 transition-all duration-300 flex items-center">
                <span class="w-1 h-1 bg-green-500 rounded-full mr-2 opacity-0 hover:opacity-100 transition duration-300"></span>
                Recipes
              </a>
            </li>
            <li class="link-item">
              <a href="#about" class="text-gray-600 hover:text-green-600 hover:pl-2 transition-all duration-300 flex items-center">
                <span class="w-1 h-1 bg-green-500 rounded-full mr-2 opacity-0 hover:opacity-100 transition duration-300"></span>
                Article
              </a>
            </li>
          </ul>
        </div>

        <!-- Contact info dengan animated icons -->
        <div>
          <h3 class="text-lg font-semibold mb-6 text-gray-800">Get in Touch</h3>
          <ul class="space-y-4">
            <li class="flex items-start">
              <div class="flex-shrink-0 mt-1">
                <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center animate-pulse">
                  <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                  </svg>
                </div>
              </div>
              <div class="ml-3">
                <p class="text-sm text-gray-600">Email</p>
                <a href="mailto:fadhliakbar125@gmail.com" class="text-gray-800 hover:text-green-600 transition">
                  fadhliakbar125@gmail.com
                </a>
              </div>
            </li>
            
          </ul>
        </div>

        <!-- Newsletter section -->
        <div>
          <h3 class="text-lg font-semibold mb-6 text-gray-800">Stay Updated</h3>
          <p class="text-gray-600 mb-4">Get nutrition tips and healthy recipes delivered to your inbox.</p>
          <form class="mt-4" @submit.prevent="handleNewsletterSubmit">
            <div class="relative">
              <input 
                type="email" 
                placeholder="Your email" 
                class="w-full bg-white border border-gray-300 rounded-lg py-3 px-4 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent placeholder-gray-400 text-gray-800"
                required
              >
              <button 
                type="submit" 
                class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-green-500 hover:bg-green-600 text-white rounded-lg px-4 py-1 transition"
                aria-label="Subscribe to newsletter"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                </svg>
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Bottom section -->
      <div class="mt-16 pt-8 border-t border-gray-300 flex flex-col md:flex-row justify-between items-center">
        <p class="text-gray-600 text-sm mb-4 md:mb-0">
          &copy; <span class="text-green-600">{{ currentYear }}</span> Nutrisense. All rights reserved.
        </p>
        <div class="flex space-x-6">
          <a href="#privacy" class="text-gray-600 hover:text-green-600 transition">Privacy Policy</a>
          <a href="#terms" class="text-gray-600 hover:text-green-600 transition">Terms of Service</a>
          <a href="#cookies" class="text-gray-600 hover:text-green-600 transition">Cookies</a>
        </div>
      </div>
    </div>

    <!-- Floating orb that follows cursor -->
    <div class="orb absolute w-64 h-64 rounded-full bg-gradient-to-r from-green-300/10 to-green-500/10 filter blur-3xl pointer-events-none"></div>
  </footer>
</template>

<style scoped>
/* Animations */
@keyframes float1 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(20px, 20px); }
}

@keyframes float2 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-15px, 15px); }
}

@keyframes float3 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(0, -20px); }
}

.animate-float1 { 
  animation: float1 8s ease-in-out infinite; 
}

.animate-float2 { 
  animation: float2 10s ease-in-out infinite; 
}

.animate-float3 { 
  animation: float3 12s ease-in-out infinite; 
}

/* Orb follow effect */
.orb {
  transform: translate(-50%, -50%);
  opacity: 0.3;
  transition: transform 0.1s ease-out;
}

/* Link hover effects */
.link-item:hover span {
  opacity: 1;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}
</style>