<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

// API Base URL
const API_BASE_URL = 'http://localhost:5000'

// Reactive state
const isLogin = ref(true)
const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const needsEmailConfirmation = ref(false)
const lastRegisteredEmail = ref('')

// Form data
const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  rememberMe: false
})

// Validation computed properties
const emailValidation = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email) return { isValid: true, message: '' }
  return {
    isValid: emailRegex.test(form.email),
    message: emailRegex.test(form.email) ? '' : 'Email format is invalid'
  }
})

const passwordValidation = computed(() => {
  const password = form.password
  if (!password) return { isValid: true, message: '', strength: 0 }
  
  const minLength = password.length >= 8
  const maxLength = password.length <= 30
  const hasUpperCase = /[A-Z]/.test(password)
  const hasLowerCase = /[a-z]/.test(password)
  const hasNumbers = /\d/.test(password)
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password)
  
  const requirements = [
    { met: minLength, text: 'At least 8 characters' },
    { met: maxLength, text: 'Maximum 30 characters' },
    { met: hasUpperCase, text: 'One uppercase letter' },
    { met: hasLowerCase, text: 'One lowercase letter' },
    { met: hasNumbers, text: 'One number' },
    { met: hasSpecialChar, text: 'One special character' }
  ]
  
  const metRequirements = requirements.filter(req => req.met).length
  const isValid = minLength && maxLength && hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChar
  
  return {
    isValid,
    requirements,
    strength: (metRequirements / requirements.length) * 100,
    message: isValid ? 'Strong password' : 'Password must meet all requirements'
  }
})

const confirmPasswordValidation = computed(() => {
  if (!form.confirmPassword) return { isValid: true, message: '' }
  return {
    isValid: form.password === form.confirmPassword,
    message: form.password === form.confirmPassword ? '' : 'Passwords do not match'
  }
})

const isFormValid = computed(() => {
  if (isLogin.value) {
    return emailValidation.value.isValid && passwordValidation.value.isValid && form.email && form.password
  } else {
    return (
      emailValidation.value.isValid &&
      passwordValidation.value.isValid &&
      confirmPasswordValidation.value.isValid &&
      form.name &&
      form.email &&
      form.password &&
      form.confirmPassword
    )
  }
})

// Methods
const toggleAuthMode = () => {
  isLogin.value = !isLogin.value
  clearMessages()
  // Reset form when switching modes
  Object.assign(form, {
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    rememberMe: false
  })
}

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const clearMessages = () => {
  errorMessage.value = ''
  successMessage.value = ''
  needsEmailConfirmation.value = false
}

const resendConfirmation = async () => {
  if (!lastRegisteredEmail.value) return
  
  isLoading.value = true
  clearMessages()
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/resend-confirmation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: lastRegisteredEmail.value })
    })

    const data = await response.json()

    if (response.ok) {
      successMessage.value = 'Confirmation email sent! Please check your inbox.'
    } else {
      errorMessage.value = data.error || 'Failed to send confirmation email'
    }
  } catch (error) {
    errorMessage.value = 'Network error. Please try again.'
    console.error('Resend confirmation error:', error)
  } finally {
    isLoading.value = false
  }
}

const confirmEmailManual = async () => {
  if (!lastRegisteredEmail.value) return
  
  isLoading.value = true
  clearMessages()
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/confirm-email-manual`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: lastRegisteredEmail.value })
    })

    const data = await response.json()

    if (response.ok) {
      successMessage.value = 'Email confirmed! You can now login. ' + (data.warning || '')
      needsEmailConfirmation.value = false
      setTimeout(() => {
        clearMessages()
      }, 3000)
    } else {
      errorMessage.value = data.error || 'Failed to confirm email'
    }
  } catch (error) {
    errorMessage.value = 'Network error. Please try again.'
    console.error('Manual confirmation error:', error)
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!isFormValid.value) {
    errorMessage.value = 'Please fix all validation errors before submitting'
    return
  }

  isLoading.value = true
  clearMessages()

  try {
    const endpoint = isLogin.value ? '/auth/login' : '/auth/signup'
    const payload = isLogin.value 
      ? { email: form.email, password: form.password }
      : { name: form.name, email: form.email, password: form.password }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    })

    const data = await response.json()

    if (response.ok) {
      successMessage.value = data.message
      if (isLogin.value) {
        // Store user session/token if needed
        if (data.session?.access_token) {
          localStorage.setItem('access_token', data.session.access_token)
        }
        // Redirect to dashboard or home
        setTimeout(() => {
          window.location.href = '/'
        }, 1500)
      } else {
        // Show success message for registration
        lastRegisteredEmail.value = form.email
        setTimeout(() => {
          isLogin.value = true
          clearMessages()
        }, 2000)
      }
    } else {
      // Handle specific error messages
      if (data.error && data.error.includes('Please confirm your email address')) {
        needsEmailConfirmation.value = true
        lastRegisteredEmail.value = form.email
        errorMessage.value = data.error + ' Click below to resend confirmation email.'
      } else if (data.error && (data.error.includes('Email signup') || data.error.includes('Email logins are disabled') || data.error.includes('signup_disabled'))) {
        errorMessage.value = 'Email authentication is disabled. Please enable it in Supabase Dashboard → Authentication → Providers → Enable Email Provider and Allow new signups.'
      } else {
        errorMessage.value = data.error || 'An error occurred'
      }
    }
  } catch (error) {
    errorMessage.value = 'Network error. Please check if backend is running on port 5000.'
    console.error('Auth error:', error)
  } finally {
    isLoading.value = false
  }
}

const loginWithGoogle = () => {
  // TODO: Implement Google OAuth
  console.log('Login with Google')
  errorMessage.value = 'Google OAuth integration coming soon!'
}

const loginWithGithub = () => {
  // TODO: Implement GitHub OAuth
  console.log('Login with GitHub')
  errorMessage.value = 'GitHub OAuth integration coming soon!'
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl w-full grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16">
      
      <!-- Left Side - Image (Hidden on mobile) -->
      <div class="hidden lg:flex items-center justify-center">
        <div class="relative">
          <img 
            src="../assets/being-health.png" 
            alt="Health Illustration" 
            class="w-full max-w-lg h-auto transform hover:scale-105 transition-transform duration-300"
          />
          
        </div>
      </div>

      <!-- Right Side - Auth Form -->
      <div class="flex items-center justify-center">
        <div class="w-full max-w-md space-y-8">
          
          <!-- Header -->
          <div class="text-center">
            <h2 class="text-3xl lg:text-4xl font-bold text-gray-900 mb-2">
              {{ isLogin ? 'Welcome Back!' : 'Join Nutrisense' }}
            </h2>
            <p class="text-gray-600">
              {{ isLogin ? 'Sign in to your account' : 'Create your account to get started' }}
            </p>
          </div>

          <!-- Error/Success Messages -->
          <div v-if="errorMessage" class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded-lg">
            {{ errorMessage }}
            <div v-if="needsEmailConfirmation" class="mt-3 space-y-2">
              <button 
                @click="resendConfirmation"
                :disabled="isLoading"
                class="inline-flex items-center px-3 py-1 mr-2 border border-transparent text-sm font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 disabled:opacity-50"
              >
                <svg v-if="isLoading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-red-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ isLoading ? 'Sending...' : 'Resend Email' }}
              </button>
              <button 
                @click="confirmEmailManual"
                :disabled="isLoading"
                class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:opacity-50"
              >
                <svg v-if="isLoading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ isLoading ? 'Confirming...' : 'Skip Email (Dev Mode)' }}
              </button>
              <div class="text-xs text-red-600 mt-1">
                Or disable "Enable email confirmations" in Supabase Auth settings for development
              </div>
            </div>
          </div>
          <div v-if="successMessage" class="bg-green-50 border border-green-300 text-green-700 px-4 py-3 rounded-lg">
            {{ successMessage }}
          </div>

          <!-- Social Login Buttons -->
          <div class="space-y-3">
            <button 
              class="w-full flex items-center justify-center px-4 py-3 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 transform hover:scale-105"
              @click="loginWithGoogle"
            >
              <svg class="w-5 h-5 mr-3" viewBox="0 0 24 24">
                <path fill="#4285f4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34a853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#fbbc05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#ea4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Continue with Google
            </button>

            <button 
              class="w-full flex items-center justify-center px-4 py-3 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 transform hover:scale-105"
              @click="loginWithGithub"
            >
              <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              Continue with GitHub
            </button>
          </div>

          <!-- Divider -->
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-gradient-to-br from-green-50 to-blue-50 text-gray-500">Or continue with email</span>
            </div>
          </div>

          <!-- Auth Form -->
          <form class="space-y-6" @submit.prevent="handleSubmit">
            <!-- Name Field (Only for Register) -->
            <div v-if="!isLogin" class="transform transition-all duration-300">
              <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input
                id="name"
                name="name"
                type="text"
                required
                v-model="form.name"
                class="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm transition-all duration-200"
                placeholder="Enter your full name"
              />
            </div>

            <!-- Email Field -->
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
              <input
                id="email"
                name="email"
                type="email"
                required
                v-model="form.email"
                :class="[
                  'appearance-none relative block w-full px-3 py-3 border placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:z-10 sm:text-sm transition-all duration-200',
                  emailValidation.isValid ? 'border-gray-300 focus:ring-green-500 focus:border-green-500' : 'border-red-300 focus:ring-red-500 focus:border-red-500'
                ]"
                placeholder="Enter your email"
              />
              <p v-if="!emailValidation.isValid && form.email" class="mt-1 text-sm text-red-600">
                {{ emailValidation.message }}
              </p>
            </div>

            <!-- Password Field -->
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <div class="relative">
                <input
                  id="password"
                  name="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  v-model="form.password"
                  :class="[
                    'appearance-none relative block w-full px-3 py-3 pr-10 border placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:z-10 sm:text-sm transition-all duration-200',
                    passwordValidation.isValid || !form.password ? 'border-gray-300 focus:ring-green-500 focus:border-green-500' : 'border-red-300 focus:ring-red-500 focus:border-red-500'
                  ]"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center"
                  @click="togglePassword"
                >
                  <svg v-if="!showPassword" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                  </svg>
                </button>
              </div>
              
              <!-- Password Strength Indicator -->
              <div v-if="form.password && !isLogin" class="mt-2">
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600">Password Strength</span>
                  <span :class="passwordValidation.strength >= 100 ? 'text-green-600' : passwordValidation.strength >= 60 ? 'text-yellow-600' : 'text-red-600'">
                    {{ passwordValidation.strength >= 100 ? 'Strong' : passwordValidation.strength >= 60 ? 'Medium' : 'Weak' }}
                  </span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    :class="[
                      'h-2 rounded-full transition-all duration-300',
                      passwordValidation.strength >= 100 ? 'bg-green-500' : passwordValidation.strength >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                    ]"
                    :style="{ width: passwordValidation.strength + '%' }"
                  ></div>
                </div>
                <ul class="mt-2 text-xs space-y-1">
                  <li v-for="req in passwordValidation.requirements" :key="req.text" 
                      :class="req.met ? 'text-green-600' : 'text-red-600'">
                    <span :class="req.met ? 'text-green-500' : 'text-red-500'">{{ req.met ? '✓' : '✗' }}</span>
                    {{ req.text }}
                  </li>
                </ul>
              </div>
            </div>

            <!-- Confirm Password (Only for Register) -->
            <div v-if="!isLogin" class="transform transition-all duration-300">
              <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                v-model="form.confirmPassword"
                :class="[
                  'appearance-none relative block w-full px-3 py-3 border placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:z-10 sm:text-sm transition-all duration-200',
                  confirmPasswordValidation.isValid || !form.confirmPassword ? 'border-gray-300 focus:ring-green-500 focus:border-green-500' : 'border-red-300 focus:ring-red-500 focus:border-red-500'
                ]"
                placeholder="Confirm your password"
              />
              <p v-if="!confirmPasswordValidation.isValid && form.confirmPassword" class="mt-1 text-sm text-red-600">
                {{ confirmPasswordValidation.message }}
              </p>
            </div>

            <!-- Remember Me & Forgot Password -->
            <div v-if="isLogin" class="flex items-center justify-between">
              <div class="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  v-model="form.rememberMe"
                  class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label for="remember-me" class="ml-2 block text-sm text-gray-900">Remember me</label>
              </div>
              <div class="text-sm">
                <a href="#" class="font-medium text-green-600 hover:text-green-500 transition-colors duration-200">
                  Forgot your password?
                </a>
              </div>
            </div>

            <!-- Submit Button -->
            <div>
              <button
                type="submit"
                :disabled="!isFormValid || isLoading"
                :class="[
                  'group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-200 transform hover:shadow-lg',
                  isFormValid && !isLoading 
                    ? 'bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 hover:scale-105' 
                    : 'bg-gray-400 cursor-not-allowed'
                ]"
              >
                <span v-if="isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
                  <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
                {{ isLoading ? 'Processing...' : (isLogin ? 'Sign In' : 'Create Account') }}
              </button>
            </div>

            <!-- Toggle Auth Mode -->
            <div class="text-center">
              <p class="text-sm text-gray-600">
                {{ isLogin ? "Don't have an account?" : 'Already have an account?' }}
                <button
                  type="button"
                  @click="toggleAuthMode"
                  class="font-medium text-green-600 hover:text-green-500 transition-colors duration-200 ml-1"
                >
                  {{ isLogin ? 'Sign up' : 'Sign in' }}
                </button>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Additional custom animations */
.transform {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover\:scale-105:hover {
  transform: scale(1.05);
}

.hover\:shadow-lg:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style>