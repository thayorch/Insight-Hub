<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <div class="mb-8">
      <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">แจ้งเหตุด่วน / ร้องเรียนปัญหา</h1>
      <p class="mt-2 text-sm text-slate-500">กรุณาระบุรายละเอียดของปัญหาเพื่อให้ AI ประเมินความเสี่ยงและส่งเรื่องไปยังหน่วยงานที่เกี่ยวข้อง</p>
    </div>
    
    <div class="bg-white shadow-sm ring-1 ring-slate-200 rounded-xl overflow-hidden">
      <form @submit.prevent="submitIssue" class="divide-y divide-slate-200">
        
        <!-- Section 1 -->
        <div class="p-6 sm:p-8">
          <h2 class="text-lg font-medium text-slate-900 mb-4">1. ข้อมูลปัญหา</h2>
          <div class="space-y-5">
            <div>
              <label for="issue" class="block text-sm font-medium text-slate-700 mb-1">หัวข้อปัญหา (ประเด็น)</label>
              <input 
                type="text" 
                id="issue" 
                v-model="form.issue" 
                required
                class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border"
                placeholder="เช่น น้ำรั่วในห้องน้ำ, คนแปลกหน้าในพื้นที่..."
              />
            </div>
            <div>
              <label for="details" class="block text-sm font-medium text-slate-700 mb-1">รายละเอียดเพิ่มเติม</label>
              <textarea 
                id="details" 
                v-model="form.details" 
                rows="4" 
                required
                class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border"
                placeholder="ระบุข้อมูลบริบทที่เกี่ยวข้อง หรือความรุนแรงของสถานการณ์..."
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Section 2 -->
        <div class="p-6 sm:p-8 bg-slate-50">
          <h2 class="text-lg font-medium text-slate-900 mb-4">2. ระบุสถานที่</h2>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">ค้นหาหรือปักหมุดบนแผนที่</label>
            <div class="mb-3 flex gap-2">
              <div class="relative flex-1">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>
                <input 
                  type="text" 
                  v-model="searchQuery" 
                  @keydown.enter.prevent="searchLocation"
                  placeholder="ค้นหาสถานที่..." 
                  class="block w-full pl-10 rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border bg-white"
                />
              </div>
              <button 
                type="button" 
                @click="searchLocation"
                class="px-4 py-2.5 bg-white border border-slate-300 text-slate-700 rounded-md hover:bg-slate-50 transition text-sm font-medium shadow-sm"
              >
                ค้นหา
              </button>
            </div>
            
            <div class="h-64 rounded-lg overflow-hidden border border-slate-300 shadow-inner relative z-0">
              <ClientOnly>
                <div id="picker-map" class="h-full w-full"></div>
              </ClientOnly>
            </div>
            
            <div class="mt-3 flex items-start gap-2">
              <svg class="w-5 h-5 text-indigo-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
              <div>
                <p class="text-sm font-medium text-slate-900" v-if="form.locationName">{{ form.locationName }}</p>
                <p class="text-sm font-medium text-red-600" v-else>ยังไม่ได้เลือกสถานที่</p>
                <p class="text-xs text-slate-500" v-if="form.mapCoords">{{ form.mapCoords }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Submission / Actions -->
        <div class="p-6 sm:p-8 bg-white flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="flex-1 w-full">
             <div v-if="submitStatus" :class="['p-3 flex items-center gap-2 rounded-md text-sm border', submitStatus.type === 'success' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-red-50 text-red-700 border-red-200']">
               <svg v-if="submitStatus.type === 'success'" class="w-5 h-5 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
               <svg v-else class="w-5 h-5 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
               {{ submitStatus.message }}
             </div>
          </div>
          <button 
            type="submit" 
            :disabled="isSubmitting || !form.mapCoords"
            class="w-full sm:w-auto inline-flex justify-center items-center gap-2 py-2.5 px-6 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            {{ isSubmitting ? 'กำลังประมวลผล...' : 'ส่งรายงาน' }}
          </button>
        </div>
      </form>
      
      <!-- AI Result Overlay -->
      <div v-if="aiResponse" class="border-t border-slate-200 bg-indigo-50 p-6 sm:p-8">
        <h3 class="text-sm font-bold tracking-wide text-indigo-900 uppercase mb-4 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          ผลการประเมินจาก AI
        </h3>
        <dl class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div class="bg-white rounded-lg p-4 shadow-sm border border-indigo-100">
            <dt class="text-xs font-medium text-slate-500 uppercase">หมวดหมู่ปัญหา</dt>
            <dd class="mt-1 text-sm font-semibold text-slate-900">{{ aiResponse.category }}</dd>
          </div>
          <div class="bg-white rounded-lg p-4 shadow-sm border border-indigo-100">
            <dt class="text-xs font-medium text-slate-500 uppercase">ระดับความรุนแรง</dt>
            <dd class="mt-1 flex items-center gap-2">
              <span class="text-sm font-semibold text-slate-900">Level {{ aiResponse.base_risk_level }}</span>
              <span v-if="aiResponse.base_risk_level === 3" class="w-2 h-2 rounded-full bg-red-500"></span>
              <span v-else-if="aiResponse.base_risk_level === 2" class="w-2 h-2 rounded-full bg-yellow-500"></span>
              <span v-else class="w-2 h-2 rounded-full bg-green-500"></span>
            </dd>
          </div>
          <div class="bg-white rounded-lg p-4 shadow-sm border border-indigo-100 sm:col-span-3">
            <dt class="text-xs font-medium text-slate-500 uppercase">เหตุผลที่ประเมิน</dt>
            <dd class="mt-1 text-sm text-slate-700">{{ aiResponse.reason }}</dd>
          </div>
        </dl>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, onBeforeUnmount } from 'vue'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase || 'http://localhost:8000'

const form = ref({
  issue: '',
  details: '',
  mapCoords: '',
  locationName: ''
})

let pickerMap = null
let pickerMarker = null
const searchQuery = ref('')

async function initMap() {
  await nextTick()
  if (typeof window !== 'undefined') {
    const L = await import('leaflet')
    if (!pickerMap) {
      pickerMap = L.map('picker-map').setView([18.7953, 98.9526], 15)
      
      // Free Google Maps Tiles (Roadmap view)
      L.tileLayer('http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}', {
        attribution: '&copy; Google Maps',
        maxZoom: 20
      }).addTo(pickerMap)
      
      pickerMap.on('click', async (e) => {
        if (pickerMarker) pickerMap.removeLayer(pickerMarker)
        pickerMarker = L.marker(e.latlng).addTo(pickerMap)
        form.value.mapCoords = `${e.latlng.lat.toFixed(5)}, ${e.latlng.lng.toFixed(5)}`
        
        // Free Reverse Geocoding via OpenStreetMap Nominatim
        try {
          const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${e.latlng.lat}&lon=${e.latlng.lng}`)
          const data = await res.json()
          if (data && data.display_name) {
            form.value.locationName = data.display_name
          } else {
            form.value.locationName = ''
          }
        } catch(err) {
          form.value.locationName = ''
        }
      })
    }
    setTimeout(() => pickerMap.invalidateSize(), 200)
  }
}

async function searchLocation() {
  if (!searchQuery.value) return
  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery.value)}`)
    const data = await res.json()
    if (data && data.length > 0) {
      const lat = parseFloat(data[0].lat)
      const lon = parseFloat(data[0].lon)
      if (pickerMap) {
        pickerMap.setView([lat, lon], 16)
        
        const L = await import('leaflet')
        if (pickerMarker) pickerMap.removeLayer(pickerMarker)
        pickerMarker = L.marker([lat, lon]).addTo(pickerMap)
        form.value.mapCoords = `${lat.toFixed(5)}, ${lon.toFixed(5)}`
        form.value.locationName = data[0].display_name || ''
      }
    } else {
      alert("Location not found. Try a different search term.")
    }
  } catch (e) {
    console.error("Search error:", e)
  }
}

onMounted(() => {
  initMap()
})

onBeforeUnmount(() => {
  if (pickerMap) {
    pickerMap.remove()
    pickerMap = null
  }
})

const isSubmitting = ref(false)
const submitStatus = ref(null)
const aiResponse = ref(null)

const finalLocation = computed(() => {
  if (form.value.locationName && form.value.mapCoords) {
    return `${form.value.locationName} | ${form.value.mapCoords}`
  }
  return form.value.mapCoords || 'No coordinates selected'
})

async function submitIssue() {
  if (!form.value.mapCoords) {
    submitStatus.value = { type: 'error', message: 'Please select a location on the map.' }
    return
  }

  isSubmitting.value = true
  submitStatus.value = null
  aiResponse.value = null
  
  try {
    const payload = {
      issue: form.value.issue,
      details: form.value.details,
      location: finalLocation.value
    }
    
    const res = await fetch(`${apiBase}/api/analyze-issue`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    if (!res.ok) {
      let errorMsg = 'Failed to analyze issue'
      try {
        const errData = await res.json()
        if (errData.detail) errorMsg = errData.detail
      } catch(e) {}
      throw new Error(errorMsg)
    }
    
    const data = await res.json()
    aiResponse.value = data
    
    submitStatus.value = {
      type: 'success',
      message: 'Incident successfully recorded and assessed.'
    }
    
    form.value.issue = ''
    form.value.details = ''
    form.value.mapCoords = ''
    form.value.locationName = ''
    searchQuery.value = ''
    if (pickerMarker && pickerMap) {
      pickerMap.removeLayer(pickerMarker)
      pickerMarker = null
    }
    
  } catch (err) {
    submitStatus.value = {
      type: 'error',
      message: err.message || 'An error occurred while submitting.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>
