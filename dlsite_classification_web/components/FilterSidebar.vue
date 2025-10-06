<template>
  <aside
    class="flex-shrink-0 bg-bg-secondary backdrop-blur-xl border-r border-bg-border fixed left-0 top-0 h-full z-30 flex flex-col transition-all duration-300 ease-out shadow-2xl"
    :class="[
      isCollapsed ? 'w-16' : 'w-80',
      { 'translate-x-0': isVisible, '-translate-x-full lg:translate-x-0': !isVisible }
    ]"
  >
    <div class="flex-1 overflow-y-auto" :class="{ 'overflow-hidden': isCollapsed }">
      <!-- Collapsed State - Show expand button -->
      <div v-if="isCollapsed" class="flex flex-col items-center py-6 gap-4">
        <button
          @click="$emit('toggle-collapse')"
          class="p-3 text-text-muted hover:text-text-primary hover:bg-bg-elevated rounded-lg transition-all duration-200 hover:scale-110"
          title="展開側邊欄"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <div class="p-6 space-y-6" v-if="!isCollapsed">
        <!-- Sidebar Header -->
        <div class="flex items-center justify-between pb-4 border-b border-bg-border">
          <h2 class="text-xl font-bold text-text-primary flex items-center gap-3">
            <svg class="w-6 h-6 text-accent-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707v4.172a1 1 0 01-.434.82l-2 1.333A1 1 0 019 19.086v-5.379a1 1 0 00-.293-.707L2.293 7.586A1 1 0 012 6.879V4z" />
            </svg>
            篩選控制台
          </h2>
          <div class="flex items-center gap-1">
            <button
              @click="$emit('toggle-collapse')"
              class="p-2 text-text-muted hover:text-text-primary hover:bg-bg-elevated rounded-lg transition-all duration-200"
              title="收起側邊欄"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
              </svg>
            </button>
            <button
              @click="$emit('toggle-visibility')"
              class="lg:hidden p-2 text-text-muted hover:text-text-primary hover:bg-bg-elevated rounded-lg transition-all duration-200"
              title="關閉側邊欄"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Search -->
        <div class="space-y-3">
          <label class="block text-sm font-medium text-text-muted">搜索</label>
          <div class="relative group">
            <input
              :value="modelValue.search"
              @input="updateFilter('search', $event.target.value)"
              type="text"
              placeholder="搜索作品、公司、標籤..."
              class="input w-full pl-10 pr-10 transition-all duration-200"
            >
            <div class="absolute left-3 top-1/2 transform -translate-y-1/2 text-text-muted group-focus-within:text-accent-primary transition-colors duration-200">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <div v-if="modelValue.search" class="absolute right-3 top-1/2 transform -translate-y-1/2">
              <button
                @click="updateFilter('search', '')"
                class="p-1 text-text-muted hover:text-text-primary hover:bg-bg-elevated rounded transition-all duration-200"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="space-y-4">
          <h3 class="text-base font-semibold text-text-primary">基本篩選</h3>

          <!-- Company Filter -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-text-muted">公司</label>
            <div class="relative">
              <input
                v-model="companySearchQuery"
                @input="filterCompanies"
                @focus="showCompanyDropdown = true"
                @blur="hideCompanyDropdown"
                type="text"
                placeholder="搜索或選擇公司..."
                class="input w-full text-sm"
              >
              <div
                v-if="showCompanyDropdown && filteredCompanies.length > 0"
                class="absolute top-full left-0 right-0 bg-bg-elevated backdrop-blur-xl border border-bg-border rounded-lg shadow-xl z-50 max-h-60 overflow-y-auto mt-1 animate-slide-up"
              >
                <button
                  @mousedown="selectCompany('')"
                  class="w-full text-left px-3 py-2 hover:bg-accent-primary/10 text-text-muted text-sm border-b border-bg-border transition-colors duration-150"
                >
                  所有公司
                </button>
                <button
                  v-for="company in filteredCompanies"
                  :key="company"
                  @mousedown="selectCompany(company)"
                  class="w-full text-left px-3 py-2 hover:bg-accent-primary/10 text-text-primary text-sm transition-colors duration-150"
                >
                  {{ company }}
                </button>
              </div>
            </div>
          </div>

          <!-- Collection Filter -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-text-muted">收藏分類</label>
            <select :value="modelValue.collection" @change="updateFilter('collection', $event.target.value)" class="input w-full text-sm">
              <option value="">所有收藏</option>
              <option v-for="collection in collections" :key="collection" :value="collection">{{ collection }}</option>
            </select>
          </div>

          <!-- Rating Filter -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-text-muted">評分篩選</label>
            <select :value="modelValue.rating" @change="updateFilter('rating', $event.target.value)" class="input w-full text-sm">
              <option value="">所有評分</option>
              <option value="5">⭐⭐⭐⭐⭐ 5星</option>
              <option value="4">⭐⭐⭐⭐ 4星以上</option>
              <option value="3">⭐⭐⭐ 3星以上</option>
              <option value="2">⭐⭐ 2星以上</option>
              <option value="1">⭐ 1星以上</option>
            </select>
          </div>

          <!-- Work Format Filter -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-text-muted">作品形式</label>
            <select :value="modelValue.workFormat" @change="updateFilter('workFormat', $event.target.value)" class="input w-full text-sm">
              <option value="">所有形式</option>
              <option v-for="format in workFormats" :key="format" :value="format">{{ format }}</option>
            </select>
          </div>

          <!-- File Format Filter -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-text-muted">檔案格式</label>
            <select :value="modelValue.fileFormat" @change="updateFilter('fileFormat', $event.target.value)" class="input w-full text-sm">
              <option value="">所有格式</option>
              <option v-for="format in fileFormats" :key="format" :value="format">{{ format }}</option>
            </select>
          </div>

          <!-- Sort By -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-text-muted">排序方式</label>
            <select :value="modelValue.sortBy" @change="updateFilter('sortBy', $event.target.value)" class="input w-full text-sm">
              <option value="title">標題</option>
              <option value="sale_date">發售日期</option>
              <option value="company">公司</option>
              <option value="rating">評分</option>
              <option value="collection">收藏分類</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Fixed Bottom Actions -->
    <div class="flex-shrink-0 border-t border-bg-border bg-bg-secondary/95 backdrop-blur-xl p-4 space-y-2">
      <button
        @click="$emit('clear-filters')"
        class="btn-secondary w-full"
      >
        清除篩選
      </button>
      <button
        @click="$emit('refresh')"
        :disabled="loading"
        class="btn-primary w-full"
      >
        <template v-if="loading">
          <div class="spinner w-4 h-4 mr-2"></div>
          載入中...
        </template>
        <template v-else>
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          重新載入
        </template>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  isVisible: {
    type: Boolean,
    default: true
  },
  isCollapsed: {
    type: Boolean,
    default: false
  },
  companies: {
    type: Array,
    default: () => []
  },
  collections: {
    type: Array,
    default: () => []
  },
  workFormats: {
    type: Array,
    default: () => []
  },
  fileFormats: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:modelValue',
  'toggle-collapse',
  'toggle-visibility',
  'clear-filters',
  'refresh'
])

// Local state for company filter
const companySearchQuery = ref(props.modelValue.company || '')
const showCompanyDropdown = ref(false)

// Computed
const filteredCompanies = computed(() => {
  if (!companySearchQuery.value) return props.companies
  const query = companySearchQuery.value.toLowerCase()
  return props.companies.filter(c => c.toLowerCase().includes(query))
})

// Methods
const updateFilter = (key, value) => {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}

const selectCompany = (company) => {
  companySearchQuery.value = company
  showCompanyDropdown.value = false
  updateFilter('company', company)
}

const hideCompanyDropdown = () => {
  setTimeout(() => {
    showCompanyDropdown.value = false
  }, 200)
}

const filterCompanies = () => {
  showCompanyDropdown.value = true
}

// Watch for external company changes
watch(() => props.modelValue.company, (newCompany) => {
  companySearchQuery.value = newCompany || ''
})
</script>

<style scoped>
/* Custom scrollbar for the filter list */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(59, 130, 246, 0.5);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(59, 130, 246, 0.7);
}
</style>
