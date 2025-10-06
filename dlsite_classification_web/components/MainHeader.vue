<template>
  <header class="bg-bg-secondary/80 backdrop-blur-xl sticky top-0 z-20 border-b border-bg-border shadow-lg">
    <div class="px-6 py-4">
      <div class="flex items-center justify-between gap-4">
        <div class="flex items-center gap-4">
          <button
            @click="$emit('toggle-sidebar')"
            class="lg:hidden p-2 text-text-muted hover:text-text-primary hover:bg-bg-elevated rounded-lg transition-all duration-200"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <div class="flex items-center gap-3">
            <h1 class="text-2xl lg:text-3xl font-bold text-gradient">DLsite 收藏庫</h1>
            <div class="flex items-center gap-2 text-sm text-text-muted">
              <svg class="w-4 h-4 text-accent-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              <span class="font-medium">{{ totalWorks }}</span>
              <span>作品</span>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button
            @click="$emit('toggle-tag-filter')"
            :class="[
              'btn-secondary flex items-center gap-2',
              { 'ring-2 ring-accent-primary': selectedTagCount > 0 }
            ]"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.99 1.99 0 013 12V7a4 4 0 014-4z" />
            </svg>
            <span>標籤篩選</span>
            <span v-if="selectedTagCount > 0" class="badge-primary">{{ selectedTagCount }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Tag Filter Panel -->
    <div v-if="showTagFilter" class="px-6 pb-6 animate-slide-down">
      <slot name="tag-filter"></slot>
    </div>
  </header>
</template>

<script setup>
defineProps({
  totalWorks: {
    type: Number,
    default: 0
  },
  selectedTagCount: {
    type: Number,
    default: 0
  },
  showTagFilter: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-sidebar', 'toggle-tag-filter'])
</script>

<style scoped>
.text-gradient {
  background: linear-gradient(135deg, var(--color-accent-primary), var(--color-accent-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.animate-slide-down {
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
