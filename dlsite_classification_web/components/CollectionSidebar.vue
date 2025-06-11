<template>
  <div class="fixed right-0 top-0 h-full z-50 transition-transform duration-300" 
       :class="isOpen ? 'translate-x-0' : 'translate-x-full'">
    <!-- 側邊欄內容 -->
    <div class="w-80 h-full bg-dark-glass backdrop-blur-25 border-l border-dark-border shadow-2xl overflow-hidden">
      <!-- 標題欄 -->
      <div class="p-6 border-b border-dark-border">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
            收藏分類
          </h2>
          <button 
            @click="$emit('close')"
            class="p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-gray-700"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- 收藏統計 -->
      <div class="p-6 border-b border-dark-border">
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-blue-600 bg-opacity-20 rounded-lg p-3 border border-blue-500 border-opacity-30">
            <div class="text-blue-400 text-sm font-medium">總收藏</div>
            <div class="text-white text-xl font-bold">{{ totalCollected }}</div>
          </div>
          <div class="bg-green-600 bg-opacity-20 rounded-lg p-3 border border-green-500 border-opacity-30">
            <div class="text-green-400 text-sm font-medium">分類數</div>
            <div class="text-white text-xl font-bold">{{ collections.length }}</div>
          </div>
        </div>
      </div>

      <!-- 收藏列表 -->
      <div class="flex-1 overflow-y-auto">
        <div class="p-6 space-y-3">
          <div v-if="collections.length === 0" class="text-center py-8">
            <svg class="w-16 h-16 mx-auto text-gray-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
            <p class="text-gray-400">尚無收藏分類</p>
          </div>
          
          <div 
            v-for="collection in collections" 
            :key="collection.name"
            class="group"
          >
            <div 
              class="p-4 rounded-lg border transition-all duration-200 cursor-pointer"
              :class="expandedCollection === collection.name 
                ? 'bg-blue-600 bg-opacity-20 border-blue-500 border-opacity-50 shadow-lg' 
                : 'bg-gray-800 bg-opacity-50 border-gray-600 hover:border-blue-400 hover:bg-gray-700'"
              @click="toggleExpand(collection.name)"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <h3 class="font-medium text-white group-hover:text-blue-300 transition-colors">
                    {{ collection.name }}
                  </h3>
                  <p class="text-sm text-gray-400 mt-1">
                    {{ collection.count }} 個作品
                  </p>
                </div>
                <div class="ml-3">
                  <svg 
                    class="w-5 h-5 transition-transform duration-200"
                    :class="[
                      expandedCollection === collection.name ? 'text-blue-400 rotate-90' : 'text-gray-500 group-hover:text-blue-400',
                      expandedCollection === collection.name ? 'rotate-90' : ''
                    ]"
                    fill="none" stroke="currentColor" viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
              
              <!-- 進度條 -->
              <div class="mt-3">
                <div class="w-full bg-gray-700 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full transition-all duration-500"
                    :class="expandedCollection === collection.name ? 'bg-blue-500' : 'bg-gray-600'"
                    :style="{ width: Math.min(100, (collection.count / maxCollectionCount) * 100) + '%' }"
                  ></div>
                </div>
              </div>
            </div>
            
            <!-- 展開的作品列表 -->
            <div 
              v-if="expandedCollection === collection.name"
              class="mt-2 bg-gray-900 bg-opacity-50 rounded-lg border border-gray-600 overflow-hidden animate-slide-up"
            >
              <div class="p-3">
                <div v-if="loadingWorks" class="text-center py-4">
                  <div class="spinner w-6 h-6 mx-auto mb-2"></div>
                  <p class="text-gray-400 text-sm">載入作品中...</p>
                </div>
                
                <div v-else-if="collectionWorks.length > 0" class="space-y-2">
                  <div 
                    v-for="work in collectionWorks.slice(0, 5)" 
                    :key="work.code"
                    class="flex items-center space-x-3 p-2 bg-gray-800 bg-opacity-50 rounded-lg hover:bg-gray-700 transition-colors"
                  >
                    <img 
                      :src="work.image_url ? `http://localhost:8001${work.image_url}` : 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBmaWxsPSIjMzc0MTUxIi8+CjxwYXRoIGQ9Ik0yMCAyMFYxNUwxNyAxOEwyMCAyMUwyMyAxOEwyMCAxNVoiIGZpbGw9IiM2Qjcy ODAiLz4KPC9zdmc+Cg=='"
                      :alt="work.title"
                      class="w-10 h-10 object-cover rounded-md flex-shrink-0"
                    >
                    <div class="flex-1 min-w-0">
                      <h4 class="text-sm font-medium text-white truncate">{{ work.title }}</h4>
                      <p class="text-xs text-gray-400 truncate">{{ work.code }}</p>
                    </div>
                  </div>
                  
                  <div v-if="collectionWorks.length > 5" class="text-center pt-2">
                    <span class="text-xs text-gray-400">還有 {{ collectionWorks.length - 5 }} 個作品...</span>
                  </div>
                </div>
                
                <div v-else class="text-center py-4">
                  <p class="text-gray-400 text-sm">此分類沒有作品</p>
                </div>
                
                <!-- Apply 按鈕 -->
                <div class="mt-3 pt-3 border-t border-gray-600">
                  <button
                    @click="applyFilter(collection.name)"
                    class="w-full btn-primary py-2 text-sm"
                  >
                    套用此收藏篩選
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部操作 -->
      <div class="p-6 border-t border-dark-border">
        <div class="space-y-3">
          <button
            @click="clearFilter"
            class="w-full btn-secondary py-3 text-center"
            :disabled="!selectedCollection"
          >
            清除篩選
          </button>
          <button
            @click="refreshCollections"
            class="w-full btn-primary py-3 text-center"
            :disabled="loading"
          >
            <span v-if="loading">載入中...</span>
            <span v-else>重新整理</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 背景遮罩 -->
  <div 
    v-if="isOpen"
    class="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300"
    @click="$emit('close')"
  ></div>

  <!-- 開啟按鈕 -->
  <button
    v-if="!isOpen"
    @click="$emit('open')"
    class="fixed right-6 top-1/2 transform -translate-y-1/2 z-45 p-3 bg-green-600 hover:bg-green-500 text-white rounded-l-lg shadow-lg transition-all duration-300 hover:scale-110"
    title="顯示收藏分類"
  >
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
    </svg>
  </button>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  selectedCollection: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['close', 'open', 'collection-selected', 'filter-cleared'])

// State
const collections = ref([])
const loading = ref(false)
const expandedCollection = ref(null)
const collectionWorks = ref([])
const loadingWorks = ref(false)

// Computed
const totalCollected = computed(() => {
  return collections.value.reduce((total, collection) => total + collection.count, 0)
})

const maxCollectionCount = computed(() => {
  return Math.max(...collections.value.map(c => c.count), 1)
})

// Methods
const loadCollections = async () => {
  loading.value = true
  try {
    const response = await fetch('http://localhost:8001/collections')
    const data = await response.json()
    
    if (data.collections && Array.isArray(data.collections)) {
      // Get collection counts by fetching works for each collection
      const collectionData = await Promise.all(
        data.collections.map(async (collectionName) => {
          try {
            const worksResponse = await fetch(`http://localhost:8001/works?collection=${encodeURIComponent(collectionName)}&limit=1`)
            const worksData = await worksResponse.json()
            return {
              name: collectionName,
              count: worksData.total || 0
            }
          } catch (error) {
            console.error(`Error loading collection ${collectionName}:`, error)
            return {
              name: collectionName,
              count: 0
            }
          }
        })
      )
      
      // Sort by count descending
      collections.value = collectionData
        .filter(c => c.count > 0)
        .sort((a, b) => b.count - a.count)
    }
  } catch (error) {
    console.error('Error loading collections:', error)
  } finally {
    loading.value = false
  }
}

const toggleExpand = async (collectionName) => {
  if (expandedCollection.value === collectionName) {
    expandedCollection.value = null
    collectionWorks.value = []
  } else {
    expandedCollection.value = collectionName
    await loadCollectionWorks(collectionName)
  }
}

const loadCollectionWorks = async (collectionName) => {
  loadingWorks.value = true
  try {
    const response = await fetch(`http://localhost:8001/works?collection=${encodeURIComponent(collectionName)}&limit=10`)
    const data = await response.json()
    collectionWorks.value = data.works || []
  } catch (error) {
    console.error('Error loading collection works:', error)
    collectionWorks.value = []
  } finally {
    loadingWorks.value = false
  }
}

const applyFilter = (collectionName) => {
  emit('collection-selected', collectionName)
  expandedCollection.value = null
}

const clearFilter = () => {
  emit('filter-cleared')
  expandedCollection.value = null
}

const refreshCollections = () => {
  loadCollections()
  expandedCollection.value = null
}

// Watchers
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    loadCollections()
  }
})

// Lifecycle
onMounted(() => {
  if (props.isOpen) {
    loadCollections()
  }
})
</script>

<style scoped>
/* Custom scrollbar for the collection list */
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