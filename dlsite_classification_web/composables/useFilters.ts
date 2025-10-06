import { ref, computed } from 'vue'
import type { WorkFilters } from './useWorkData'

export const useFilters = () => {
  // Filter state
  const filters = ref<WorkFilters>({
    search: '',
    company: '',
    collection: '',
    rating: '',
    workFormat: '',
    fileFormat: '',
    sortBy: 'title',
    tags: [],
    tagMode: 'AND'
  })

  // Computed
  const activeFiltersCount = computed(() => {
    let count = 0
    if (filters.value.search) count++
    if (filters.value.company) count++
    if (filters.value.collection) count++
    if (filters.value.rating) count++
    if (filters.value.workFormat) count++
    if (filters.value.fileFormat) count++
    return count
  })

  // Methods
  const updateFilter = (key: keyof WorkFilters, value: any) => {
    filters.value = { ...filters.value, [key]: value }
  }

  const clearAllFilters = () => {
    filters.value = {
      search: '',
      company: '',
      collection: '',
      rating: '',
      workFormat: '',
      fileFormat: '',
      sortBy: 'title',
      tags: [],
      tagMode: 'AND'
    }
  }

  const addTag = (tag: string) => {
    if (!filters.value.tags.includes(tag)) {
      filters.value.tags = [...filters.value.tags, tag]
    }
  }

  const removeTag = (tag: string) => {
    filters.value.tags = filters.value.tags.filter(t => t !== tag)
  }

  const clearTags = () => {
    filters.value.tags = []
  }

  const setTagMode = (mode: 'AND' | 'OR') => {
    filters.value.tagMode = mode
  }

  const setTagFilter = (selectedTags: string[], filterMode: 'AND' | 'OR') => {
    filters.value.tags = selectedTags
    filters.value.tagMode = filterMode
  }

  const resetTagFilter = () => {
    filters.value.tags = []
    filters.value.tagMode = 'AND'
  }

  return {
    // State
    filters,

    // Computed
    activeFiltersCount,

    // Methods
    updateFilter,
    clearAllFilters,
    addTag,
    removeTag,
    clearTags,
    setTagMode,
    setTagFilter,
    resetTagFilter
  }
}
