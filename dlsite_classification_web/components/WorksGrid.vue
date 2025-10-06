<template>
  <div class="space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="text-center">
        <div class="spinner-lg mx-auto mb-4"></div>
        <p class="text-text-muted text-lg">載入收藏庫中...</p>
      </div>
    </div>

    <!-- Works Grid -->
    <template v-else-if="works.length > 0">
      <!-- Stats & Controls -->
      <div class="flex flex-wrap justify-between items-center gap-4">
        <div class="flex items-center gap-4 flex-wrap">
          <p class="text-text-secondary text-sm">
            顯示 <span class="text-accent-primary font-semibold">{{ works.length }}</span> / <span class="text-accent-primary font-semibold">{{ totalWorks }}</span> 個作品
          </p>
          <div v-if="activeFiltersCount > 0 || selectedTagCount > 0" class="flex items-center gap-2 flex-wrap">
            <span v-if="activeFiltersCount > 0" class="badge-secondary text-xs">{{ activeFiltersCount }} 個基本篩選</span>
            <span v-if="selectedTagCount > 0" class="badge-primary text-xs">{{ selectedTagCount }} 個標籤 ({{ tagFilterMode }})</span>
          </div>
        </div>

        <!-- Page Size Selection -->
        <div class="flex items-center gap-2">
          <span class="text-sm text-text-muted">每頁:</span>
          <div class="flex bg-bg-elevated rounded-lg border border-bg-border overflow-hidden">
            <button
              v-for="size in [20, 50, 100]"
              :key="size"
              @click="$emit('change-page-size', size)"
              :class="[
                'px-3 py-1.5 text-sm font-medium transition-all duration-200',
                pageSize === size
                  ? 'bg-accent-primary text-white'
                  : 'text-text-muted hover:text-text-primary hover:bg-bg-elevated'
              ]"
            >
              {{ size }}
            </button>
          </div>
        </div>
      </div>

      <!-- Works Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <WorkCard
          v-for="work in works"
          :key="work.code"
          :work="work"
          @click="$emit('work-click', work)"
          @rating-updated="$emit('rating-updated', $event)"
          @collection-updated="$emit('collection-updated', $event)"
          @tag-filter-add="$emit('tag-filter-add', $event)"
          @company-filter="$emit('company-filter', $event)"
          @show-toast="$emit('show-toast', $event)"
        />
      </div>

      <!-- Load More Trigger -->
      <div ref="loadMoreTrigger" class="h-20 flex items-center justify-center">
        <div v-if="loadingMore" class="text-center">
          <div class="spinner mx-auto mb-2"></div>
          <p class="text-text-muted text-sm">載入更多...</p>
        </div>
        <div v-else-if="!hasMore" class="text-text-muted text-sm">
          已載入全部作品
        </div>
      </div>
    </template>

    <!-- Empty State -->
    <div v-else class="flex flex-col items-center justify-center h-64 text-center">
      <svg class="w-24 h-24 text-text-muted mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-text-muted text-lg mb-2">沒有找到作品</p>
      <button @click="$emit('clear-filters')" class="btn-primary">清除所有篩選</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import WorkCard from './WorkCard.vue'

defineProps({
  works: {
    type: Array,
    required: true
  },
  totalWorks: {
    type: Number,
    default: 0
  },
  loading: {
    type: Boolean,
    default: false
  },
  loadingMore: {
    type: Boolean,
    default: false
  },
  hasMore: {
    type: Boolean,
    default: true
  },
  pageSize: {
    type: Number,
    default: 50
  },
  activeFiltersCount: {
    type: Number,
    default: 0
  },
  selectedTagCount: {
    type: Number,
    default: 0
  },
  tagFilterMode: {
    type: String,
    default: 'AND'
  }
})

defineEmits([
  'work-click',
  'rating-updated',
  'collection-updated',
  'tag-filter-add',
  'company-filter',
  'show-toast',
  'change-page-size',
  'clear-filters'
])

// Template ref for infinite scroll
const loadMoreTrigger = ref(null)

// Expose the ref so parent can access it
defineExpose({
  loadMoreTrigger
})
</script>
