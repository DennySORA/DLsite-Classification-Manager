import { ref, watch } from 'vue'

const API_BASE = 'http://localhost:8001'

export interface WorkFilters {
  search: string
  company: string
  collection: string
  rating: string
  workFormat: string
  fileFormat: string
  sortBy: string
  tags: string[]
  tagMode: 'AND' | 'OR'
}

export const useWorkData = () => {
  // State
  const loading = ref(true)
  const loadingMore = ref(false)
  const works = ref<any[]>([])
  const totalWorks = ref(0)
  const hasMore = ref(true)
  const offset = ref(0)
  const pageSize = ref(50)

  // Data
  const companies = ref<string[]>([])
  const collections = ref<string[]>([])
  const workFormats = ref<string[]>([])
  const fileFormats = ref<string[]>([])
  const allTags = ref<any[]>([])

  // Fetch works with filters
  const fetchWorks = async (filters: WorkFilters, reset = false) => {
    if (reset) {
      offset.value = 0
      hasMore.value = true
      loading.value = true
    } else {
      loadingMore.value = true
    }

    try {
      const params = new URLSearchParams()
      if (filters.search) params.append('search', filters.search)
      if (filters.company) params.append('company', filters.company)
      if (filters.collection) params.append('collection', filters.collection)
      if (filters.rating) params.append('my_rating', filters.rating)
      if (filters.workFormat) params.append('work_format', filters.workFormat)
      if (filters.fileFormat) params.append('file_format', filters.fileFormat)
      if (filters.sortBy) params.append('sort', filters.sortBy)
      if (filters.tags.length > 0) {
        params.append('tags', filters.tags.join(','))
        params.append('tag_mode', filters.tagMode)
      }
      params.append('limit', pageSize.value.toString())
      params.append('offset', offset.value.toString())

      const response = await fetch(`${API_BASE}/works?${params}`)
      const data = await response.json()

      if (reset) {
        works.value = data.works
        companies.value = data.companies || []
      } else {
        works.value = [...works.value, ...data.works]
      }

      totalWorks.value = data.total
      offset.value += data.works.length
      hasMore.value = works.value.length < data.total

      // Fetch all tags
      if (reset && data.genres && data.genres.length > 0) {
        allTags.value = data.genres.map((g: string) => ({ name: g, count: 0 }))
      }

      return { success: true }
    } catch (error) {
      console.error('Error fetching works:', error)
      return { success: false, error }
    } finally {
      loading.value = false
      loadingMore.value = false
    }
  }

  // Fetch collections
  const fetchCollections = async () => {
    try {
      const response = await fetch(`${API_BASE}/collections`)
      const data = await response.json()
      collections.value = data.collections || []
    } catch (error) {
      console.error('Error fetching collections:', error)
    }
  }

  // Fetch work formats
  const fetchWorkFormats = async () => {
    try {
      const response = await fetch(`${API_BASE}/work-formats`)
      const data = await response.json()
      workFormats.value = data.work_formats || []
    } catch (error) {
      console.error('Error fetching work formats:', error)
    }
  }

  // Fetch file formats
  const fetchFileFormats = async () => {
    try {
      const response = await fetch(`${API_BASE}/file-formats`)
      const data = await response.json()
      fileFormats.value = data.file_formats || []
    } catch (error) {
      console.error('Error fetching file formats:', error)
    }
  }

  // Fetch work detail
  const fetchWorkDetail = async (code: string) => {
    try {
      const response = await fetch(`${API_BASE}/work/${code}`)
      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      console.error('Error fetching work detail:', error)
      return { success: false, error }
    }
  }

  // Update work rating
  const updateWorkRating = (code: string, rating: number) => {
    const work = works.value.find(w => w.code === code)
    if (work) {
      work.my_rating = rating.toString()
    }
  }

  // Update work collections
  const updateWorkCollections = (code: string, collections: string[]) => {
    const work = works.value.find(w => w.code === code)
    if (work) {
      work.my_collections = collections
    }
  }

  // Change page size
  const changePageSize = (size: number) => {
    pageSize.value = size
  }

  // Load more works
  const loadMore = async (filters: WorkFilters) => {
    if (loadingMore.value || !hasMore.value) return
    await fetchWorks(filters, false)
  }

  // Refresh all data
  const refreshData = async (filters: WorkFilters) => {
    await Promise.all([
      fetchWorks(filters, true),
      fetchCollections(),
      fetchWorkFormats(),
      fetchFileFormats()
    ])
  }

  // Initialize data
  const initializeData = async (filters: WorkFilters) => {
    await Promise.all([
      fetchWorks(filters, true),
      fetchCollections(),
      fetchWorkFormats(),
      fetchFileFormats()
    ])
  }

  return {
    // State
    loading,
    loadingMore,
    works,
    totalWorks,
    hasMore,
    offset,
    pageSize,

    // Data
    companies,
    collections,
    workFormats,
    fileFormats,
    allTags,

    // Methods
    fetchWorks,
    fetchCollections,
    fetchWorkFormats,
    fetchFileFormats,
    fetchWorkDetail,
    updateWorkRating,
    updateWorkCollections,
    changePageSize,
    loadMore,
    refreshData,
    initializeData
  }
}
