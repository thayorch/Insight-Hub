<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
    <div class="flex flex-col sm:flex-row justify-between sm:items-end gap-4 mb-6 sm:mb-8">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">แดชบอร์ดสรุปผล</h1>
        <p class="mt-1 text-sm text-slate-500">ภาพรวมสถานการณ์และผลการประเมินความเสี่ยงจาก AI แบบเรียลไทม์</p>
      </div>
      <div class="w-full sm:w-auto">
        <button @click="refreshData" class="w-full sm:w-auto inline-flex justify-center items-center gap-2 px-4 py-2 border border-slate-300 rounded-md shadow-sm text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition">
          <svg class="h-4 w-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          รีเฟรชข้อมูล
        </button>
      </div>
    </div>
    
    <!-- KPI Summary Row -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
        <div class="p-3 bg-indigo-50 rounded-lg text-indigo-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500">ปัญหาทั้งหมด</p>
          <p class="text-2xl font-bold text-slate-900">{{ issues.length }}</p>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
        <div class="p-3 bg-red-50 rounded-lg text-red-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500">ภัยคุกคามฉุกเฉิน (Level 3)</p>
          <p class="text-2xl font-bold text-slate-900">{{ issues.filter(i => i.risk_level === 3).length }}</p>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
        <div class="p-3 bg-yellow-50 rounded-lg text-yellow-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500">ปัญหาซ้ำซาก (Level 2)</p>
          <p class="text-2xl font-bold text-slate-900">{{ issues.filter(i => i.risk_level === 2).length }}</p>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
        <div class="p-3 bg-green-50 rounded-lg text-green-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500">ปัญหาทั่วไป (Level 1)</p>
          <p class="text-2xl font-bold text-slate-900">{{ issues.filter(i => i.risk_level === 1).length }}</p>
        </div>
      </div>
    </div>
    
    <!-- Filters -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-8 flex flex-col sm:flex-row gap-3">
      <div class="relative flex-1">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-4 w-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        </div>
        <input
          type="text"
          v-model="searchText"
          placeholder="ค้นหาหัวข้อ / รายละเอียด / สถานที่..."
          class="block w-full pl-10 rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border bg-white"
        />
      </div>
      <select v-model="filterCategory" class="w-full sm:w-auto rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border bg-white">
        <option value="">ทุกหมวดหมู่</option>
        <option v-for="c in CATEGORIES" :key="c" :value="c">{{ c }}</option>
      </select>
      <select v-model="filterStatus" class="w-full sm:w-auto rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border bg-white">
        <option value="">ทุกสถานะ</option>
        <option v-for="s in STATUS_FLOW" :key="s" :value="s">{{ statusLabel(s) }}</option>
      </select>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
      <div class="lg:col-span-1 flex flex-col gap-8">
        <!-- Severity Pie Chart Card -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col">
          <h2 class="text-base font-semibold text-slate-900 mb-6">สัดส่วนปัญหาแบ่งตามระดับความรุนแรง</h2>
          <div class="flex-1 min-h-[220px] relative">
            <ClientOnly>
              <Pie v-if="chartData" :data="chartData" :options="chartOptions" />
              <div v-else class="flex h-full items-center justify-center text-slate-400 text-sm">กำลังโหลดข้อมูลกราฟ...</div>
            </ClientOnly>
          </div>
        </div>

        <!-- Category Bar Chart Card -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col">
          <h2 class="text-base font-semibold text-slate-900 mb-6">จำนวนปัญหาแยกตามหมวดหมู่</h2>
          <div class="flex-1 min-h-[220px] relative">
            <ClientOnly>
              <Bar v-if="categoryChartData" :data="categoryChartData" :options="barChartOptions" />
              <div v-else class="flex h-full items-center justify-center text-slate-400 text-sm">กำลังโหลดข้อมูลกราฟ...</div>
            </ClientOnly>
          </div>
        </div>

        <!-- Status Doughnut Chart Card -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col">
          <h2 class="text-base font-semibold text-slate-900 mb-6">สถานะการแก้ไข</h2>
          <div class="flex-1 min-h-[220px] relative">
            <ClientOnly>
              <Doughnut v-if="statusChartData" :data="statusChartData" :options="chartOptions" />
              <div v-else class="flex h-full items-center justify-center text-slate-400 text-sm">กำลังโหลดข้อมูลกราฟ...</div>
            </ClientOnly>
          </div>
        </div>
      </div>

      <!-- Map Card -->
      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6">
          <h2 class="text-base font-semibold text-slate-900">แผนที่จุดเกิดเหตุ</h2>
          <div class="flex rounded-md border border-slate-300 overflow-hidden text-xs font-medium">
            <button type="button" @click="setMapView('marker')" :class="mapView === 'marker' ? 'bg-indigo-600 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'" class="px-3 py-1.5 transition">หมุด</button>
            <button type="button" @click="setMapView('heatmap')" :class="mapView === 'heatmap' ? 'bg-indigo-600 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'" class="px-3 py-1.5 transition border-l border-slate-300">ความหนาแน่น</button>
          </div>
        </div>
        <div class="flex-1 min-h-[280px] sm:min-h-[380px] lg:min-h-[460px] rounded-lg overflow-hidden border border-slate-200 relative z-0">
          <ClientOnly>
            <div id="map" class="absolute inset-0"></div>
          </ClientOnly>
        </div>
      </div>
    </div>
    
    <!-- Recent Issues Table -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="px-6 py-5 border-b border-slate-200">
        <h2 class="text-base font-semibold text-slate-900">บันทึกประวัติ (Issue Log)</h2>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200">
          <thead class="bg-slate-50">
            <tr>
              <th scope="col" class="px-6 py-3.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Case ID</th>
              <th scope="col" class="px-6 py-3.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">วันและเวลา</th>
              <th scope="col" class="px-6 py-3.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">หัวข้อปัญหา</th>
              <th scope="col" class="px-6 py-3.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">สถานที่</th>
              <th scope="col" class="px-6 py-3.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">หมวดหมู่</th>
              <th scope="col" class="px-6 py-3.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">ความรุนแรง</th>
              <th scope="col" class="px-6 py-3.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">สถานะ</th>
              <th scope="col" class="px-6 py-3.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">ผู้รับผิดชอบ</th>
              <th scope="col" class="relative px-6 py-3.5">
                <span class="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-slate-200">
            <tr v-for="issue in filteredIssues" :key="issue.id" @click="focusOnMap(issue)" class="group hover:bg-indigo-50 transition cursor-pointer">
              <td class="px-6 py-4 whitespace-nowrap text-xs font-mono text-slate-500">#{{ issue.id.slice(0, 8).toUpperCase() }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{{ new Date(issue.created_at).toLocaleString() }}</td>
              <td class="px-6 py-4 text-sm font-medium text-slate-900 max-w-xs truncate" :title="issue.issue">{{ issue.issue }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                <div class="flex items-center gap-1.5">
                  <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z"></path></svg>
                  <span class="truncate max-w-[150px] inline-block" :title="issue.location.split('|')[0]">{{ issue.location.split('|')[0] }}</span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-slate-100 text-slate-800">
                  {{ issue.category }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="severityClass(issue.risk_level)" class="px-2.5 py-1 inline-flex text-xs font-semibold rounded-md border">
                  Level {{ issue.risk_level }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button @click.stop="cycleStatus(issue)" :class="statusClass(issue.status)" class="px-2.5 py-1 inline-flex text-xs font-semibold rounded-md border" title="คลิกเพื่อเปลี่ยนสถานะ">
                  {{ statusLabel(issue.status) }}
                </button>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ issue.assignee || '-' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center justify-end gap-3 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button @click.stop="editIssue(issue)" class="text-indigo-600 hover:text-indigo-900" title="Edit Title">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                  </button>
                  <button @click.stop="toggleLevel(issue)" class="text-yellow-600 hover:text-yellow-900" title="Change Severity Level">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                  </button>
                  <button @click.stop="deleteIssue(issue.id)" class="text-red-600 hover:text-red-900" title="Delete Log">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredIssues.length === 0">
              <td colspan="9" class="px-6 py-12 text-center text-sm text-slate-500">
                <div class="flex flex-col items-center">
                  <svg class="h-10 w-10 text-slate-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
                  <p>ไม่มีบันทึกข้อมูลในขณะนี้</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    <!-- Edit Modal -->
    <div v-if="editingIssue" class="fixed inset-0 z-[1000] overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity bg-slate-900 bg-opacity-75" @click="closeEditModal" aria-hidden="true"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        
        <div class="inline-block align-bottom bg-white rounded-xl text-left shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 rounded-t-xl border-b border-slate-200">
            <div class="flex justify-between items-center mb-5">
              <h3 class="text-xl leading-6 font-semibold text-slate-900" id="modal-title">แก้ไขรายงานปัญหา</h3>
              <button @click="closeEditModal" class="text-slate-400 hover:text-slate-500">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
            
            <form @submit.prevent="saveEditIssue" class="space-y-6">
              <!-- Section 1 -->
              <div>
                <h2 class="text-sm font-semibold tracking-wide text-indigo-900 uppercase mb-3">1. ข้อมูลปัญหา</h2>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">หัวข้อปัญหา (ประเด็น)</label>
                    <input type="text" v-model="editForm.issue" required class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border" />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">รายละเอียดเพิ่มเติม</label>
                    <textarea v-model="editForm.details" rows="3" required class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border"></textarea>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">ผู้รับผิดชอบ</label>
                    <input type="text" v-model="editForm.assignee" placeholder="ชื่อผู้รับผิดชอบ (ถ้ามี)" class="block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border" />
                  </div>
                </div>
              </div>

              <!-- Section 2 -->
              <div>
                <h2 class="text-sm font-semibold tracking-wide text-indigo-900 uppercase mb-3">2. ระบุสถานที่</h2>
                <div>
                  <div class="mb-3 flex gap-2">
                    <div class="relative flex-1">
                      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg class="h-4 w-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                      </div>
                      <input type="text" v-model="editSearchQuery" @keydown.enter.prevent="searchEditLocation" placeholder="ค้นหาสถานที่..." class="block w-full pl-10 rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 border bg-white" />
                    </div>
                    <button type="button" @click="searchEditLocation" class="px-4 py-2 bg-white border border-slate-300 text-slate-700 rounded-md hover:bg-slate-50 transition text-sm font-medium shadow-sm">ค้นหา</button>
                  </div>
                  
                  <div class="h-56 rounded-lg overflow-hidden border border-slate-300 shadow-inner relative z-0">
                    <ClientOnly>
                      <div id="edit-map" class="h-full w-full"></div>
                    </ClientOnly>
                  </div>
                  
                  <div class="mt-3 flex items-start gap-2">
                    <svg class="w-5 h-5 text-indigo-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                    <div>
                      <p class="text-sm font-medium text-slate-900" v-if="editForm.locationName">{{ editForm.locationName }}</p>
                      <p class="text-sm font-medium text-red-600" v-else>ยังไม่ได้เลือกสถานที่</p>
                      <p class="text-xs text-slate-500" v-if="editForm.mapCoords">{{ editForm.mapCoords }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="bg-slate-50 px-4 py-4 sm:px-6 flex flex-col sm:flex-row items-center sm:justify-between gap-4 rounded-b-xl border-t border-slate-200">
            <div class="w-full sm:w-auto sm:flex-1 sm:mr-4">
               <div v-if="saveStatus" :class="['p-2 text-xs rounded border text-center sm:text-left', saveStatus.type === 'success' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-red-50 text-red-700 border-red-200']">
                 {{ saveStatus.message }}
               </div>
            </div>
            <div class="flex gap-3 w-full sm:w-auto">
              <button type="button" @click="closeEditModal" class="flex-1 sm:flex-none inline-flex justify-center rounded-md border border-slate-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-slate-700 hover:bg-slate-50 focus:outline-none sm:text-sm">ยกเลิก</button>
              <button type="button" @click="saveEditIssue" :disabled="isSaving || !editForm.mapCoords" class="flex-1 sm:flex-none inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none disabled:opacity-50 sm:text-sm">
                {{ isSaving ? 'กำลังบันทึก...' : 'บันทึกการแก้ไข' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { Pie, Bar, Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale)

const config = useRuntimeConfig()
const apiBase = config.public.apiBase || 'http://localhost:8000'

const CATEGORIES = ['Safety & Persons', 'Structure & Traffic', 'Common areas', 'Environment']

const issues = ref([])
const chartData = ref(null)
const categoryChartData = ref(null)
const statusChartData = ref(null)

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: { beginAtZero: true, ticks: { precision: 0 } }
  }
}

const searchText = ref('')
const filterCategory = ref('')
const filterStatus = ref('')

const filteredIssues = computed(() => {
  return issues.value.filter(i => {
    if (filterCategory.value && i.category !== filterCategory.value) return false
    if (filterStatus.value && i.status !== filterStatus.value) return false
    if (searchText.value) {
      const q = searchText.value.toLowerCase()
      const haystack = `${i.issue} ${i.details} ${i.location}`.toLowerCase()
      if (!haystack.includes(q)) return false
    }
    return true
  })
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      display: true
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.label || ''
          if (label) {
            label += ': '
          }
          if (context.parsed !== null) {
            const total = context.dataset.data.reduce((a, b) => a + b, 0)
            const percentage = ((context.parsed / total) * 100).toFixed(1) + '%'
            label += context.parsed + ' รายการ (' + percentage + ')'
          }
          return label
        }
      }
    }
  }
}

const severityClass = (level) => {
  if (level === 3) return 'bg-red-50 text-red-700 border-red-200'
  if (level === 2) return 'bg-yellow-50 text-yellow-700 border-yellow-200'
  return 'bg-green-50 text-green-700 border-green-200'
}

const STATUS_FLOW = ['unresolved', 'in_progress', 'resolved']
const STATUS_LABELS = {
  unresolved: 'ยังไม่ได้แก้ไข',
  in_progress: 'กำลังดำเนินการ',
  resolved: 'แก้ไขแล้ว'
}
const STATUS_CLASSES = {
  unresolved: 'bg-slate-100 text-slate-700 border-slate-300',
  in_progress: 'bg-blue-50 text-blue-700 border-blue-200',
  resolved: 'bg-green-50 text-green-700 border-green-200'
}

const statusLabel = (status) => STATUS_LABELS[status] || STATUS_LABELS.unresolved
const statusClass = (status) => STATUS_CLASSES[status] || STATUS_CLASSES.unresolved

const cycleStatus = async (issue) => {
  const currentIndex = STATUS_FLOW.indexOf(issue.status)
  const nextStatus = STATUS_FLOW[(currentIndex + 1) % STATUS_FLOW.length] || STATUS_FLOW[0]
  try {
    const res = await fetch(`${apiBase}/api/issues/${issue.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: nextStatus })
    })
    if (res.ok) await fetchData()
  } catch (e) {
    console.error('Failed to update status', e)
  }
}

const refreshData = async () => {
  issues.value = []
  chartData.value = null
  categoryChartData.value = null
  statusChartData.value = null
  await fetchData()
}

async function fetchData() {
  try {
    const res = await fetch(`${apiBase}/api/issues`)
    if (res.ok) {
      const data = await res.json()
      issues.value = data.data || []
      prepareChartData()
      prepareCategoryChartData()
      prepareStatusChartData()
      initMap()
    }
  } catch (e) {
    console.error('Error fetching issues:', e)
  }
}

onMounted(() => {
  fetchData()
})

watch([searchText, filterCategory, filterStatus], () => {
  initMap()
})

const mapView = ref('marker')

function setMapView(view) {
  mapView.value = view
  applyMapView()
}

const deleteIssue = async (id) => {
  if(!confirm("Are you sure you want to permanently delete this incident log?")) return;
  try {
    const res = await fetch(`${apiBase}/api/issues/${id}`, { method: 'DELETE' })
    if (res.ok) await fetchData()
  } catch(e) {
    console.error("Failed to delete", e)
  }
}

const editingIssue = ref(null)
const editForm = ref({
  issue: '',
  details: '',
  mapCoords: '',
  locationName: '',
  assignee: ''
})
const editSearchQuery = ref('')
const isSaving = ref(false)
const saveStatus = ref(null)
let editMapInstance = null
let editMarker = null

const editIssue = (issue) => {
  editingIssue.value = issue
  editForm.value.issue = issue.issue || ''
  editForm.value.details = issue.details || ''
  editForm.value.assignee = issue.assignee || ''
  editSearchQuery.value = ''
  saveStatus.value = null
  
  let coords = null
  let name = ''
  if (issue.location) {
    if (issue.location.includes('|')) {
       const parts = issue.location.split('|')
       name = parts[0].trim()
       const coordStr = parts[1].trim()
       if(coordStr.includes(',')) {
         const cp = coordStr.split(',')
         coords = [parseFloat(cp[0]), parseFloat(cp[1])]
       }
    } else if (issue.location.includes(',')) {
       const cp = issue.location.split(',')
       if(cp.length === 2 && !isNaN(cp[0]) && !isNaN(cp[1])) {
         coords = [parseFloat(cp[0]), parseFloat(cp[1])]
       }
    }
  }
  
  editForm.value.locationName = name
  if (coords) {
    editForm.value.mapCoords = `${coords[0].toFixed(5)}, ${coords[1].toFixed(5)}`
  } else {
    editForm.value.mapCoords = ''
  }
  
  nextTick(() => {
     initEditMap(coords)
  })
}

const closeEditModal = () => {
  editingIssue.value = null
  if(editMapInstance) {
    editMapInstance.remove()
    editMapInstance = null
    editMarker = null
  }
}

async function initEditMap(initialCoords) {
  if (typeof window === 'undefined') return
  const L = await import('leaflet')
  
  if (!editMapInstance) {
    const center = initialCoords || [18.8038, 98.9530]
    editMapInstance = L.map('edit-map').setView(center, 15)
    L.tileLayer('http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}', {
      attribution: '&copy; Google Maps',
      maxZoom: 20
    }).addTo(editMapInstance)
    
    const getEditIcon = () => L.divIcon({
      className: 'bg-transparent border-0',
      html: `<div style="color: #4f46e5; filter: drop-shadow(0 4px 3px rgb(0 0 0 / 0.15));"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width: 32px; height: 32px;"><path fill-rule="evenodd" d="M11.54 22.351l.07.04.028.016a.76.76 0 00.723 0l.028-.015.071-.041a16.975 16.975 0 001.144-.742 19.58 19.58 0 002.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 00-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 002.682 2.282 16.975 16.975 0 001.145.742zM12 13.5a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" /></svg></div>`,
      iconSize: [32, 32],
      iconAnchor: [16, 32],
      popupAnchor: [0, -32]
    })
    
    if (initialCoords) {
      editMarker = L.marker(initialCoords, { icon: getEditIcon() }).addTo(editMapInstance)
    }
    
    editMapInstance.on('click', async (e) => {
      if (editMarker) editMapInstance.removeLayer(editMarker)
      editMarker = L.marker(e.latlng, { icon: getEditIcon() }).addTo(editMapInstance)
      editForm.value.mapCoords = `${e.latlng.lat.toFixed(5)}, ${e.latlng.lng.toFixed(5)}`
      
      try {
        const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${e.latlng.lat}&lon=${e.latlng.lng}`)
        const data = await res.json()
        if (data && data.display_name) {
          editForm.value.locationName = data.display_name
        } else {
          editForm.value.locationName = ''
        }
      } catch(err) {
        editForm.value.locationName = ''
      }
    })
  }
  setTimeout(() => editMapInstance.invalidateSize(), 200)
}

async function searchEditLocation() {
  if (!editSearchQuery.value) return
  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(editSearchQuery.value)}`)
    const data = await res.json()
    if (data && data.length > 0) {
      const lat = parseFloat(data[0].lat)
      const lon = parseFloat(data[0].lon)
      if (editMapInstance) {
        editMapInstance.setView([lat, lon], 16)
        const L = await import('leaflet')
        const getEditIcon = () => L.divIcon({
          className: 'bg-transparent border-0',
          html: `<div style="color: #4f46e5; filter: drop-shadow(0 4px 3px rgb(0 0 0 / 0.15));"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width: 32px; height: 32px;"><path fill-rule="evenodd" d="M11.54 22.351l.07.04.028.016a.76.76 0 00.723 0l.028-.015.071-.041a16.975 16.975 0 001.144-.742 19.58 19.58 0 002.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 00-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 002.682 2.282 16.975 16.975 0 001.145.742zM12 13.5a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" /></svg></div>`,
          iconSize: [32, 32],
          iconAnchor: [16, 32],
          popupAnchor: [0, -32]
        })
        if (editMarker) editMapInstance.removeLayer(editMarker)
        editMarker = L.marker([lat, lon], { icon: getEditIcon() }).addTo(editMapInstance)
        editForm.value.mapCoords = `${lat.toFixed(5)}, ${lon.toFixed(5)}`
        editForm.value.locationName = data[0].display_name || ''
      }
    }
  } catch (e) {
    console.error("Search error:", e)
  }
}

const saveEditIssue = async () => {
  isSaving.value = true
  saveStatus.value = null
  
  const finalLoc = (editForm.value.locationName && editForm.value.mapCoords) 
    ? `${editForm.value.locationName} | ${editForm.value.mapCoords}`
    : editForm.value.mapCoords || 'No coordinates selected'
    
  try {
    const res = await fetch(`${apiBase}/api/issues/${editingIssue.value.id}`, { 
      method: 'PATCH',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        issue: editForm.value.issue,
        details: editForm.value.details,
        location: finalLoc,
        assignee: editForm.value.assignee
      })
    })
    if (res.ok) {
      saveStatus.value = { type: 'success', message: 'Incident updated successfully.' }
      await fetchData()
      setTimeout(() => closeEditModal(), 1500)
    } else {
      throw new Error('Update failed')
    }
  } catch(e) {
    saveStatus.value = { type: 'error', message: 'Failed to save changes.' }
    console.error(e)
  } finally {
    isSaving.value = false
  }
}

const toggleLevel = async (issue) => {
  // Cycle levels: 1 -> 2 -> 3 -> 1
  const newLevel = issue.risk_level === 3 ? 1 : (issue.risk_level + 1)
  try {
    const res = await fetch(`${apiBase}/api/issues/${issue.id}`, { 
      method: 'PATCH',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ risk_level: newLevel })
    })
    if (res.ok) await fetchData()
  } catch(e) {
    console.error("Failed to toggle level", e)
  }
}

function prepareChartData() {
  const levels = {
    'Level 3 (ฉุกเฉิน)': 0,
    'Level 2 (ซ้ำซาก)': 0,
    'Level 1 (ทั่วไป)': 0
  }
  
  issues.value.forEach(issue => {
    if (issue.risk_level === 3) levels['Level 3 (ฉุกเฉิน)']++
    else if (issue.risk_level === 2) levels['Level 2 (ซ้ำซาก)']++
    else levels['Level 1 (ทั่วไป)']++
  })
  
  chartData.value = {
    labels: Object.keys(levels),
    datasets: [{
      backgroundColor: ['#ef4444', '#eab308', '#22c55e'], // Red, Yellow, Green
      data: Object.values(levels),
      borderWidth: 1
    }]
  }
}

function prepareCategoryChartData() {
  const counts = {}
  CATEGORIES.forEach(c => { counts[c] = 0 })

  issues.value.forEach(issue => {
    counts[issue.category] = (counts[issue.category] || 0) + 1
  })

  categoryChartData.value = {
    labels: Object.keys(counts),
    datasets: [{
      label: 'จำนวนปัญหา',
      backgroundColor: '#6366f1',
      data: Object.values(counts),
      borderRadius: 6
    }]
  }
}

const STATUS_CHART_COLORS = {
  unresolved: '#94a3b8',
  in_progress: '#3b82f6',
  resolved: '#22c55e'
}

function prepareStatusChartData() {
  const counts = {}
  STATUS_FLOW.forEach(s => { counts[s] = 0 })

  issues.value.forEach(issue => {
    const s = STATUS_FLOW.includes(issue.status) ? issue.status : 'unresolved'
    counts[s]++
  })

  statusChartData.value = {
    labels: STATUS_FLOW.map(s => statusLabel(s)),
    datasets: [{
      backgroundColor: STATUS_FLOW.map(s => STATUS_CHART_COLORS[s]),
      data: STATUS_FLOW.map(s => counts[s]),
      borderWidth: 1
    }]
  }
}

let mapInstance = null
let markerLayerGroup = null
let heatLayerInstance = null
let markersMap = {}

function applyMapView() {
  if (!mapInstance || !markerLayerGroup) return
  if (mapView.value === 'heatmap' && heatLayerInstance) {
    if (mapInstance.hasLayer(markerLayerGroup)) mapInstance.removeLayer(markerLayerGroup)
    if (!mapInstance.hasLayer(heatLayerInstance)) heatLayerInstance.addTo(mapInstance)
  } else {
    if (heatLayerInstance && mapInstance.hasLayer(heatLayerInstance)) mapInstance.removeLayer(heatLayerInstance)
    if (!mapInstance.hasLayer(markerLayerGroup)) markerLayerGroup.addTo(mapInstance)
  }
}

async function initMap() {
  await nextTick()
  if (typeof window === 'undefined') return

  try {
    const L = await import('leaflet')

    if (!mapInstance) {
      mapInstance = L.map('map').setView([18.8038, 98.9530], 15)
      L.tileLayer('http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}', {
        attribution: '&copy; Google Maps',
        maxZoom: 20
      }).addTo(mapInstance)

      markerLayerGroup = L.layerGroup()

      try {
        await import('leaflet.heat')
        heatLayerInstance = L.heatLayer([], { radius: 30, blur: 20, maxZoom: 18 })
      } catch (heatErr) {
        console.error('Heatmap layer unavailable, falling back to markers only', heatErr)
        heatLayerInstance = null
      }
    } else {
      markerLayerGroup.clearLayers()
    }

    markersMap = {}
    const heatPoints = []

    filteredIssues.value.forEach(issue => {
      let coords = null
      
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
      
      if (!coords) {
        coords = [18.8038 + (Math.random() - 0.5)*0.01, 98.9530 + (Math.random() - 0.5)*0.01]
      }
      
      if (coords) {
        let color = '#22c55e' // green-500
        if (issue.risk_level === 3) color = '#ef4444' // red-500
        if (issue.risk_level === 2) color = '#eab308' // yellow-500
        
        const customIcon = L.divIcon({
          className: 'bg-transparent border-0',
          html: `<div style="color: ${color}; filter: drop-shadow(0 4px 3px rgb(0 0 0 / 0.15));"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width: 32px; height: 32px;"><path fill-rule="evenodd" d="M11.54 22.351l.07.04.028.016a.76.76 0 00.723 0l.028-.015.071-.041a16.975 16.975 0 001.144-.742 19.58 19.58 0 002.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 00-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 002.682 2.282 16.975 16.975 0 001.145.742zM12 13.5a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" /></svg></div>`,
          iconSize: [32, 32],
          iconAnchor: [16, 32],
          popupAnchor: [0, -32]
        })

        const marker = L.marker(coords, { icon: customIcon }).addTo(markerLayerGroup)
        .bindPopup(`
          <div style="font-family: sans-serif;">
            <strong style="display:block;margin-bottom:4px;color:#0f172a">${issue.issue}</strong>
            <span style="display:inline-block;padding:2px 6px;border-radius:4px;background:#f1f5f9;font-size:12px;color:#475569;margin-bottom:4px;">${issue.category}</span>
            <div style="font-size:12px;color:#64748b;">Risk Level: <b style="color:${color}">${issue.risk_level}</b></div>
          </div>
        `)

        markersMap[issue.id] = marker

        const intensity = issue.risk_level === 3 ? 1 : issue.risk_level === 2 ? 0.6 : 0.3
        heatPoints.push([coords[0], coords[1], intensity])
      }
    })

    if (heatLayerInstance) heatLayerInstance.setLatLngs(heatPoints)
    applyMapView()
  } catch (e) {
    console.error("Map initialization failed", e)
  }
}

function focusOnMap(issue) {
  if (mapInstance && markersMap[issue.id]) {
    if (mapView.value !== 'marker') setMapView('marker')

    // Scroll smoothly up to the map container
    document.getElementById('map').scrollIntoView({ behavior: 'smooth', block: 'center' })

    // Fly to the coordinates and open the popup
    const marker = markersMap[issue.id]
    mapInstance.flyTo(marker.getLatLng(), 18, { duration: 1.5 })
    
    // Open popup after flying finishes
    setTimeout(() => {
      marker.openPopup()
    }, 1500)
  }
}
</script>
