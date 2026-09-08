<template>
  <div class="min-h-screen bg-slate-50 font-sans text-slate-900 flex flex-col">
    <!-- Enterprise Navbar -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-4 lg:gap-8 flex-1 min-w-0">
            <NuxtLink to="/" class="flex items-center gap-2 text-indigo-700 font-bold text-lg lg:text-xl tracking-tight min-w-0">
              <svg class="w-7 h-7 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
              <span class="truncate block">Insight Hub</span>
            </NuxtLink>
            <nav class="hidden md:flex space-x-1 flex-shrink-0">
              <NuxtLink to="/" class="px-3 lg:px-4 py-2 rounded-md text-sm font-medium text-slate-600 hover:text-indigo-600 hover:bg-indigo-50 transition" active-class="text-indigo-700 bg-indigo-50">แจ้งปัญหา</NuxtLink>
              <NuxtLink to="/dashboard" class="px-3 lg:px-4 py-2 rounded-md text-sm font-medium text-slate-600 hover:text-indigo-600 hover:bg-indigo-50 transition" active-class="text-indigo-700 bg-indigo-50">แดชบอร์ดสรุปผล</NuxtLink>
            </nav>
          </div>
          <!-- <div class="flex items-center gap-4">
            <div class="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold text-sm">
              AD
            </div>
          </div> -->
        </div>
      </div>
    </header>
    
    <main class="flex-grow pb-16 md:pb-0">
      <NuxtPage />
    </main>
    
    <!-- Mobile Bottom Navigation -->
    <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 flex justify-around items-center h-16 z-50">
      <NuxtLink to="/" class="flex flex-col items-center justify-center w-full h-full text-slate-500 hover:text-indigo-600 transition" active-class="text-indigo-700 bg-indigo-50">
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
        <span class="text-[10px] font-medium">แจ้งปัญหา</span>
      </NuxtLink>
      <NuxtLink to="/dashboard" class="flex flex-col items-center justify-center w-full h-full text-slate-500 hover:text-indigo-600 transition border-l border-slate-100" active-class="text-indigo-700 bg-indigo-50">
        <svg class="w-6 h-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
        <span class="text-[10px] font-medium">แดชบอร์ด</span>
      </NuxtLink>
    </nav>
    
    <footer class="hidden md:block bg-white border-t border-slate-200 mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-sm text-slate-500">
        &copy; 2026 Insight Hub. All rights reserved for <a href="https://github.com/thayorch" target="_blank" class="hover:text-indigo-800 hover:underline transition">thayorch</a>
      </div>
    </footer>
  </div>
</template>

<style>
/* Add base Leaflet styles globally if needed */
@import 'leaflet/dist/leaflet.css';
</style>
