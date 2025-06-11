<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-primary via-dark-secondary to-dark-tertiary font-multilingual flex">
    <!-- Left Sidebar - Basic Filters -->
    <aside class="w-80 flex-shrink-0 bg-dark-glass backdrop-blur-25 border-r border-dark-border fixed left-0 top-0 h-full z-30 flex flex-col" 
           :class="{ 'translate-x-0': showSidebar, '-translate-x-full': !showSidebar }"
           style="transition: transform 0.3s ease;">
      <div class="flex-1 overflow-y-auto">
        <div class="p-6 space-y-6">
        <!-- Sidebar Header -->
        <div class="flex items-center justify-between pb-4 border-b border-dark-border">
          <h2 class="text-xl font-bold text-text-primary font-multilingual flex items-center">
            <svg class="w-6 h-6 mr-3 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707v4.172a1 1 0 01-.434.82l-2 1.333A1 1 0 019 19.086v-5.379a1 1 0 00-.293-.707L2.293 6.586A1 1 0 012 5.879V4z" />
            </svg>
            篩選控制台
          </h2>
          <button @click="showSidebar = false" class="lg:hidden text-text-muted hover:text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Search -->
        <div class="space-y-3">
          <label class="block text-sm font-medium text-text-secondary">搜索</label>
          <div class="relative">
            <input
              v-model="searchQuery"
              @input="debounceSearch"
              type="text"
              placeholder="搜索作品、公司、標籤..."
              class="input-field w-full pl-10 pr-8"
            >
            <div class="absolute left-3 top-1/2 transform -translate-y-1/2">
              <svg class="w-4 h-4 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <div v-if="searchQuery" class="absolute right-3 top-1/2 transform -translate-y-1/2">
              <button @click="searchQuery = ''" class="text-text-muted hover:text-text-secondary">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Basic Filters -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-text-primary font-multilingual">基本篩選</h3>
          
          <div class="space-y-3">
            <label class="block text-sm font-medium text-text-secondary">公司</label>
            <div class="relative">
              <input 
                v-model="companySearchQuery"
                @input="filterCompanies"
                @focus="showCompanyDropdown = true"
                @blur="hideCompanyDropdown"
                type="text"
                placeholder="搜索或選擇公司..."
                class="input-field w-full text-sm"
              >
              <div 
                v-if="showCompanyDropdown && filteredCompanies.length > 0" 
                class="absolute top-full left-0 right-0 bg-dark-glass backdrop-blur-md border border-dark-border rounded-lg shadow-xl z-50 max-h-60 overflow-y-auto mt-1"
              >
                <button
                  @mousedown="selectCompany('')"
                  class="w-full text-left px-3 py-2 hover:bg-gray-600 text-text-secondary text-sm border-b border-dark-border"
                >
                  所有公司
                </button>
                <button
                  v-for="company in filteredCompanies"
                  :key="company"
                  @mousedown="selectCompany(company)"
                  class="w-full text-left px-3 py-2 hover:bg-gray-600 text-text-primary text-sm"
                >
                  {{ company }}
                </button>
              </div>
            </div>
          </div>
          
          <div class="space-y-3">
            <label class="block text-sm font-medium text-text-secondary">收藏分類</label>
            <select v-model="selectedCollection" class="input-field w-full text-sm">
              <option value="">所有收藏</option>
              <option v-for="collection in collections" :key="collection" :value="collection">{{ collection }}</option>
            </select>
          </div>
          
          <div class="space-y-3">
            <label class="block text-sm font-medium text-text-secondary">評分篩選</label>
            <select v-model="selectedRating" class="input-field w-full text-sm">
              <option value="">所有評分</option>
              <option value="5">⭐⭐⭐⭐⭐ 5星</option>
              <option value="4">⭐⭐⭐⭐ 4星以上</option>
              <option value="3">⭐⭐⭐ 3星以上</option>
              <option value="2">⭐⭐ 2星以上</option>
              <option value="1">⭐ 1星以上</option>
            </select>
          </div>
          
          <div class="space-y-3">
            <label class="block text-sm font-medium text-text-secondary">作品形式</label>
            <select v-model="selectedWorkFormat" class="input-field w-full text-sm">
              <option value="">所有形式</option>
              <option v-for="format in workFormats" :key="format" :value="format">{{ format }}</option>
            </select>
          </div>
          
          <div class="space-y-3">
            <label class="block text-sm font-medium text-text-secondary">檔案格式</label>
            <select v-model="selectedFileFormat" class="input-field w-full text-sm">
              <option value="">所有格式</option>
              <option v-for="format in fileFormats" :key="format" :value="format">{{ format }}</option>
            </select>
          </div>
          
          <div class="space-y-3">
            <label class="block text-sm font-medium text-text-secondary">排序方式</label>
            <select v-model="sortBy" class="input-field w-full text-sm">
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
      
      <!-- Fixed Filter Actions at Bottom -->
      <div class="flex-shrink-0 border-t border-dark-border bg-dark-glass backdrop-blur-25 p-4">
        <div class="space-y-2">
          <button 
            @click="clearAllFilters" 
            class="w-full px-4 py-2.5 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors duration-200 text-sm font-medium"
          >
            清除篩選
          </button>
          <button 
            @click="refreshData" 
            :disabled="loading"
            class="w-full px-4 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 disabled:cursor-not-allowed text-white rounded-lg transition-colors duration-200 text-sm font-medium flex items-center justify-center"
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
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col" :class="{ 'lg:ml-80': showSidebar }">
      <!-- Header -->
      <header class="glass sticky top-0 z-20 border-b border-dark-border">
        <div class="px-6 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <button 
                @click="showSidebar = !showSidebar"
                class="lg:hidden text-text-muted hover:text-white"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              
              <div class="flex items-center space-x-3">
                <h1 class="text-2xl lg:text-3xl font-bold gradient-text animate-glow-pulse">DLsite 收藏庫</h1>
                <div class="text-sm text-text-muted flex items-center space-x-2">
                  <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                  <span>{{ totalWorks }} 作品</span>
                </div>
              </div>
            </div>
            
            <div class="flex items-center space-x-4">
              <!-- Sidebar Toggle Button for Desktop -->
              <button 
                @click="showSidebar = !showSidebar"
                class="hidden lg:flex btn-secondary items-center space-x-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
                <span>{{ showSidebar ? '隱藏' : '顯示' }}篩選器</span>
              </button>

              <!-- Tag Filter Button -->
              <button
                @click="showTagFilter = !showTagFilter"
                :class="[
                  'btn-secondary flex items-center space-x-2',
                  { 'animate-pulse': tagFilter.selectedTags.length > 0 }
                ]"
                :style="tagFilter.selectedTags.length > 0 ? { backgroundColor: '#B537F2', color: 'white' } : {}"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.99 1.99 0 013 12V7a4 4 0 014-4z" />
                </svg>
                <span>標籤篩選</span>
                <span v-if="tagFilter.selectedTags.length > 0" class="collection-badge text-xs">{{ tagFilter.selectedTags.length }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Advanced Tag Filter Panel -->
        <div v-if="showTagFilter" class="px-6 pb-6 animate-slide-up">
          <TagFilter 
            :all-tags="allTags"
            v-model="tagFilter"
            @apply="applyTagFilter"
            @reset="resetTagFilter"
          />
        </div>
      </header>

      <!-- Main Content -->
      <main class="container mx-auto px-6 py-8">
        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="text-center">
            <div class="spinner-large mx-auto mb-4"></div>
            <p class="text-text-muted text-lg font-multilingual">載入收藏庫中...</p>
          </div>
        </div>

        <!-- Works Grid -->
        <div v-else-if="works.length > 0" class="space-y-8">
          <!-- Stats & Controls -->
          <div class="flex justify-between items-center animate-fade-in">
            <div class="flex items-center space-x-6">
              <p class="text-text-secondary">
                顯示 <span class="text-blue-400 font-semibold">{{ works.length }}</span> 個作品，共 <span class="text-blue-400 font-semibold">{{ totalWorks }}</span> 個
              </p>
              <div v-if="activeFiltersCount > 0 || tagFilter.selectedTags.length > 0" class="flex items-center space-x-2">
                <span class="text-sm text-text-muted">已套用篩選:</span>
                <div class="flex space-x-2">
                  <span v-if="activeFiltersCount > 0" class="tag-selected text-xs px-3 py-1">{{ activeFiltersCount }} 個基本篩選</span>
                  <span v-if="tagFilter.selectedTags.length > 0" class="tag-filter-and text-xs px-3 py-1">{{ tagFilter.selectedTags.length }} 個標籤 ({{ tagFilter.filterMode }})</span>
                </div>
              </div>
            </div>
            
            <div class="flex items-center space-x-3">
              <!-- 每頁顯示數量選擇 -->
              <div class="flex items-center space-x-2">
                <span class="text-sm text-text-muted">每頁:</span>
                <div class="flex bg-dark-glass rounded-lg border border-dark-border overflow-hidden">
                  <button
                    v-for="size in [10, 50, 100]"
                    :key="size"
                    @click="changePageSize(size)"
                    :class="[
                      'px-3 py-2 text-sm font-medium transition-all duration-200',
                      pageSize === size 
                        ? 'text-white' 
                        : 'text-text-muted hover:text-text-secondary hover:bg-gray-700'
                    ]"
                    :style="pageSize === size ? { backgroundColor: '#00D2FF' } : {}"
                  >
                    {{ size }}
                  </button>
                  <div class="flex items-center border-l border-dark-border">
                    <input
                      v-model="customPageSize"
                      @keyup.enter="applyCustomPageSize"
                      @blur="applyCustomPageSize"
                      type="number"
                      min="1"
                      max="500"
                      placeholder="自訂"
                      class="w-16 px-2 py-2 text-sm bg-transparent text-white placeholder-gray-400 focus:outline-none"
                    >
                  </div>
                </div>
              </div>
              
              <div class="flex items-center space-x-2">
                <span class="text-sm text-text-muted">檢視模式:</span>
                <div class="flex bg-dark-glass rounded-full p-1 border border-dark-border">
                  <button
                    @click="viewMode = 'grid'"
                    :class="[
                      'p-2 rounded-full transition-all duration-300 interactive-feedback',
                      viewMode === 'grid' ? 'text-white' : 'text-text-muted hover:text-text-secondary'
                    ]"
                    :style="viewMode === 'grid' ? { backgroundColor: '#00D2FF' } : {}"
                    title="網格檢視"
                  >
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                    </svg>
                  </button>
                  <button
                    @click="viewMode = 'list'"
                    :class="[
                      'p-2 rounded-full transition-all duration-300 interactive-feedback',
                      viewMode === 'list' ? 'text-white' : 'text-text-muted hover:text-text-secondary'
                    ]"
                    :style="viewMode === 'list' ? { backgroundColor: '#00D2FF' } : {}"
                    title="列表檢視"
                  >
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Grid View -->
          <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-3 gap-8">
            <WorkCard 
              v-for="work in works" 
              :key="work.code"
              :work="work"
              @click="openWorkDetail(work)"
              @rating-updated="handleRatingUpdate"
              @collection-updated="handleCollectionUpdate"
              @tag-filter-add="handleTagFilterAdd"
              @company-filter="handleCompanyFilter"
              @show-toast="showToastMessage"
            />
          </div>

          <!-- List View -->
          <div v-else class="space-y-4">
            <WorkListItem 
              v-for="work in works" 
              :key="work.code"
              :work="work"
              @click="openWorkDetail(work)"
              @show-toast="showToastMessage"
            />
          </div>

          <!-- Load More -->
          <div v-if="hasMore" class="text-center mt-12">
            <button 
              @click="loadMore" 
              :disabled="loadingMore"
              class="px-8 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 disabled:cursor-not-allowed text-white rounded-lg transition-colors duration-200 font-medium flex items-center justify-center mx-auto mb-8"
            >
              <template v-if="loadingMore">
                <div class="spinner w-5 h-5 mr-2"></div>
                載入中...
              </template>
              <template v-else>
                載入更多
                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                </svg>
              </template>
            </button>
          </div>
          
          <!-- Infinite Scroll Trigger -->
          <div ref="loadMoreTrigger" class="h-20 flex items-center justify-center">
            <div v-if="loadingMore && isAutoLoading" class="text-center">
              <div class="spinner w-6 h-6 mx-auto mb-2"></div>
              <p class="text-text-muted text-sm">自動載入中...</p>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-20 animate-fade-in">
          <div class="max-w-md mx-auto">
            <svg class="w-32 h-32 mx-auto text-text-muted mb-8 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.469.759-6.173 2.042M12 3c2.21 0 4.21.895 5.657 2.343A7.963 7.963 0 0120 12a7.963 7.963 0 01-2.343 5.657A7.962 7.962 0 0112 20a7.963 7.963 0 01-5.657-2.343A7.962 7.962 0 014 12c0-2.21.895-4.21 2.343-5.657A7.962 7.962 0 0112 3z" />
            </svg>
            <h3 class="text-2xl font-bold text-text-primary mb-4">沒有找到作品</h3>
            <p class="text-text-muted text-lg mb-8">試試調整搜索條件或篩選器</p>
            <div class="space-y-3">
              <button @click="clearAllFilters" class="btn-primary w-full">清除所有篩選</button>
              <button @click="refreshData" class="btn-secondary w-full">重新載入資料</button>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Work Detail Modal -->
    <WorkModal 
      v-if="selectedWork"
      :work="selectedWork"
      @close="closeWorkDetail"
      @tag-filter-add="handleTagFilterAdd"
      @show-toast="showToastMessage"
    />

    <!-- Collection Sidebar -->
    <CollectionSidebar
      :is-open="showCollectionSidebar"
      :selected-collection="collectionFilter"
      @close="showCollectionSidebar = false"
      @open="showCollectionSidebar = true"
      @collection-selected="selectCollection"
      @filter-cleared="clearCollectionFilter"
    />

    <!-- Toast Notification -->
    <div v-if="showToast" class="fixed bottom-6 right-6 z-50 transition-all duration-300">
      <div class="bg-gray-800 border border-gray-600 rounded-lg p-4 shadow-lg max-w-sm">
        <div class="flex items-center space-x-3">
          <div class="spinner w-5 h-5 flex-shrink-0"></div>
          <span class="text-white font-medium">{{ toastMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

// Components
const WorkCard = defineAsyncComponent(() => import('~/components/WorkCard.vue'))
const WorkListItem = defineAsyncComponent(() => import('~/components/WorkListItem.vue'))
const WorkModal = defineAsyncComponent(() => import('~/components/WorkModal.vue'))
const TagFilter = defineAsyncComponent(() => import('~/components/TagFilter.vue'))
const CollectionSidebar = defineAsyncComponent(() => import('~/components/CollectionSidebar.vue'))

// State
const works = ref([])
const companies = ref([])
const collections = ref([])
const allTags = ref([])
const workFormats = ref([])
const fileFormats = ref([])
const loading = ref(false)
const loadingMore = ref(false)
const totalWorks = ref(0)
const currentPage = ref(0)
const pageSize = ref(24) // 增加每頁顯示數量
const customPageSize = ref('')

// Search and filters
const searchQuery = ref('')
const selectedCompany = ref('')
const companySearchQuery = ref('')
const showCompanyDropdown = ref(false)
const filteredCompanies = ref([])
const selectedCollection = ref('')
const selectedRating = ref('')
const selectedWorkFormat = ref('')
const selectedFileFormat = ref('')
const sortBy = ref('title')
const showFilters = ref(false)
const showTagFilter = ref(false)
const showSidebar = ref(true) // 側邊欄顯示狀態
const viewMode = ref('grid')
const selectedWork = ref(null)

// Collection sidebar
const showCollectionSidebar = ref(false)
const collectionFilter = ref(null)

// Toast notifications
const showToast = ref(false)
const toastMessage = ref('')

// Tag filter
const tagFilter = ref({
  selectedTags: [],
  filterMode: 'AND'
})

// Infinite scroll
const loadMoreTrigger = ref(null)
const isAutoLoading = ref(false)

// API URL
const API_BASE = process.client ? 'http://localhost:8001' : 'http://localhost:8001'

// Computed
const activeFiltersCount = computed(() => {
  let count = 0
  if (selectedCompany.value) count++
  if (selectedCollection.value) count++
  if (selectedRating.value) count++
  if (selectedWorkFormat.value) count++
  if (selectedFileFormat.value) count++
  if (searchQuery.value) count++
  return count
})

const hasActiveFilters = computed(() => 
  activeFiltersCount.value > 0 || tagFilter.value.selectedTags.length > 0
)

const hasMore = computed(() => works.value.length < totalWorks.value)

// Methods
const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

// Company filter methods
const filterCompanies = () => {
  if (!companySearchQuery.value) {
    filteredCompanies.value = companies.value
  } else {
    filteredCompanies.value = companies.value.filter(company =>
      company.toLowerCase().includes(companySearchQuery.value.toLowerCase())
    )
  }
}

const selectCompany = (company) => {
  selectedCompany.value = company
  companySearchQuery.value = company
  showCompanyDropdown.value = false
  fetchWorks(true)
}

const hideCompanyDropdown = () => {
  setTimeout(() => {
    showCompanyDropdown.value = false
  }, 200)
}

const fetchWorks = async (reset = false) => {
  try {
    if (reset) {
      console.log('fetchWorks: reset=true, setting loading to true')
      loading.value = true
      loadingMore.value = false
      currentPage.value = 0
    } else {
      console.log('fetchWorks: reset=false, setting loadingMore to true')
      loadingMore.value = true
    }

    const params = new URLSearchParams({
      limit: pageSize.value.toString(),
      offset: (currentPage.value * pageSize.value).toString(),
    })

    if (searchQuery.value) params.append('search', searchQuery.value)
    if (selectedCompany.value) params.append('company', selectedCompany.value)
    if (selectedCollection.value) params.append('collection', selectedCollection.value)
    if (selectedRating.value) params.append('rating', selectedRating.value)
    if (selectedWorkFormat.value) params.append('work_format', selectedWorkFormat.value)
    if (selectedFileFormat.value) params.append('file_format', selectedFileFormat.value)
    if (sortBy.value) params.append('sort', sortBy.value)

    // 添加標籤篩選
    if (tagFilter.value.selectedTags.length > 0) {
      params.append('tags', tagFilter.value.selectedTags.join(','))
      params.append('tag_mode', tagFilter.value.filterMode)
    }

    const response = await fetch(`${API_BASE}/works?${params}`)
    const data = await response.json()

    if (reset) {
      works.value = data.works
      companies.value = data.companies
      filteredCompanies.value = data.companies
      
      // 使用新的智能合併標籤統計
      try {
        const genresResponse = await fetch(`${API_BASE}/genres`)
        const genresData = await genresResponse.json()
        allTags.value = genresData.genres || []
      } catch (error) {
        console.error('Error fetching genre counts:', error)
        // 降級到舊的處理方式
        const tagMap = new Map()
        data.genres.forEach(genre => {
          if (genre && genre.trim()) {
            const normalizedGenre = genre.trim()
            if (tagMap.has(normalizedGenre)) {
              tagMap.set(normalizedGenre, tagMap.get(normalizedGenre) + 1)
            } else {
              tagMap.set(normalizedGenre, 1)
            }
          }
        })
        
        allTags.value = Array.from(tagMap.entries())
          .map(([name, count]) => ({ name, count }))
          .sort((a, b) => b.count - a.count)
      }
    } else {
      works.value.push(...data.works)
    }

    totalWorks.value = data.total
    currentPage.value++

  } catch (error) {
    console.error('Error fetching works:', error)
    showToastMessage('載入資料時發生錯誤')
  } finally {
    console.log('fetchWorks: finally block, setting loading and loadingMore to false')
    loading.value = false
    loadingMore.value = false
  }
}

const fetchCollections = async () => {
  try {
    const response = await fetch(`${API_BASE}/collections`)
    const data = await response.json()
    collections.value = data.collections
  } catch (error) {
    console.error('Error fetching collections:', error)
  }
}

const fetchWorkFormats = async () => {
  try {
    const response = await fetch(`${API_BASE}/work-formats`)
    const data = await response.json()
    workFormats.value = data.work_formats
  } catch (error) {
    console.error('Error fetching work formats:', error)
  }
}

const fetchFileFormats = async () => {
  try {
    const response = await fetch(`${API_BASE}/file-formats`)
    const data = await response.json()
    fileFormats.value = data.file_formats
  } catch (error) {
    console.error('Error fetching file formats:', error)
  }
}

const refreshData = async () => {
  showToastMessage('重新載入資料中...')
  console.log('refreshData: setting loading to true')
  await Promise.all([
    fetchWorks(true),
    fetchCollections(),
    fetchWorkFormats(),
    fetchFileFormats()
  ])
  console.log('refreshData: completed, loading should be false')
}

const loadMore = async () => {
  if (loadingMore.value || !hasMore.value) return
  await fetchWorks(false)
}

// 無限滾動檢測
let scrollObserver = null

const setupInfiniteScroll = () => {
  // 清理舊的 observer
  if (scrollObserver) {
    scrollObserver.disconnect()
    scrollObserver = null
  }
  
  // 等待 DOM 更新
  nextTick(() => {
    if (!loadMoreTrigger.value || !hasMore.value) {
      console.log('InfiniteScroll: 條件不符合，跳過設置', {
        hasTrigger: !!loadMoreTrigger.value,
        hasMore: hasMore.value
      })
      return
    }
    
    scrollObserver = new IntersectionObserver(
      (entries) => {
        const [entry] = entries
        console.log('IntersectionObserver triggered:', {
          isIntersecting: entry.isIntersecting,
          hasMore: hasMore.value,
          loadingMore: loadingMore.value,
          isAutoLoading: isAutoLoading.value,
          loading: loading.value,
          worksCount: works.value.length,
          totalWorks: totalWorks.value
        })
        
        if (entry.isIntersecting && hasMore.value && !loadingMore.value && !isAutoLoading.value && !loading.value) {
          console.log('觸發自動載入更多')
          isAutoLoading.value = true
          loadMore().finally(() => {
            isAutoLoading.value = false
            // 載入完成後重新設置 observer
            setTimeout(() => setupInfiniteScroll(), 100)
          })
        }
      },
      {
        root: null,
        rootMargin: '100px',
        threshold: 0.1
      }
    )
    
    scrollObserver.observe(loadMoreTrigger.value)
    console.log('IntersectionObserver 設置完成')
  })
}

const clearFilters = () => {
  selectedCompany.value = ''
  selectedCollection.value = ''
  selectedRating.value = ''
  selectedWorkFormat.value = ''
  selectedFileFormat.value = ''
  showFilters.value = false
  fetchWorks(true)
}

const clearAllFilters = () => {
  searchQuery.value = ''
  selectedCompany.value = ''
  companySearchQuery.value = ''
  selectedCollection.value = ''
  selectedRating.value = ''
  selectedWorkFormat.value = ''
  selectedFileFormat.value = ''
  tagFilter.value = { selectedTags: [], filterMode: 'AND' }
  showFilters.value = false
  showTagFilter.value = false
  fetchWorks(true)
}

const applyFilters = () => {
  showFilters.value = false
  fetchWorks(true)
}

const applyTagFilter = (filter) => {
  tagFilter.value = filter
  showTagFilter.value = false
  fetchWorks(true)
}

const resetTagFilter = () => {
  tagFilter.value = { selectedTags: [], filterMode: 'OR' }
  fetchWorks(true)
}

const openWorkDetail = async (work) => {
  try {
    showToastMessage('載入作品詳情...')
    const response = await fetch(`${API_BASE}/work/${work.code}`)
    const detailData = await response.json()
    selectedWork.value = detailData
    showToast.value = false
  } catch (error) {
    console.error('Error fetching work detail:', error)
    selectedWork.value = work
    showToastMessage('載入詳情時發生錯誤')
  }
}

const closeWorkDetail = () => {
  selectedWork.value = null
}

const handleRatingUpdate = (data) => {
  // 更新本地資料
  const work = works.value.find(w => w.code === data.code)
  if (work) {
    work.my_rating = data.rating.toString()
  }
  showToastMessage(`評分已更新: ${data.rating} 星`)
}

const handleCollectionUpdate = (data) => {
  // 更新本地資料
  const work = works.value.find(w => w.code === data.code)
  if (work) {
    work.my_collection = data.collection
  }
  
  // 重新載入收藏分類列表
  fetchCollections()
  showToastMessage(`收藏分類已更新: ${data.collection}`)
}

// Debounced search
let searchTimeout
const debounceSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchWorks(true)
  }, 500)
}

// Watch for filter changes
watch([selectedCompany, selectedCollection, selectedRating, selectedWorkFormat, selectedFileFormat, sortBy], () => {
  if (!loading.value) {
    fetchWorks(true)
  }
})

// Watch for tag filter changes
watch(() => tagFilter.value, () => {
  if (!loading.value) {
    fetchWorks(true)
  }
}, { deep: true })

// Collection sidebar methods
const selectCollection = (collectionName) => {
  collectionFilter.value = collectionName
  selectedCollection.value = collectionName
  fetchWorks(true)
  showToastMessage(`已篩選收藏分類: ${collectionName}`)
}

const clearCollectionFilter = () => {
  collectionFilter.value = null
  selectedCollection.value = ''
  fetchWorks(true)
  showToastMessage('已清除收藏篩選')
}

// Page size methods
const changePageSize = (size) => {
  pageSize.value = size
  customPageSize.value = '' // Clear custom input
  fetchWorks(true) // Reset to first page
  showToastMessage(`每頁顯示數量已設為 ${size}`)
}

const applyCustomPageSize = () => {
  const size = parseInt(customPageSize.value)
  if (size && size >= 1 && size <= 500) {
    pageSize.value = size
    fetchWorks(true) // Reset to first page
    showToastMessage(`每頁顯示數量已設為 ${size}`)
  } else if (customPageSize.value !== '') {
    // Invalid input, reset
    customPageSize.value = ''
    showToastMessage('請輸入 1-500 的數字')
  }
}

// 標籤篩選處理
const handleTagFilterAdd = (tagName) => {
  if (!tagFilter.value.selectedTags.includes(tagName)) {
    tagFilter.value.selectedTags.push(tagName)
    showTagFilter.value = true
    fetchWorks(true)
    showToastMessage(`已添加標籤篩選: ${tagName}`)
  } else {
    showToastMessage(`標籤已存在於篩選中: ${tagName}`)
  }
}

// 公司篩選處理
const handleCompanyFilter = (companyName) => {
  selectedCompany.value = companyName
  companySearchQuery.value = companyName
  fetchWorks(true)
  showToastMessage(`已篩選公司: ${companyName}`)
}

// Keyboard shortcuts
const handleKeydown = (event) => {
  if (event.ctrlKey || event.metaKey) {
    switch (event.key) {
      case 'f':
      case 'F':
        event.preventDefault()
        showFilters.value = !showFilters.value
        break
      case 't':
      case 'T':
        event.preventDefault()
        showTagFilter.value = !showTagFilter.value
        break
      case 'r':
      case 'R':
        event.preventDefault()
        refreshData()
        break
    }
  }
  
  if (event.key === 'Escape') {
    if (selectedWork.value) {
      closeWorkDetail()
    } else if (showCollectionSidebar.value) {
      showCollectionSidebar.value = false
    } else if (showFilters.value) {
      showFilters.value = false
    } else if (showTagFilter.value) {
      showTagFilter.value = false
    }
  }
}

// Lifecycle
onMounted(() => {
  Promise.all([
    fetchWorks(true),
    fetchCollections(),
    fetchWorkFormats(),
    fetchFileFormats()
  ]).then(() => {
    // 在資料載入完成後設置無限滾動
    setupInfiniteScroll()
  })
  
  // 添加鍵盤快捷鍵
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  
  // 清理 observer
  if (scrollObserver) {
    scrollObserver.disconnect()
    scrollObserver = null
  }
})

// 當 works 數據變化時重新設置無限滾動
watch(() => works.value.length, (newLength, oldLength) => {
  console.log('Works 數據變化:', { newLength, oldLength, hasMore: hasMore.value })
  if (newLength > 0 && hasMore.value) {
    setTimeout(() => setupInfiniteScroll(), 100)
  }
})

// 監聽 hasMore 變化
watch(() => hasMore.value, (newHasMore) => {
  console.log('HasMore 變化:', { newHasMore, worksLength: works.value.length })
  if (newHasMore && works.value.length > 0) {
    setTimeout(() => setupInfiniteScroll(), 100)
  } else if (!newHasMore && scrollObserver) {
    scrollObserver.disconnect()
    scrollObserver = null
  }
})
</script>