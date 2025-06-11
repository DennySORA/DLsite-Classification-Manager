<template>
  <div 
    class="bg-gray-800 rounded-lg p-4 card-hover cursor-pointer group flex items-center space-x-4"
    @click="$emit('click')"
  >
    <!-- Thumbnail -->
    <div class="flex-shrink-0">
      <div class="relative w-20 h-28 overflow-hidden rounded">
        <img 
          :src="imageUrl" 
          :alt="work.title"
          class="w-full h-full object-cover image-hover"
          @error="handleImageError"
        />
        <div v-if="work.age_rating && work.age_rating.length > 0" class="absolute top-1 left-1">
          <span class="px-1 py-0.5 text-xs font-bold bg-red-600 text-white rounded">
            {{ work.age_rating[0] }}
          </span>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="flex-1 min-w-0">
      <div class="flex items-start justify-between">
        <div class="flex-1 min-w-0">
          <!-- Title and Code -->
          <div class="flex items-center space-x-3 mb-1">
            <div class="flex items-center space-x-2 group flex-1 min-w-0">
              <h3 class="font-bold text-white text-lg truncate flex-1">
                {{ work.title }}
              </h3>
              <button
                @click.stop="copyToClipboard(work.title)"
                class="p-1 rounded bg-green-500 bg-opacity-20 text-green-400 hover:bg-opacity-30 hover:text-green-300 transition-all duration-200 opacity-0 group-hover:opacity-100 flex-shrink-0"
                title="複製作品標題"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </button>
            </div>
            <div class="flex items-center space-x-2">
              <span class="text-blue-400 text-sm font-mono flex-shrink-0">{{ work.code }}</span>
              <button
                @click.stop="copyToClipboard(work.code)"
                class="p-1 rounded bg-blue-500 bg-opacity-20 text-blue-400 hover:bg-opacity-30 hover:text-blue-300 transition-all duration-200 opacity-0 group-hover:opacity-100"
                title="複製作品代碼"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Company and Date -->
          <div class="flex items-center space-x-4 text-sm text-gray-400 mb-2">
            <span>{{ work.company }}</span>
            <span>{{ formatDate(work.sale_date) }}</span>
          </div>

          <!-- Introduction (truncated) -->
          <p v-if="work.introduction" class="text-gray-300 text-sm line-clamp-2 mb-2">
            {{ work.introduction }}
          </p>

          <!-- Genres -->
          <div class="flex flex-wrap gap-1">
            <span 
              v-for="genre in work.genre.slice(0, 5)" 
              :key="genre"
              class="tag text-xs"
            >
              {{ genre }}
            </span>
            <span v-if="work.genre.length > 5" class="text-xs text-gray-400">
              +{{ work.genre.length - 5 }} 更多
            </span>
          </div>
        </div>

        <!-- Action Button -->
        <div class="flex-shrink-0 ml-4">
          <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <button class="btn-primary text-sm px-3 py-1">
              查看
            </button>
          </div>
        </div>
      </div>

      <!-- Additional Info Row -->
      <div class="flex items-center justify-between mt-3 text-xs text-gray-500">
        <div class="flex items-center space-x-4">
          <span v-if="work.work_format && work.work_format.length > 0">
            {{ work.work_format.join(', ') }}
          </span>
          <span v-if="work.file_size && work.file_size.length > 0">
            {{ work.file_size[0] }}
          </span>
        </div>
        
        <div class="flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  work: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click', 'show-toast'])

const imageError = ref(false)

const imageUrl = computed(() => {
  if (imageError.value) {
    return '/api/placeholder/160/224'  // Fallback image
  }
  return props.work.image_url ? `http://localhost:8001${props.work.image_url}` : '/api/placeholder/160/224'
})

const handleImageError = () => {
  imageError.value = true
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return dateString
  }
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
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>