<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Area Dashboard</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      <!-- Chart Card -->
      <div class="bg-white rounded-xl shadow-lg p-6 flex flex-col">
        <h2 class="text-lg font-semibold mb-4">Issues by Category</h2>
        <div class="flex-1 min-h-[250px] relative">
          <ClientOnly>
            <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
            <div v-else class="flex h-full items-center justify-center text-gray-500">Loading chart...</div>
          </ClientOnly>
        </div>
      </div>

      <!-- Map Card -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <h2 class="text-lg font-semibold mb-4">Interactive Map</h2>
        <div class="h-[250px] rounded-md overflow-hidden border">
          <ClientOnly>
            <div id="map" class="h-full w-full"></div>
          </ClientOnly>
        </div>
      </div>
    </div>
    
    <!-- Recent Issues Table -->
    <div class="mt-8 bg-white rounded-xl shadow-lg p-6">
      <h2 class="text-lg font-semibold mb-4">Recent Issues</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Issue</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Severity</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="issue in issues" :key="issue.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ new Date(issue.created_at).toLocaleDateString() }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ issue.issue }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ issue.location }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ issue.category }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="severityClass(issue.risk_level)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                  Level {{ issue.risk_level }}
                </span>
              </td>
            </tr>
            <tr v-if="issues.length === 0">
              <td colspan="5" class="px-6 py-4 text-center text-sm text-gray-500">No issues found or loading...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const config = useRuntimeConfig()
const apiBase = config.public.apiBase || 'http://localhost:8000'

const issues = ref([])
const chartData = ref(null)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
}

const severityClass = (level) => {
  if (level === 3) return 'bg-red-100 text-red-800'
  if (level === 2) return 'bg-yellow-100 text-yellow-800'
  return 'bg-green-100 text-green-800'
}

const locationCoordinates = {
  'Parking Area A': [18.7953, 98.9526],
  'Library': [18.7963, 98.9536],
  'Fitness Center': [18.7943, 98.9516],
  'Cafeteria': [18.7933, 98.9506],
}

onMounted(async () => {
  try {
    const res = await fetch(`${apiBase}/api/issues`)
    if (res.ok) {
      const data = await res.json()
      issues.value = data.data || []
      prepareChartData()
      initMap()
    }
  } catch (e) {
    console.error('Error fetching issues:', e)
  }
})

function prepareChartData() {
  const categories = {}
  issues.value.forEach(issue => {
    categories[issue.category] = (categories[issue.category] || 0) + 1
  })
  
  chartData.value = {
    labels: Object.keys(categories),
    datasets: [{
      label: 'Issues Reported',
      backgroundColor: '#4f46e5',
      data: Object.values(categories)
    }]
  }
}

async function initMap() {
  await nextTick()
  if (typeof window === 'undefined') return
  
  try {
    const L = await import('leaflet')
    
    const map = L.map('map').setView([18.7953, 98.9526], 15)
    
    L.tileLayer('http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}', {
      attribution: '&copy; Google Maps',
      maxZoom: 20
    }).addTo(map)
    
    issues.value.forEach(issue => {
      let coords = null
      
      // Parse coordinates if they come from the Map Picker (e.g. "Library | 18.795, 98.952" or "18.79, 98.95")
      if (issue.location) {
        let coordString = issue.location
        if (coordString.includes('|')) {
          coordString = coordString.split('|')[1].trim()
        }
        
        if (coordString.includes(',')) {
          const parts = coordString.split(',')
          if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
            coords = [parseFloat(parts[0]), parseFloat(parts[1])]
          }
        }
      }
      
      // Fallback to legacy dictionary or random scatter
      if (!coords) {
        coords = locationCoordinates[issue.location]
      }
      if (!coords) {
        coords = [18.7953 + (Math.random() - 0.5)*0.01, 98.9526 + (Math.random() - 0.5)*0.01]
      }
      
      if (coords) {
        let color = 'green'
        if (issue.risk_level === 3) color = 'red'
        if (issue.risk_level === 2) color = 'yellow'
        
        L.circleMarker(coords, {
          color: color,
          fillColor: color,
          fillOpacity: 0.7,
          radius: 8
        }).addTo(map)
        .bindPopup(`<b>${issue.issue}</b><br>Level ${issue.risk_level}<br>${issue.category}`)
      }
    })
  } catch (e) {
    console.error("Map initialization failed", e)
  }
}
</script>
