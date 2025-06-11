<template>
  <div 
    class="fixed inset-0 z-50 overflow-y-auto font-multilingual"
    @click="handleBackdropClick"
    @keydown.esc="$emit('close')"
    tabindex="-1"
  >
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black bg-opacity-80 backdrop-blur-sm transition-all duration-500"></div>
    
    <!-- Modal -->
    <div 
      class="flex min-h-full items-center justify-center p-4"
      @click="handleBackdropClick"
    >
      <div 
        ref="modalContent"
        class="relative bg-dark-glass backdrop-blur-25 rounded-3xl max-w-5xl w-full max-h-[95vh] overflow-hidden border border-dark-border shadow-card-hover transition-all duration-500 ease-out transform scale-100 animate-scale-in"
      >
        <!-- Close Button -->
        <button 
          @click="$emit('close')"
          class="absolute top-6 right-6 z-20 p-3 bg-dark-glass backdrop-blur-15 rounded-full text-text-secondary hover:text-white transition-all duration-300 interactive-feedback border border-dark-border"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <div class="overflow-y-auto max-h-[90vh]">
          <!-- Header Section -->
          <div class="relative">
            <!-- Background Image -->
            <div class="h-64 overflow-hidden">
              <img 
                :src="mainImageUrl" 
                :alt="work.title"
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent"></div>
            </div>

            <!-- Title Overlay -->
            <div class="absolute bottom-0 left-0 right-0 p-6">
              <div class="flex items-end space-x-4">
                <div class="flex-1">
                  <div class="flex items-start space-x-3 mb-2">
                    <h1 class="text-3xl font-bold text-white flex-1">{{ work.title }}</h1>
                    <button
                      @click="copyToClipboard(work.title)"
                      class="p-2 rounded-lg bg-green-500 bg-opacity-20 text-green-400 hover:bg-opacity-30 hover:text-green-300 transition-all duration-200 flex-shrink-0"
                      title="複製作品標題"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                    </button>
                  </div>
                  <div class="flex items-center space-x-4 text-sm text-gray-300">
                    <div class="flex items-center space-x-2">
                      <span class="font-mono text-blue-400 text-lg font-bold tracking-wide">{{ work.code }}</span>
                      <button
                        @click="copyToClipboard(work.code)"
                        class="p-1.5 rounded-lg bg-blue-500 bg-opacity-20 text-blue-400 hover:bg-opacity-30 hover:text-blue-300 transition-all duration-200"
                        title="複製作品代碼"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                      </button>
                    </div>
                    <span>{{ work.company }}</span>
                    <span v-if="formatDate(work.sale_date)">{{ formatDate(work.sale_date) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Content Section -->
          <div class="p-6">
            <!-- 類型標籤 -->
            <div v-if="work.genre && work.genre.length > 0" class="mb-6">
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="genre in work.genre" 
                  :key="genre"
                  class="tag cursor-pointer hover:scale-105 transition-all duration-200 hover:shadow-lg"
                  @click="addToTagFilter(genre)"
                  title="點擊加入標籤篩選"
                >
                  {{ genre }}
                </span>
              </div>
            </div>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <!-- Main Content -->
              <div class="lg:col-span-2 space-y-6">
                <!-- Sample Images -->
                <div v-if="work.sample_images && work.sample_images.length > 0">
                  <h3 class="text-xl font-bold text-white mb-3">範例圖片</h3>
                  <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                    <div 
                      v-for="(image, index) in work.sample_images" 
                      :key="index"
                      class="relative aspect-square overflow-hidden rounded-lg cursor-pointer group"
                      @click="openImageViewer(image, index)"
                    >
                      <img 
                        :src="`http://localhost:8001${image}`" 
                        :alt="`範例圖片 ${index + 1}`"
                        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                      />
                      <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center">
                        <svg class="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Description -->
                <div v-if="work.introduction">
                  <h3 class="text-xl font-bold text-white mb-3">作品介紹</h3>
                  <div class="text-gray-300 leading-relaxed whitespace-pre-line">
                    {{ work.introduction }}
                  </div>
                </div>
              </div>

              <!-- Sidebar -->
              <div class="space-y-6">
                <!-- 我的評分與收藏 -->
                <div class="bg-gray-800 rounded-lg p-4">
                  <h3 class="text-lg font-bold text-white mb-3">我的評分與收藏</h3>
                  <div class="space-y-4">
                    <!-- 評分顯示與編輯 -->
                    <div>
                      <div class="flex items-center justify-between mb-2">
                        <span class="text-gray-400 text-sm">我的評分:</span>
                        <button
                          @click="toggleRatingEdit"
                          class="text-yellow-400 hover:text-yellow-300 transition-colors p-1"
                          title="編輯評分"
                        >
                          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                          </svg>
                        </button>
                      </div>
                      <div v-if="!showRatingEdit" class="flex items-center space-x-2">
                        <div v-if="currentRating > 0" class="flex">
                          <svg v-for="i in 5" :key="i" class="w-5 h-5" :class="i <= currentRating ? 'text-yellow-400' : 'text-gray-600'" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                          <span class="text-white ml-2">{{ currentRating }}/5</span>
                        </div>
                        <span v-else class="text-gray-500 text-sm">未評分</span>
                      </div>
                      <div v-else class="space-y-3">
                        <div class="flex justify-center space-x-1">
                          <button
                            v-for="i in 5"
                            :key="i"
                            @click="setRating(i)"
                            :class="[
                              'w-8 h-8 transition-all duration-200 hover:scale-110',
                              i <= tempRating ? 'text-yellow-400' : 'text-gray-600 hover:text-yellow-300'
                            ]"
                          >
                            <svg fill="currentColor" viewBox="0 0 20 20" class="w-full h-full">
                              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                          </button>
                        </div>
                        <div class="flex space-x-2">
                          <button @click="saveRating" class="btn-primary px-4 py-2 text-sm flex-1">確認</button>
                          <button @click="cancelRatingEdit" class="btn-secondary px-4 py-2 text-sm flex-1">取消</button>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 收藏顯示與編輯 -->
                    <div>
                      <div class="flex items-center justify-between mb-2">
                        <span class="text-gray-400 text-sm">我的收藏:</span>
                        <button
                          @click="toggleCollectionEdit"
                          class="text-green-400 hover:text-green-300 transition-colors p-1"
                          title="編輯收藏"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                      </div>
                      <div v-if="!showCollectionEdit">
                        <div v-if="currentCollections.length > 0" class="flex flex-wrap gap-1">
                          <span 
                            v-for="collection in currentCollections" 
                            :key="collection"
                            class="inline-flex items-center px-2 py-1 text-xs bg-green-600 text-white rounded-full font-medium shadow-sm"
                          >
                            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                            </svg>
                            {{ collection }}
                          </span>
                        </div>
                        <span v-else class="text-gray-500 text-sm">未收藏</span>
                      </div>
                      <div v-else class="space-y-3">
                        <!-- 新增收藏夹 -->
                        <div class="space-y-2">
                          <input
                            v-model="newCollectionName"
                            type="text"
                            placeholder="新增收藏夹..."
                            class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm focus:outline-none focus:border-blue-400"
                            @keyup.enter="addToCollection"
                          >
                          <button 
                            @click="addToCollection" 
                            :disabled="!newCollectionName.trim()"
                            class="w-full btn-primary py-2 text-sm disabled:opacity-50"
                          >
                            新增
                          </button>
                        </div>
                        
                        <!-- 當前收藏夹 -->
                        <div v-if="currentCollections.length > 0" class="space-y-2">
                          <div class="text-xs text-gray-400">當前收藏:</div>
                          <div class="space-y-2">
                            <div 
                              v-for="collection in currentCollections" 
                              :key="collection"
                              class="flex items-center justify-between bg-blue-600 bg-opacity-20 border border-blue-500 border-opacity-30 text-blue-300 px-3 py-2 rounded-lg shadow-sm backdrop-blur-sm"
                            >
                              <div class="flex items-center">
                                <svg class="w-3 h-3 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                                </svg>
                                <span class="text-sm font-medium">{{ collection }}</span>
                              </div>
                              <button 
                                @click="removeFromCollection(collection)"
                                class="flex items-center justify-center w-5 h-5 hover:bg-red-500 hover:bg-opacity-20 rounded-full transition-colors group"
                              >
                                <svg class="w-3 h-3 text-red-400 group-hover:text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                              </button>
                            </div>
                          </div>
                        </div>
                        
                        <!-- 可用收藏夹 -->
                        <div v-if="availableCollections.length > 0" class="space-y-2">
                          <div class="text-xs text-gray-400">可用收藏:</div>
                          <div class="grid grid-cols-1 gap-2 max-h-40 overflow-y-auto">
                            <button
                              v-for="collection in availableCollections"
                              :key="collection"
                              @click="addToCollection(collection)"
                              class="flex items-center text-left px-3 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm transition-colors"
                            >
                              <svg class="w-3 h-3 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                              </svg>
                              {{ collection }}
                            </button>
                          </div>
                        </div>
                        
                        <div class="flex space-x-2 pt-2">
                          <button @click="saveCollections" class="btn-primary px-4 py-2 text-sm flex-1">儲存</button>
                          <button @click="cancelCollectionEdit" class="btn-secondary px-4 py-2 text-sm flex-1">取消</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Basic Info -->
                <div class="bg-gray-800 rounded-lg p-4">
                  <h3 class="text-lg font-bold text-white mb-3">基本資訊</h3>
                  <div class="space-y-2 text-sm">
                    <div v-if="work.work_format && work.work_format.length > 0">
                      <span class="text-gray-400">作品形式:</span>
                      <span class="text-white ml-2">{{ work.work_format.join(', ') }}</span>
                    </div>
                    
                    <div v-if="work.file_size && work.file_size.length > 0">
                      <span class="text-gray-400">檔案大小:</span>
                      <span class="text-white ml-2">{{ work.file_size.join(', ') }}</span>
                    </div>

                    <div v-if="work.series && work.series.length > 0">
                      <span class="text-gray-400">系列:</span>
                      <span class="text-white ml-2">{{ work.series.join(', ') }}</span>
                    </div>

                    <div v-if="work.file_format && work.file_format.length > 0">
                      <span class="text-gray-400">檔案格式:</span>
                      <span class="text-white ml-2">{{ work.file_format.join(', ') }}</span>
                    </div>

                    <div v-if="work.operating_environment && work.operating_environment.length > 0">
                      <span class="text-gray-400">動作環境:</span>
                      <span class="text-white ml-2">{{ work.operating_environment.join(', ') }}</span>
                    </div>

                    <div v-if="work.languages && work.languages.length > 0">
                      <span class="text-gray-400">對應語言:</span>
                      <span class="text-white ml-2">{{ work.languages.join(', ') }}</span>
                    </div>
                  </div>
                </div>

                <!-- Staff Info -->
                <div v-if="hasStaffInfo" class="bg-gray-800 rounded-lg p-4">
                  <h3 class="text-lg font-bold text-white mb-3">製作資訊</h3>
                  <div class="space-y-2 text-sm">
                    <div v-if="work.author && work.author.length > 0">
                      <span class="text-gray-400">作者:</span>
                      <span class="text-white ml-2">{{ work.author.join(', ') }}</span>
                    </div>

                    <div v-if="work.illustration && work.illustration.length > 0">
                      <span class="text-gray-400">插畫:</span>
                      <span class="text-white ml-2">{{ work.illustration.join(', ') }}</span>
                    </div>

                    <div v-if="work.scenario && work.scenario.length > 0">
                      <span class="text-gray-400">劇本:</span>
                      <span class="text-white ml-2">{{ work.scenario.join(', ') }}</span>
                    </div>

                    <div v-if="work.voice_actor && work.voice_actor.length > 0">
                      <span class="text-gray-400">聲優:</span>
                      <span class="text-white ml-2">{{ work.voice_actor.join(', ') }}</span>
                    </div>

                    <div v-if="work.music && work.music.length > 0">
                      <span class="text-gray-400">音樂:</span>
                      <span class="text-white ml-2">{{ work.music.join(', ') }}</span>
                    </div>
                  </div>
                </div>

                <!-- Rating -->
                <div v-if="work.star" class="bg-gray-800 rounded-lg p-4">
                  <h3 class="text-lg font-bold text-white mb-3">評分</h3>
                  <div class="flex items-center space-x-2">
                    <div class="flex">
                      <svg v-for="i in 5" :key="i" class="w-5 h-5" :class="i <= work.star[0] ? 'text-yellow-400' : 'text-gray-600'" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    </div>
                    <span class="text-white">{{ work.star[0] }}/5</span>
                    <span v-if="work.star[1]" class="text-gray-400 text-sm">({{ work.star[1] }})</span>
                  </div>
                </div>

                <!-- Additional Info -->
                <div v-if="work.update_date && work.update_date.length > 0" class="bg-gray-800 rounded-lg p-4">
                  <h3 class="text-lg font-bold text-white mb-3">更新資訊</h3>
                  <div class="text-sm text-gray-300">
                    {{ work.update_date.join('\n') }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Image Viewer Modal -->
    <div v-if="imageViewerOpen" class="fixed inset-0 z-60 bg-black bg-opacity-95 flex items-center justify-center" @click.stop="closeImageViewer">
      <!-- 主圖片 -->
      <img 
        :src="`http://localhost:8001${currentImage}`" 
        class="max-w-[90vw] max-h-[90vh] object-contain" 
        @click.stop
      />
      
      <!-- 關閉按鈕 -->
      <button 
        @click.stop="closeImageViewer" 
        class="absolute top-4 right-4 p-3 bg-black bg-opacity-50 rounded-full text-white hover:bg-opacity-75 transition-all"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
      
      <!-- 左右導航 -->
      <div v-if="work.sample_images && work.sample_images.length > 1" class="absolute inset-0 flex items-center justify-between px-4 pointer-events-none">
        <button 
          v-if="currentImageIndex > 0"
          @click.stop="previousImageInViewer"
          class="p-3 bg-black bg-opacity-50 rounded-full text-white hover:bg-opacity-75 transition-all pointer-events-auto"
        >
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <button 
          v-if="currentImageIndex < work.sample_images.length - 1"
          @click.stop="nextImageInViewer"
          class="p-3 bg-black bg-opacity-50 rounded-full text-white hover:bg-opacity-75 transition-all pointer-events-auto"
        >
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
      
      <!-- 圖片計數 -->
      <div v-if="work.sample_images && work.sample_images.length > 1" class="absolute bottom-4 left-1/2 transform -translate-x-1/2">
        <div class="bg-black bg-opacity-50 text-white px-4 py-2 rounded-full text-sm">
          {{ currentImageIndex + 1 }} / {{ work.sample_images.length }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  work: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'tag-filter-add', 'show-toast'])

// Modal interaction
const modalContent = ref(null)
const imageError = ref(false)
const imageViewerOpen = ref(false)
const currentImage = ref('')
const currentImageIndex = ref(0)

// User interactions
const showRatingEdit = ref(false)
const showCollectionEdit = ref(false)
const tempRating = ref(0)
const newCollectionName = ref('')
const currentRating = ref(parseInt(props.work.my_rating) || 0)
const currentCollections = ref([])
const availableCollections = ref([])

// Initialize collections data
const initializeCollections = () => {
  if (props.work.my_collections && Array.isArray(props.work.my_collections)) {
    currentCollections.value = [...props.work.my_collections]
  } else if (props.work.my_collection && typeof props.work.my_collection === 'string') {
    currentCollections.value = [props.work.my_collection]
  } else {
    currentCollections.value = []
  }
}

const mainImageUrl = computed(() => {
  if (imageError.value) {
    return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDgwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI4MDAiIGhlaWdodD0iNDAwIiBmaWxsPSIjMzc0MTUxIi8+CjxwYXRoIGQ9Ik00MDAgMjAwVjE1MEwzNzAgMTgwTDQwMCAyMTBMNDMwIDE4MEw0MDAgMTUwWiIgZmlsbD0iIzZCNzI4MCIvPgo8L3N2Zz4K'
  }
  return props.work.image_url ? `http://localhost:8001${props.work.image_url}` : 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDgwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI4MDAiIGhlaWdodD0iNDAwIiBmaWxsPSIjMzc0MTUxIi8+CjxwYXRoIGQ9Ik00MDAgMjAwVjE1MEwzNzAgMTgwTDQwMCAyMTBMNDMwIDE4MEw0MDAgMTUwWiIgZmlsbD0iIzZCNzI4MCIvPgo8L3N2Zz4K'
})

const hasStaffInfo = computed(() => {
  return (props.work.author && props.work.author.length > 0) ||
         (props.work.illustration && props.work.illustration.length > 0) ||
         (props.work.scenario && props.work.scenario.length > 0) ||
         (props.work.voice_actor && props.work.voice_actor.length > 0) ||
         (props.work.music && props.work.music.length > 0)
})

// Modal interaction methods
const handleBackdropClick = (event) => {
  // Close if clicking on backdrop or modal container, but not on modal content
  if (event.target === event.currentTarget || !modalContent.value?.contains(event.target)) {
    emit('close')
  }
}

const handleImageError = () => {
  imageError.value = true
}

const formatDate = (dateString) => {
  if (!dateString || dateString.trim() === '') return ''
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) {
      return ''
    }
    return date.toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch {
    return ''
  }
}

const openImageViewer = (image, index = 0) => {
  currentImage.value = image
  currentImageIndex.value = index
  imageViewerOpen.value = true
}

const closeImageViewer = () => {
  imageViewerOpen.value = false
  currentImage.value = ''
  currentImageIndex.value = 0
}

const previousImageInViewer = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
    currentImage.value = props.work.sample_images[currentImageIndex.value]
  }
}

const nextImageInViewer = () => {
  if (currentImageIndex.value < props.work.sample_images.length - 1) {
    currentImageIndex.value++
    currentImage.value = props.work.sample_images[currentImageIndex.value]
  }
}

// Rating methods
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

// Collection methods
const toggleCollectionEdit = async () => {
  if (!showCollectionEdit.value) {
    // Load available collections when opening
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
    // Update available collections list
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
  initializeCollections() // Reset to original state
}

// Keyboard event handling
const handleKeydown = (event) => {
  if (event.key === 'Escape') {
    event.preventDefault()
    event.stopPropagation()
    if (imageViewerOpen.value) {
      closeImageViewer()
    } else if (showRatingEdit.value) {
      cancelRatingEdit()
    } else if (showCollectionEdit.value) {
      cancelCollectionEdit()
    } else {
      emit('close')
    }
  } else if (imageViewerOpen.value) {
    // 在圖片查看器中的鍵盤控制
    if (event.key === 'ArrowLeft') {
      event.preventDefault()
      previousImageInViewer()
    } else if (event.key === 'ArrowRight') {
      event.preventDefault()
      nextImageInViewer()
    }
  }
}

// 標籤篩選方法
const addToTagFilter = (tagName) => {
  emit('tag-filter-add', tagName)
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

// Lifecycle
onMounted(() => {
  // Initialize user data
  currentRating.value = parseInt(props.work.my_rating) || 0
  initializeCollections()
  
  // 阻止body滾動
  document.body.style.overflow = 'hidden'
  
  // Add keyboard listener
  document.addEventListener('keydown', handleKeydown)
  
  // Focus on modal for accessibility
  if (modalContent.value) {
    modalContent.value.focus()
  }
})

onUnmounted(() => {
  // 恢復body滾動
  document.body.style.overflow = ''
  
  document.removeEventListener('keydown', handleKeydown)
})
</script>