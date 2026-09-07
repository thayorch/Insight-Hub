<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-xl shadow-lg p-6">
      <h1 class="text-2xl font-bold text-gray-800 mb-6 text-center">Report an Issue</h1>
      
      <form @submit.prevent="submitIssue" class="space-y-4">
        <!-- Issue Title -->
        <div>
          <label for="issue" class="block text-sm font-medium text-gray-700">Issue Title</label>
          <input 
            type="text" 
            id="issue" 
            v-model="form.issue" 
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
            placeholder="E.g., Broken pipe, Suspicious person"
          />
        </div>

        <!-- Details -->
        <div>
          <label for="details" class="block text-sm font-medium text-gray-700">Details</label>
          <textarea 
            id="details" 
            v-model="form.details" 
            rows="3" 
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
            placeholder="Describe the problem in detail..."
          ></textarea>
        </div>

        <!-- Map Picker Input -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Location (Click on the map or search)</label>
          <div class="mb-2 flex gap-2">
            <input 
              type="text" 
              v-model="searchQuery" 
              @keydown.enter.prevent="searchLocation"
              placeholder="Search for a place (e.g. Library)" 
              class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
            />
            <button 
              type="button" 
              @click="searchLocation"
              class="px-3 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 text-sm font-medium"
            >
              Search
            </button>
          </div>
          <div class="h-48 rounded-md overflow-hidden border relative">
            <ClientOnly>
              <div id="picker-map" class="h-full w-full"></div>
            </ClientOnly>
          </div>
          <p class="text-xs text-gray-700 mt-1" v-if="form.locationName"><strong>Selected:</strong> {{ form.locationName }} ({{ form.mapCoords }})</p>
          <p class="text-xs text-gray-500 mt-1" v-else-if="form.mapCoords">Selected Coordinates: {{ form.mapCoords }}</p>
          <p class="text-xs text-red-500 mt-1" v-else>Please select a location on the map.</p>
        </div>

        <!-- Submit Button -->
        <button 
          type="submit" 
          :disabled="isSubmitting || !form.mapCoords"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {{ isSubmitting ? 'Submitting...' : 'Submit Report' }}
        </button>

        <!-- Status Message -->
        <div v-if="submitStatus" :class="['mt-4 p-3 rounded-md text-sm', submitStatus.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700']">
          {{ submitStatus.message }}
        </div>
        
        <div v-if="aiResponse" class="mt-4 p-4 bg-gray-100 rounded-md text-sm text-gray-800">
          <h3 class="font-bold mb-2">AI Analysis Result:</h3>
          <p><strong>Category:</strong> {{ aiResponse.category }}</p>
          <p><strong>Severity Level:</strong> {{ aiResponse.base_risk_level }}</p>
          <p><strong>Reason:</strong> {{ aiResponse.reason }}</p>
        </div>
      </form>
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
    // Ensures map draws correctly when shown/hidden
    setTimeout(() => pickerMap.invalidateSize(), 200)
  }
}

async function searchLocation() {
  if (!searchQuery.value) return
  try {
    // Free Geocoding Search via OpenStreetMap Nominatim
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
    
    // Attempting to send to backend API
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
      message: 'Issue successfully reported and analyzed!'
    }
    
    // Optionally reset form
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
