<template>
  <div 
    class="card-hover cursor-pointer group relative font-multilingual"
@click="handleCardClick"
  >
    <!-- 主圖片容器 -->
    <div class="relative aspect-[4/5] overflow-hidden rounded-t-3xl bg-gray-800">
      <img 
        :src="currentImageUrl" 
        :alt="work.title"
        class="w-full h-full object-contain image-hover transition-all duration-500"
        @error="handleImageError"
      />
      
      <!-- 懸停覆蓋層 -->
      <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-0 group-hover:opacity-90 transition-all duration-500 flex items-end justify-center pb-6">
        <div class="text-center text-white transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
          <svg class="w-10 h-10 mx-auto mb-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          <p class="text-sm font-medium">查看詳情</p>
        </div>
      </div>
      

      <!-- 公司標籤 -->
      <div class="absolute top-3 right-3">
        <button 
          @click.stop="filterByCompany"
          class="px-3 py-1 text-xs font-medium text-white rounded-full border border-gray-600 hover:bg-blue-600 hover:border-blue-500 transition-all duration-200 cursor-pointer" 
          style="background: rgba(20, 20, 30, 0.9); backdrop-filter: blur(10px);"
          title="點擊篩選此公司作品"
        >
          {{ work.company }}
        </button>
      </div>

      <!-- 快速動作按鈕 -->
      <div class="absolute top-1/2 right-3 transform -translate-y-1/2 flex flex-col space-y-2 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-x-4 group-hover:translate-x-0">
        <!-- 評分按鈕 -->
        <button
          @click.stop="toggleRatingEdit"
          class="p-2 rounded-full text-yellow-400 hover:text-white transition-all duration-200 interactive-feedback border border-gray-600"
          style="background: rgba(20, 20, 30, 0.9); backdrop-filter: blur(10px); border-color: rgba(255, 255, 255, 0.1);"
          title="評分"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        </button>

        <!-- 收藏按鈕 -->
        <button
          @click.stop="toggleCollectionEdit"
          class="p-2 rounded-full text-green-400 hover:text-white transition-all duration-200 interactive-feedback border border-gray-600"
          style="background: rgba(20, 20, 30, 0.9); backdrop-filter: blur(10px); border-color: rgba(255, 255, 255, 0.1);"
          title="收藏"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 內容區域 -->
    <div class="p-6 space-y-5">
      <!-- 評分顯示 -->
      <div v-if="currentRating > 0" class="mb-2">
        <div class="inline-flex items-center bg-yellow-500 text-black px-3 py-1 rounded-full text-sm font-bold shadow-lg">
          <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
          {{ currentRating }} 星
        </div>
      </div>
      
      <!-- 標題 -->
      <div class="flex items-start space-x-2 group">
        <h3 class="font-bold text-text-primary text-xl leading-tight line-clamp-2 flex-1">
          {{ work.title }}
        </h3>
        <button
          @click.stop="copyToClipboard(work.title)"
          class="p-1.5 rounded-lg bg-green-500 bg-opacity-20 text-green-400 hover:bg-opacity-30 hover:text-green-300 transition-all duration-200 interactive-feedback opacity-0 group-hover:opacity-100 flex-shrink-0 mt-0.5"
          title="複製作品標題"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </button>
      </div>

      <!-- 代碼與日期 -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <span class="text-blue-400 text-lg font-mono font-bold tracking-wide">{{ work.code }}</span>
          <button
            @click.stop="copyToClipboard(work.code)"
            class="p-1.5 rounded-lg bg-blue-500 bg-opacity-20 text-blue-400 hover:bg-opacity-30 hover:text-blue-300 transition-all duration-200 interactive-feedback"
            title="複製作品代碼"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </button>
        </div>
        <div class="text-xs text-text-muted">
          <span v-if="work.work_format && work.work_format.length > 0" class="font-medium text-purple-400">
            {{ work.work_format[0] }}
          </span>
          <span v-else-if="work.sale_date && formatDate(work.sale_date) !== work.sale_date" class="opacity-75">
            {{ formatDate(work.sale_date) }}
          </span>
          <span v-else class="opacity-50">無格式資訊</span>
        </div>
      </div>
      
      <!-- 收藏資料夾顯示 -->
      <div v-if="currentCollections.length > 0" class="space-y-2">
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="collection in currentCollections.slice(0, 3)" 
            :key="collection"
            class="px-2 py-1 text-xs bg-green-600 text-white rounded-full font-medium shadow-sm"
          >
            <svg class="w-3 h-3 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
            {{ collection }}
          </span>
          <span 
            v-if="currentCollections.length > 3"
            class="px-2 py-1 text-xs bg-gray-600 text-white rounded-full font-medium"
          >
            +{{ currentCollections.length - 3 }}
          </span>
        </div>
      </div>

      <!-- 圖片相簿區域 -->
      <div v-if="allImages.length > 1" class="border-t border-gray-600 pt-4 space-y-4">
        <div class="flex items-center justify-between">
          <h4 class="text-sm font-semibold text-gray-300">圖片相簿</h4>
          <div class="flex items-center space-x-3">
            <span class="text-sm text-gray-400">{{ currentImageIndex + 1 }} / {{ allImages.length }}</span>
            <div class="flex space-x-1">
              <button
                @click.stop="previousImage"
                :disabled="currentImageIndex <= 0"
                class="p-1.5 bg-gray-700 rounded-full text-white hover:bg-gray-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                @click.stop="nextImage"
                :disabled="currentImageIndex >= allImages.length - 1"
                class="p-1.5 bg-gray-700 rounded-full text-white hover:bg-gray-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <!-- 縮圖相簿 -->
        <div class="flex space-x-3 overflow-x-auto pb-2">
          <button
            v-for="(img, index) in allImages"
            :key="index"
            @click.stop="setCurrentImage(index)"
            :class="[
              'flex-shrink-0 w-20 h-16 rounded-xl overflow-hidden border-2 transition-all duration-300 hover:scale-105',
              currentImageIndex === index 
                ? 'border-blue-400 ring-2 ring-blue-400 ring-opacity-50 shadow-lg' 
                : 'border-gray-500 hover:border-blue-300'
            ]"
            :style="currentImageIndex === index ? { boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)' } : {}"
          >
            <img 
              :src="`http://localhost:8001${img}`" 
              :alt="`縮圖 ${index + 1}`"
              class="w-full h-full object-cover"
            />
          </button>
        </div>
      </div>

      <!-- 類型標籤 -->
      <div class="flex flex-wrap gap-2 max-h-20 overflow-y-auto scrollbar-thin">
        <span 
          v-for="genre in work.genre?.slice(0, 8)" 
          :key="genre"
          class="tag text-sm py-1.5 px-3 cursor-pointer hover:scale-105 transition-all duration-200 hover:shadow-lg"
          @click.stop="addToTagFilter(genre)"
          title="點擊加入標籤篩選"
        >
          {{ genre }}
        </span>
        <span v-if="work.genre?.length > 8" class="text-sm text-text-muted self-center">
          +{{ work.genre.length - 8 }}
        </span>
      </div>

      <!-- 作品格式與檔案大小 -->
      <div class="space-y-2">
        <!-- 作品形式 -->
        <div v-if="work.work_format && work.work_format.length > 0" class="space-y-1">
          <div class="text-xs text-text-muted">作品形式:</div>
          <div class="flex flex-wrap gap-1">
            <span 
              v-for="format in work.work_format.slice(0, 3)" 
              :key="format"
              class="px-2 py-1 text-xs rounded-md bg-indigo-600 bg-opacity-20 text-indigo-300 border border-indigo-500 border-opacity-30"
            >
              {{ format }}
            </span>
            <span v-if="work.work_format.length > 3" class="px-2 py-1 text-xs text-text-muted">
              +{{ work.work_format.length - 3 }}
            </span>
          </div>
        </div>
        
        <!-- 檔案大小 -->
        <div v-if="work.file_size && work.file_size.length > 0" class="text-xs text-text-muted">
          <span class="font-medium text-green-400">{{ work.file_size[0] }}</span>
        </div>
      </div>

      <!-- 底部資訊區 -->
      <div class="flex items-center justify-between pt-3 border-t border-gray-600">
        <!-- 評分與收藏快捷操作 -->
        <div class="flex items-center space-x-3">
          <button
            @click.stop="toggleRatingEdit"
            class="text-yellow-400 hover:text-yellow-300 transition-colors p-1"
            title="評分作品"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
          
          <button
            @click.stop="toggleCollectionEdit"
            class="text-green-400 hover:text-green-300 transition-colors p-1"
            title="管理收藏"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </button>
        </div>

        <!-- 圖片數量指示器 -->
        <div v-if="allImages.length > 1" class="flex items-center text-sm text-gray-400">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          {{ allImages.length }}
        </div>
      </div>
    </div>

    <!-- 評分編輯彈出框 -->
    <div v-if="showRatingEdit" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" @click.stop>
      <div class="p-8 rounded-3xl border border-gray-600 text-center space-y-6 mx-4 max-w-md w-full" style="background: rgba(15, 15, 25, 0.98); backdrop-filter: blur(25px);" @click.stop>
        <h4 class="text-xl font-bold text-white">評分作品</h4>
        <div class="flex justify-center space-x-2">
          <button
            v-for="i in 5"
            :key="i"
            @click.stop="setRating(i)"
            :class="[
              'w-10 h-10 transition-all duration-200 hover:scale-110',
              i <= tempRating ? 'text-yellow-400' : 'text-gray-600 hover:text-yellow-300'
            ]"
          >
            <svg fill="currentColor" viewBox="0 0 20 20" class="w-full h-full">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
        </div>
        <div class="flex space-x-4">
          <button @click.stop="saveRating" class="btn-primary px-8 py-3 text-base flex-1">確認</button>
          <button @click.stop="cancelRatingEdit" class="btn-secondary px-8 py-3 text-base flex-1">取消</button>
        </div>
      </div>
    </div>

    <!-- 收藏編輯彈出框 -->
    <div v-if="showCollectionEdit" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" @click.stop>
      <div class="p-8 rounded-3xl border border-gray-600 space-y-6 mx-4 max-w-2xl w-full max-h-[90vh] overflow-y-auto" style="background: rgba(15, 15, 25, 0.98); backdrop-filter: blur(25px);" @click.stop>
        <h4 class="text-xl font-bold text-white text-center">管理收藏夹</h4>
        
        <!-- 新增收藏夹 -->
        <div class="space-y-3">
          <label class="text-sm text-gray-300">新增收藏夹</label>
          <div class="flex space-x-3">
            <input
              v-model="newCollectionName"
              type="text"
              placeholder="輸入收藏夹名稱..."
              class="input-field flex-1 text-base py-3"
              @keyup.enter="addToCollection"
            >
            <button 
              @click.stop="addToCollection" 
              :disabled="!newCollectionName.trim()"
              class="btn-primary px-6 py-3 disabled:opacity-50"
            >
              新增
            </button>
          </div>
        </div>

        <!-- 當前收藏夹 -->
        <div v-if="currentCollections.length > 0" class="space-y-3">
          <label class="text-sm text-gray-300">當前收藏夹</label>
          <div class="space-y-2">
            <div 
              v-for="collection in currentCollections" 
              :key="collection"
              class="flex items-center justify-between bg-blue-600 bg-opacity-20 border border-blue-500 border-opacity-30 text-blue-300 px-4 py-3 rounded-lg shadow-sm backdrop-blur-sm"
            >
              <div class="flex items-center">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
                <span class="font-medium">{{ collection }}</span>
              </div>
              <button 
                @click.stop="removeFromCollection(collection)"
                class="flex items-center justify-center w-6 h-6 hover:bg-red-500 hover:bg-opacity-20 rounded-full transition-colors group"
              >
                <svg class="w-4 h-4 text-red-400 group-hover:text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- 可用收藏夹 -->
        <div v-if="availableCollections.length > 0" class="space-y-3">
          <label class="text-sm text-gray-300">可用收藏夹</label>
          <div class="grid grid-cols-1 gap-2 max-h-32 overflow-y-auto">
            <button
              v-for="collection in availableCollections"
              :key="collection"
              @click.stop="addToCollection(collection)"
              class="flex items-center tag text-sm px-4 py-3 text-left hover:scale-105 transition-transform"
            >
              <svg class="w-3 h-3 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
              {{ collection }}
            </button>
          </div>
        </div>

        <div class="flex space-x-4 pt-4">
          <button @click.stop="saveCollections" class="btn-primary px-8 py-3 text-base flex-1">儲存</button>
          <button @click.stop="cancelCollectionEdit" class="btn-secondary px-8 py-3 text-base flex-1">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  work: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click', 'rating-updated', 'collection-updated', 'tag-filter-add', 'show-toast', 'company-filter'])

// 圖片相關
const imageError = ref(false)
const currentImageIndex = ref(0)

// 評分相關
const showRatingEdit = ref(false)
const tempRating = ref(0)
const currentRating = ref(parseInt(props.work.my_rating) || 0)

// 收藏相關
const showCollectionEdit = ref(false)
const newCollectionName = ref('')
const currentCollections = ref([])
const availableCollections = ref([])

// 初始化收藏數據
const initializeCollections = () => {
  if (props.work.my_collections && Array.isArray(props.work.my_collections)) {
    currentCollections.value = [...props.work.my_collections]
  } else if (props.work.my_collection && typeof props.work.my_collection === 'string') {
    currentCollections.value = [props.work.my_collection]
  } else {
    currentCollections.value = []
  }
}

// 計算所有圖片
const allImages = computed(() => {
  const images = []
  
  // 主圖片
  if (props.work.image_url) {
    images.push(props.work.image_url)
  }
  
  // 範例圖片
  if (props.work.sample_images && props.work.sample_images.length > 0) {
    images.push(...props.work.sample_images)
  }
  
  return images
})

// 當前圖片URL
const currentImageUrl = computed(() => {
  if (imageError.value || allImages.value.length === 0) {
    return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSIjMzc0MTUxIi8+CjxwYXRoIGQ9Ik0xNTAgMjAwVjE1MEwxMjAgMTgwTDE1MCAyMTBMMTgwIDE4MEwxNTAgMTUwWiIgZmlsbD0iIzZCNzI4MCIvPgo8L3N2Zz4K'
  }
  
  const imagePath = allImages.value[currentImageIndex.value]
  return `http://localhost:8001${imagePath}`
})

// 圖片導航方法
const setCurrentImage = (index) => {
  if (index >= 0 && index < allImages.value.length) {
    currentImageIndex.value = index
  }
}

const nextImage = () => {
  setCurrentImage((currentImageIndex.value + 1) % allImages.value.length)
}

const previousImage = () => {
  setCurrentImage((currentImageIndex.value - 1 + allImages.value.length) % allImages.value.length)
}

const handleImageError = () => {
  imageError.value = true
}

// 日期格式化
const formatDate = (dateString) => {
  if (!dateString || dateString.trim() === '') return ''
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) {
      return dateString
    }
    return date.toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return dateString
  }
}

// 卡片點擊處理
const handleCardClick = (event) => {
  // 如果正在編輯評分或收藏，不觸發卡片點擊
  if (showRatingEdit.value || showCollectionEdit.value) {
    return
  }
  
  emit('click')
}

// 評分相關方法
const toggleRatingEdit = () => {
  showRatingEdit.value = !showRatingEdit.value
  tempRating.value = currentRating.value
}

const setRating = (rating) => {
  tempRating.value = rating
}

const saveRating = async () => {
  try {
    const response = await fetch(`http://localhost:8001/work/${props.work.code}/user-data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        rating: tempRating.value.toString()
      })
    })
    
    if (response.ok) {
      currentRating.value = tempRating.value
      showRatingEdit.value = false
      emit('rating-updated', {
        code: props.work.code,
        rating: tempRating.value
      })
    } else {
      console.error('Failed to save rating')
    }
  } catch (error) {
    console.error('Error saving rating:', error)
  }
}

const cancelRatingEdit = () => {
  showRatingEdit.value = false
  tempRating.value = currentRating.value
}

// 收藏相關方法
const toggleCollectionEdit = async () => {
  if (!showCollectionEdit.value) {
    // 載入可用收藏夹
    await loadAvailableCollections()
  }
  showCollectionEdit.value = !showCollectionEdit.value
}

const loadAvailableCollections = async () => {
  try {
    const response = await fetch('http://localhost:8001/collections')
    const data = await response.json()
    const all = data.collections || []
    availableCollections.value = all.filter(c => !currentCollections.value.includes(c))
  } catch (error) {
    console.error('Error loading collections:', error)
    availableCollections.value = []
  }
}

const addToCollection = (collectionName = null) => {
  // Handle the case where event object is passed instead of collection name
  const name = (collectionName && typeof collectionName === 'string') 
    ? collectionName 
    : newCollectionName.value.trim()
    
  if (name && !currentCollections.value.includes(name)) {
    currentCollections.value.push(name)
    if (!collectionName || typeof collectionName !== 'string') {
      newCollectionName.value = ''
    }
    // 更新可用收藏夹列表
    availableCollections.value = availableCollections.value.filter(c => c !== name)
  }
}

const removeFromCollection = (collectionName) => {
  currentCollections.value = currentCollections.value.filter(c => c !== collectionName)
  if (!availableCollections.value.includes(collectionName)) {
    availableCollections.value.push(collectionName)
  }
}

const saveCollections = async () => {
  try {
    const response = await fetch(`http://localhost:8001/work/${props.work.code}/user-data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        collections: currentCollections.value
      })
    })
    
    if (response.ok) {
      showCollectionEdit.value = false
      emit('collection-updated', {
        code: props.work.code,
        collections: currentCollections.value
      })
    } else {
      console.error('Failed to save collections')
    }
  } catch (error) {
    console.error('Error saving collections:', error)
  }
}

const cancelCollectionEdit = () => {
  showCollectionEdit.value = false
  newCollectionName.value = ''
  initializeCollections() // 重置為原始狀態
}

// 標籤篩選方法
const addToTagFilter = (tagName) => {
  emit('tag-filter-add', tagName)
}

// 公司篩選
const filterByCompany = () => {
  emit('company-filter', props.work.company)
}

// 複製到剪貼簿
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    emit('show-toast', `已複製: ${text}`)
  } catch (err) {
    // 降級方案
    const textArea = document.createElement('textarea')
    textArea.value = text
    document.body.appendChild(textArea)
    textArea.focus()
    textArea.select()
    try {
      document.execCommand('copy')
      emit('show-toast', `已複製: ${text}`)
    } catch (fallbackErr) {
      emit('show-toast', '複製失敗')
    }
    document.body.removeChild(textArea)
  }
}

// 圖片輪播自動播放 (可選)
let autoPlayInterval = null

const startAutoPlay = () => {
  if (allImages.value.length > 1) {
    autoPlayInterval = setInterval(() => {
      nextImage()
    }, 3000) // 3秒切換一次
  }
}

const stopAutoPlay = () => {
  if (autoPlayInterval) {
    clearInterval(autoPlayInterval)
    autoPlayInterval = null
  }
}

onMounted(() => {
  // 初始化用戶數據
  currentRating.value = parseInt(props.work.my_rating) || 0
  initializeCollections()
})
</script>

<style scoped>
.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background: rgba(0, 210, 255, 0.5);
  border-radius: 2px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 210, 255, 0.7);
}
</style>