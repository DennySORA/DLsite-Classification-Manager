<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-primary via-dark-secondary to-dark-tertiary font-multilingual">
    <!-- Header -->
    <header class="glass sticky top-0 z-30 border-b border-dark-border">
      <div class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <!-- Back Button and Title -->
          <div class="flex items-center space-x-4">
            <NuxtLink
              to="/"
              class="flex items-center space-x-2 text-text-muted hover:text-white transition-colors group"
            >
              <div class="p-2 rounded-xl bg-dark-glass border border-dark-border group-hover:border-blue-500/50 group-hover:shadow-glow-blue transition-all">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
              </div>
              <span class="hidden sm:inline font-medium">返回收藏庫</span>
            </NuxtLink>

            <div class="h-8 w-px bg-dark-border"></div>

            <div class="flex items-center space-x-3">
              <div class="relative">
                <div class="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl blur-lg opacity-30"></div>
                <div class="relative p-3 rounded-xl bg-dark-glass border border-dark-border">
                  <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
              </div>
              <div>
                <h1 class="text-xl lg:text-2xl font-bold gradient-text">{{ displayCompanyName }}</h1>
                <p class="text-sm text-text-muted" v-if="totalWorks > 0">
                  共 <span class="text-blue-400 font-semibold">{{ totalWorks }}</span> 個作品
                </p>
              </div>
            </div>
          </div>

          <!-- Controls -->
          <div class="flex items-center space-x-3">
            <!-- View Mode Toggle -->
            <div class="hidden sm:flex items-center space-x-2">
              <span class="text-sm text-text-muted">檢視:</span>
              <div class="flex bg-dark-glass rounded-full p-1 border border-dark-border">
                <button
                  @click="viewMode = 'grid'"
                  :class="[
                    'p-2 rounded-full transition-all duration-300',
                    viewMode === 'grid' ? 'text-white bg-blue-500' : 'text-text-muted hover:text-white'
                  ]"
                  title="網格檢視"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                  </svg>
                </button>
                <button
                  @click="viewMode = 'list'"
                  :class="[
                    'p-2 rounded-full transition-all duration-300',
                    viewMode === 'list' ? 'text-white bg-blue-500' : 'text-text-muted hover:text-white'
                  ]"
                  title="列表檢視"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Sort -->
            <select v-model="sortBy" class="input-field text-sm py-2 px-3 min-w-[120px]">
              <option value="title">標題</option>
              <option value="sale_date">發售日期</option>
              <option value="rating">評分</option>
            </select>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-6 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="text-center">
          <div class="spinner-large mx-auto mb-4"></div>
          <p class="text-text-muted text-lg">載入公司作品中...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-20 animate-fade-in">
        <div class="max-w-md mx-auto">
          <div class="w-24 h-24 mx-auto mb-6 rounded-full bg-red-500/20 flex items-center justify-center">
            <svg class="w-12 h-12 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-text-primary mb-4">載入失敗</h3>
          <p class="text-text-muted text-lg mb-8">{{ error }}</p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button @click="fetchWorks(true)" class="btn-primary">重試</button>
            <NuxtLink to="/" class="btn-secondary">返回首頁</NuxtLink>
          </div>
        </div>
      </div>

      <!-- Works Grid -->
      <div v-else-if="works.length > 0" class="space-y-8">
        <!-- Stats Bar -->
        <div class="flex flex-wrap justify-between items-center gap-4 animate-fade-in">
          <p class="text-text-secondary">
            顯示 <span class="text-blue-400 font-semibold">{{ works.length }}</span> 個作品
          </p>

          <!-- Page Size Controls -->
          <div class="flex items-center space-x-2">
            <span class="text-sm text-text-muted">每頁:</span>
            <div class="flex bg-dark-glass rounded-lg border border-dark-border overflow-hidden">
              <button
                v-for="size in [12, 24, 48]"
                :key="size"
                @click="changePageSize(size)"
                :class="[
                  'px-3 py-1.5 text-sm font-medium transition-all',
                  pageSize === size
                    ? 'text-white bg-blue-500'
                    : 'text-text-muted hover:text-white hover:bg-gray-700'
                ]"
              >
                {{ size }}
              </button>
            </div>
          </div>
        </div>

        <!-- Grid View -->
        <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-6">
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
            class="btn-primary px-8 py-3"
          >
            <template v-if="loadingMore">
              <div class="spinner w-5 h-5 mr-2 inline-block"></div>
              載入中...
            </template>
            <template v-else>
              載入更多
              <svg class="w-5 h-5 ml-2 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            </template>
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-20 animate-fade-in">
        <div class="max-w-md mx-auto">
          <div class="w-24 h-24 mx-auto mb-6 rounded-full bg-gray-800 flex items-center justify-center">
            <svg class="w-12 h-12 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-text-primary mb-4">此公司沒有作品</h3>
          <p class="text-text-muted text-lg mb-8">該公司目前沒有收藏的作品</p>
          <NuxtLink to="/" class="btn-primary">返回收藏庫</NuxtLink>
        </div>
      </div>
    </main>

    <!-- Work Detail Modal -->
    <WorkModal
      v-if="selectedWork"
      :work="selectedWork"
      @close="closeWorkDetail"
      @tag-filter-add="handleTagFilterAdd"
      @show-toast="showToastMessage"
    />

    <!-- Toast Notification -->
    <div v-if="showToast" class="fixed bottom-6 right-6 z-50 animate-slide-up">
      <div class="bg-dark-glass backdrop-blur-25 border border-dark-border rounded-xl p-4 shadow-2xl max-w-sm">
        <div class="flex items-center space-x-3">
          <div class="flex-shrink-0">
            <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <span class="text-white font-medium">{{ toastMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// Components
const WorkCard = defineAsyncComponent(() => import('~/components/WorkCard.vue'))
const WorkListItem = defineAsyncComponent(() => import('~/components/WorkListItem.vue'))
const WorkModal = defineAsyncComponent(() => import('~/components/WorkModal.vue'))

// Route
const route = useRoute()
const router = useRouter()

// State
const works = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const error = ref(null)
const totalWorks = ref(0)
const currentPage = ref(0)
const pageSize = ref(24)
const sortBy = ref('title')
const viewMode = ref('grid')
const selectedWork = ref(null)

// Toast
const showToast = ref(false)
const toastMessage = ref('')

// API Base URL
const API_BASE = 'http://localhost:8001'

// Computed
const companyName = computed(() => {
  // Decode URL-encoded company name
  return decodeURIComponent(route.params.name || '')
})

const displayCompanyName = computed(() => {
  return companyName.value || '未知公司'
})

const hasMore = computed(() => works.value.length < totalWorks.value)

// Methods
const fetchWorks = async (reset = false) => {
  try {
    if (reset) {
      loading.value = true
      error.value = null
      currentPage.value = 0
    } else {
      loadingMore.value = true
    }

    const params = new URLSearchParams({
      company: companyName.value,
      limit: pageSize.value.toString(),
      offset: (currentPage.value * pageSize.value).toString(),
      sort: sortBy.value,
    })

    const response = await fetch(`${API_BASE}/works?${params}`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    if (reset) {
      works.value = data.works
    } else {
      works.value.push(...data.works)
    }

    totalWorks.value = data.total
    currentPage.value++

  } catch (e) {
    console.error('Error fetching company works:', e)
    error.value = '無法載入公司作品，請稍後再試'
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const loadMore = async () => {
  if (loadingMore.value || !hasMore.value) return
  await fetchWorks(false)
}

const changePageSize = (size) => {
  pageSize.value = size
  fetchWorks(true)
}

const openWorkDetail = async (work) => {
  try {
    showToastMessage('載入作品詳情...')
    const response = await fetch(`${API_BASE}/work/${work.code}`)
    const detailData = await response.json()
    selectedWork.value = detailData
    showToast.value = false
  } catch (e) {
    console.error('Error fetching work detail:', e)
    selectedWork.value = work
    showToastMessage('載入詳情時發生錯誤')
  }
}

const closeWorkDetail = () => {
  selectedWork.value = null
}

const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const handleRatingUpdate = (data) => {
  const work = works.value.find(w => w.code === data.code)
  if (work) {
    work.my_rating = data.rating.toString()
  }
  showToastMessage(`評分已更新: ${data.rating} 星`)
}

const handleCollectionUpdate = (data) => {
  const work = works.value.find(w => w.code === data.code)
  if (work) {
    work.my_collection = data.collection
  }
  showToastMessage(`收藏分類已更新`)
}

const handleTagFilterAdd = (tagName) => {
  showToastMessage(`請返回首頁使用標籤篩選: ${tagName}`)
}

const handleCompanyFilter = (companyName) => {
  // Navigate to the company page
  router.push(`/company/${encodeURIComponent(companyName)}`)
}

// Watch sort changes
watch(sortBy, () => {
  fetchWorks(true)
})

// On mount
onMounted(() => {
  if (companyName.value) {
    fetchWorks(true)
  } else {
    error.value = '未指定公司名稱'
    loading.value = false
  }
})
</script>

<style scoped>
/* Page-specific animations */
.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
