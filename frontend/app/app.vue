<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-indigo-600 text-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex-shrink-0 font-bold text-xl">
            CMU Area Management
          </div>
          <div class="flex space-x-4">
            <NuxtLink to="/" class="px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-500" active-class="bg-indigo-700">Report Issue</NuxtLink>
            <NuxtLink to="/dashboard" class="px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-500" active-class="bg-indigo-700">Dashboard</NuxtLink>
          </div>
        </div>
      </div>
    </nav>
    <main class="py-6">
      <NuxtPage />
    </main>
  </div>
</template>

<style>
/* Add base Leaflet styles globally if needed */
@import 'leaflet/dist/leaflet.css';
</style>
