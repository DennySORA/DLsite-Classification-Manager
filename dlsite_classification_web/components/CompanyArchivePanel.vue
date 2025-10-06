<template>
  <div class="company-archive-panel">
    <!-- Header -->
    <div class="panel-header">
      <div class="header-content">
        <h2 class="panel-title">公司作品總覽</h2>
        <button @click="$emit('close')" class="close-button" aria-label="關閉">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Company Selector -->
    <div class="selector-section">
      <div class="selector-group">
        <label for="company-select" class="selector-label">選擇公司</label>
        <div class="selector-wrapper">
          <select
            id="company-select"
            v-model="selectedCompanyId"
            @change="onCompanySelect"
            :disabled="loading"
            class="company-select"
          >
            <option value="">-- 請選擇公司 --</option>
            <option
              v-for="company in companies"
              :key="company.id"
              :value="company.id"
            >
              {{ company.name }} ({{ company.work_count }} 作品)
            </option>
          </select>
          <div class="select-icon">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-section">
      <div class="skeleton-stats">
        <div v-for="i in 3" :key="i" class="skeleton-stat"></div>
      </div>
      <div class="skeleton-grid">
        <div v-for="i in 12" :key="i" class="skeleton-card"></div>
      </div>
    </div>

    <!-- Results -->
    <div v-else-if="companyStatus" class="results-section">
      <!-- Stats -->
      <div class="stats-bar">
        <div class="stat-item owned-stat">
          <div class="stat-icon">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ ownedCount }}</div>
            <div class="stat-label">已擁有</div>
          </div>
        </div>

        <div class="stat-item missing-stat">
          <div class="stat-icon">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ missingCount }}</div>
            <div class="stat-label">尚缺</div>
          </div>
        </div>

        <div class="stat-item total-stat">
          <div class="stat-content">
            <div class="stat-value">{{ completionPercent }}%</div>
            <div class="stat-label">完成度</div>
          </div>
          <div class="progress-ring">
            <svg viewBox="0 0 36 36">
              <path
                class="progress-bg"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                class="progress-fill"
                :stroke-dasharray="`${completionPercent}, 100`"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
          </div>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="filter-section">
        <div class="filter-tabs">
          <button
            @click="activeFilter = 'all'"
            :class="['filter-tab', { active: activeFilter === 'all' }]"
          >
            全部 ({{ allWorks.length }})
          </button>
          <button
            @click="activeFilter = 'owned'"
            :class="['filter-tab', { active: activeFilter === 'owned' }]"
          >
            已擁有 ({{ ownedCount }})
          </button>
          <button
            @click="activeFilter = 'missing'"
            :class="['filter-tab', { active: activeFilter === 'missing' }]"
          >
            尚缺 ({{ missingCount }})
          </button>
        </div>

        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索作品代碼或標題..."
            class="search-input"
          >
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="clear-search"
            aria-label="清除搜索"
          >
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Works Grid -->
      <div v-if="filteredWorks.length > 0" class="works-grid">
        <TransitionGroup name="work-card">
          <div
            v-for="(work, index) in filteredWorks"
            :key="work.code"
            :class="['work-card', work.isOwned ? 'owned' : 'missing']"
            :style="{ animationDelay: `${index * 30}ms` }"
          >
            <div class="card-header">
              <div class="status-badge">
                <svg v-if="work.isOwned" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <svg v-else viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="work-code">{{ work.code }}</div>
            </div>

            <div class="card-body">
              <h3 class="work-title">{{ work.title || '無標題' }}</h3>
              <p v-if="work.folder" class="work-folder">
                <svg viewBox="0 0 20 20" fill="currentColor">
                  <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/>
                </svg>
                {{ truncateFolder(work.folder) }}
              </p>
            </div>

            <div class="card-footer">
              <a
                :href="`https://www.dlsite.com/maniax/work/=/product_id/${work.code}.html`"
                target="_blank"
                rel="noopener noreferrer"
                class="dlsite-link"
                @click.stop
              >
                <span>查看 DLsite</span>
                <svg viewBox="0 0 20 20" fill="currentColor">
                  <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"/>
                  <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"/>
                </svg>
              </a>
            </div>
          </div>
        </TransitionGroup>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <svg class="empty-icon" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
        </svg>
        <p class="empty-text">沒有找到符合條件的作品</p>
        <p class="empty-hint">試試調整搜索或篩選條件</p>
      </div>

      <!-- Action Bar -->
      <div v-if="missingCount > 0" class="action-bar">
        <button
          @click="createArchive(false)"
          :disabled="archiving"
          :class="['create-archive-btn', { loading: archiving, success: archiveSuccess }]"
        >
          <span v-if="archiving" class="btn-content">
            <span class="btn-spinner"></span>
            <span>正在創建 Archive...</span>
          </span>
          <span v-else-if="archiveSuccess" class="btn-content">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>創建成功</span>
          </span>
          <span v-else class="btn-content">
            <svg viewBox="0 0 20 20" fill="currentColor">
              <path d="M4 3a2 2 0 100 4h12a2 2 0 100-4H4z"/>
              <path fill-rule="evenodd" d="M3 8h14v7a2 2 0 01-2 2H5a2 2 0 01-2-2V8zm5 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" clip-rule="evenodd"/>
            </svg>
            <span>創建 Archive ({{ missingCount }} 作品)</span>
          </span>
        </button>

        <button
          @click="createArchive(true)"
          :disabled="archiving"
          class="force-refresh-btn"
        >
          <svg viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/>
          </svg>
          <span>強制更新</span>
        </button>
      </div>
    </div>

    <!-- Initial State -->
    <div v-else class="initial-state">
      <svg class="initial-icon" viewBox="0 0 20 20" fill="currentColor">
        <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
        <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/>
      </svg>
      <h3 class="initial-title">選擇公司以開始</h3>
      <p class="initial-text">選擇一間公司來查看其所有作品，並比對你的收藏狀態</p>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast.show" :class="['toast', toast.type]">
        <svg v-if="toast.type === 'success'" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>
        <svg v-else viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
        <span>{{ toast.message }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const emit = defineEmits(['close'])

// State
const companies = ref([])
const selectedCompanyId = ref('')
const companyStatus = ref(null)
const loading = ref(false)
const archiving = ref(false)
const archiveSuccess = ref(false)
const activeFilter = ref('all')
const searchQuery = ref('')
const toast = ref({ show: false, message: '', type: 'success' })

// Computed
const allWorks = computed(() => {
  if (!companyStatus.value) return []

  const owned = companyStatus.value.owned_works.map(w => ({
    ...w,
    isOwned: true
  }))

  const missing = companyStatus.value.missing_works.map(w => ({
    ...w,
    isOwned: false
  }))

  return [...owned, ...missing].sort((a, b) => a.code.localeCompare(b.code))
})

const filteredWorks = computed(() => {
  let works = allWorks.value

  // Apply filter
  if (activeFilter.value === 'owned') {
    works = works.filter(w => w.isOwned)
  } else if (activeFilter.value === 'missing') {
    works = works.filter(w => !w.isOwned)
  }

  // Apply search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    works = works.filter(w =>
      w.code.toLowerCase().includes(query) ||
      (w.title && w.title.toLowerCase().includes(query))
    )
  }

  return works
})

const ownedCount = computed(() =>
  companyStatus.value?.owned_works.length || 0
)

const missingCount = computed(() =>
  companyStatus.value?.missing_works.length || 0
)

const completionPercent = computed(() => {
  if (!companyStatus.value || companyStatus.value.total_on_dlsite <= 0) return 0
  return Math.round((ownedCount.value / companyStatus.value.total_on_dlsite) * 100)
})

// Methods
const showToast = (message, type = 'success') => {
  toast.value = { show: true, message, type }
  setTimeout(() => {
    toast.value.show = false
  }, 3000)
}

const truncateFolder = (folder) => {
  if (folder.length > 35) {
    return '...' + folder.slice(-32)
  }
  return folder
}

const fetchCompanies = async () => {
  try {
    const response = await fetch('http://localhost:8001/companies/list')
    const data = await response.json()
    companies.value = data.companies || []
  } catch (error) {
    console.error('Failed to fetch companies:', error)
    showToast('無法載入公司列表', 'error')
  }
}

const onCompanySelect = async () => {
  if (!selectedCompanyId.value) {
    companyStatus.value = null
    return
  }

  loading.value = true
  companyStatus.value = null
  activeFilter.value = 'all'
  searchQuery.value = ''

  try {
    const response = await fetch(`http://localhost:8001/company/${selectedCompanyId.value}/works-status`)
    const data = await response.json()
    companyStatus.value = data

    if (data.total_on_dlsite === -1) {
      showToast('無法取得 DLsite 資料，僅顯示已擁有作品', 'error')
    }
  } catch (error) {
    console.error('Failed to fetch company status:', error)
    showToast('無法載入公司資料', 'error')
  } finally {
    loading.value = false
  }
}

const createArchive = async (forceUpdate) => {
  if (!selectedCompanyId.value) return

  archiving.value = true
  archiveSuccess.value = false

  try {
    const response = await fetch(`http://localhost:8001/company/${selectedCompanyId.value}/archive`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ force_update: forceUpdate })
    })

    const data = await response.json()

    if (response.ok) {
      archiveSuccess.value = true
      showToast(`Archive 創建成功：${data.works_archived} 個作品`, 'success')

      setTimeout(() => {
        archiveSuccess.value = false
      }, 2000)

      // Refresh data
      await onCompanySelect()
    } else {
      showToast(data.detail || 'Archive 創建失敗', 'error')
    }
  } catch (error) {
    console.error('Failed to create archive:', error)
    showToast('Archive 創建失敗', 'error')
  } finally {
    archiving.value = false
  }
}

onMounted(() => {
  fetchCompanies()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Variables */
.company-archive-panel {
  --color-bg: #0a0a0f;
  --color-surface: #12121a;
  --color-surface-elevated: #1a1a24;
  --color-border: #2a2a34;
  --color-border-hover: #3a3a44;

  --color-text-primary: #e5e7eb;
  --color-text-secondary: #9ca3af;
  --color-text-muted: #6b7280;

  --color-owned: #3b82f6;
  --color-owned-hover: #60a5fa;
  --color-owned-bg: rgba(59, 130, 246, 0.1);

  --color-missing: #f59e0b;
  --color-missing-hover: #fbbf24;
  --color-missing-bg: rgba(245, 158, 11, 0.1);

  --color-accent: #06b6d4;
  --color-accent-hover: #0891b2;

  --color-success: #10b981;
  --color-error: #ef4444;

  --spacing-xs: 0.5rem;
  --spacing-sm: 0.75rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;

  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Panel Container */
.company-archive-panel {
  font-family: 'DM Sans', 'Inter', -apple-system, system-ui, sans-serif;
  background: linear-gradient(to bottom, var(--color-bg), #0f0f15);
  color: var(--color-text-primary);
  border-radius: var(--radius-lg);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

/* Header */
.panel-header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: var(--spacing-lg) var(--spacing-xl);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  letter-spacing: -0.02em;
}

.close-button {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-md);
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
}

.close-button:hover {
  background: var(--color-border);
  color: var(--color-text-primary);
  transform: scale(1.05);
}

.close-button:active {
  transform: scale(0.95);
}

.close-button svg {
  width: 1.25rem;
  height: 1.25rem;
}

/* Selector Section */
.selector-section {
  padding: var(--spacing-lg) var(--spacing-xl);
  border-bottom: 1px solid var(--color-border);
}

.selector-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.selector-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  letter-spacing: 0.02em;
}

.selector-wrapper {
  position: relative;
}

.company-select {
  width: 100%;
  padding: 0.875rem 3rem 0.875rem 1rem;
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  appearance: none;
  transition: all var(--transition-base);
}

.company-select:hover:not(:disabled) {
  border-color: var(--color-border-hover);
}

.company-select:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
}

.company-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.company-select option {
  background: var(--color-surface);
  color: var(--color-text-primary);
}

.select-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-text-secondary);
  pointer-events: none;
}

/* Loading State */
.loading-section {
  padding: var(--spacing-xl);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.skeleton-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
}

.skeleton-stat {
  height: 5rem;
  background: linear-gradient(90deg, var(--color-surface) 0%, var(--color-surface-elevated) 50%, var(--color-surface) 100%);
  background-size: 200% 100%;
  border-radius: var(--radius-md);
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--spacing-md);
}

.skeleton-card {
  height: 12rem;
  background: linear-gradient(90deg, var(--color-surface) 0%, var(--color-surface-elevated) 50%, var(--color-surface) 100%);
  background-size: 200% 100%;
  border-radius: var(--radius-md);
  animation: skeleton-loading 1.5s ease-in-out infinite;
  animation-delay: calc(var(--i) * 50ms);
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Results Section */
.results-section {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* Stats Bar */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  padding: var(--spacing-lg) var(--spacing-xl);
  border-bottom: 1px solid var(--color-border);
}

.stat-item {
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  transition: all var(--transition-base);
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.owned-stat {
  border-color: rgba(59, 130, 246, 0.3);
}

.owned-stat:hover {
  background: var(--color-owned-bg);
  border-color: var(--color-owned);
}

.missing-stat {
  border-color: rgba(245, 158, 11, 0.3);
}

.missing-stat:hover {
  background: var(--color-missing-bg);
  border-color: var(--color-missing);
}

.total-stat {
  border-color: rgba(6, 182, 212, 0.3);
}

.total-stat:hover {
  background: rgba(6, 182, 212, 0.05);
  border-color: var(--color-accent);
}

.stat-icon {
  width: 2.5rem;
  height: 2.5rem;
  flex-shrink: 0;
}

.owned-stat .stat-icon {
  color: var(--color-owned);
}

.missing-stat .stat-icon {
  color: var(--color-missing);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.progress-ring {
  width: 2.5rem;
  height: 2.5rem;
  flex-shrink: 0;
}

.progress-ring svg {
  transform: rotate(-90deg);
}

.progress-bg {
  fill: none;
  stroke: var(--color-border);
  stroke-width: 3;
}

.progress-fill {
  fill: none;
  stroke: var(--color-accent);
  stroke-width: 3;
  stroke-linecap: round;
  transition: stroke-dasharray var(--transition-slow);
}

/* Filter Section */
.filter-section {
  padding: var(--spacing-lg) var(--spacing-xl);
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
}

.filter-tabs {
  display: flex;
  gap: var(--spacing-xs);
  flex: 1;
}

.filter-tab {
  padding: 0.625rem 1rem;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  white-space: nowrap;
}

.filter-tab:hover {
  background: var(--color-surface-elevated);
  border-color: var(--color-border-hover);
  color: var(--color-text-primary);
}

.filter-tab.active {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: white;
}

.filter-tab:active {
  transform: scale(0.95);
}

.search-box {
  position: relative;
  flex: 0 1 300px;
}

.search-icon {
  position: absolute;
  left: 0.875rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.125rem;
  height: 1.125rem;
  color: var(--color-text-muted);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.625rem 2.75rem 0.625rem 2.5rem;
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: 0.875rem;
  transition: all var(--transition-base);
}

.search-input::placeholder {
  color: var(--color-text-muted);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
}

.clear-search {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.5rem;
  height: 1.5rem;
  padding: 0;
  background: transparent;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  border-radius: 0.25rem;
  transition: all var(--transition-fast);
}

.clear-search:hover {
  background: var(--color-surface);
  color: var(--color-text-secondary);
}

.clear-search svg {
  width: 100%;
  height: 100%;
}

/* Works Grid */
.works-grid {
  padding: var(--spacing-xl);
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--spacing-md);
  flex: 1;
}

.work-card {
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all var(--transition-base);
  animation: card-appear 0.4s ease-out backwards;
}

@keyframes card-appear {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.work-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  border-color: var(--color-border-hover);
}

.work-card.owned {
  border-color: rgba(59, 130, 246, 0.3);
}

.work-card.owned:hover {
  border-color: var(--color-owned);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
}

.work-card.missing {
  border-color: rgba(245, 158, 11, 0.3);
}

.work-card.missing:hover {
  border-color: var(--color-missing);
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.2);
}

.card-header {
  padding: var(--spacing-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-sm);
  border-bottom: 1px solid var(--color-border);
}

.status-badge {
  width: 1.5rem;
  height: 1.5rem;
  flex-shrink: 0;
}

.work-card.owned .status-badge {
  color: var(--color-owned);
}

.work-card.missing .status-badge {
  color: var(--color-missing);
}

.work-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 0.05em;
}

.card-body {
  padding: var(--spacing-md);
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.work-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.work-folder {
  font-size: 0.8125rem;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin: 0;
}

.work-folder svg {
  width: 0.875rem;
  height: 0.875rem;
  flex-shrink: 0;
}

.card-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--color-border);
}

.dlsite-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  font-size: 0.8125rem;
  font-weight: 600;
  text-decoration: none;
  transition: all var(--transition-base);
}

.dlsite-link:hover {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: white;
  transform: translateY(-1px);
}

.dlsite-link:active {
  transform: translateY(0);
}

.dlsite-link svg {
  width: 0.875rem;
  height: 0.875rem;
}

/* Empty State */
.empty-state {
  padding: var(--spacing-xl);
  text-align: center;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
}

.empty-icon {
  width: 4rem;
  height: 4rem;
  color: var(--color-text-muted);
  opacity: 0.5;
}

.empty-text {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin: 0;
}

.empty-hint {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  margin: 0;
}

/* Action Bar */
.action-bar {
  padding: var(--spacing-lg) var(--spacing-xl);
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
  display: flex;
  gap: var(--spacing-md);
}

.create-archive-btn {
  flex: 1;
  padding: 0.875rem 1.5rem;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
}

.create-archive-btn:hover:not(:disabled) {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
}

.create-archive-btn:active:not(:disabled) {
  transform: translateY(0);
}

.create-archive-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.create-archive-btn.success {
  background: var(--color-success);
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-content svg {
  width: 1.25rem;
  height: 1.25rem;
}

.btn-spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.force-refresh-btn {
  padding: 0.875rem 1.5rem;
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}

.force-refresh-btn:hover:not(:disabled) {
  background: var(--color-surface);
  border-color: var(--color-border-hover);
  color: var(--color-text-primary);
  transform: translateY(-2px);
}

.force-refresh-btn:active:not(:disabled) {
  transform: translateY(0);
}

.force-refresh-btn svg {
  width: 1.125rem;
  height: 1.125rem;
}

/* Initial State */
.initial-state {
  padding: var(--spacing-xl);
  text-align: center;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
}

.initial-icon {
  width: 5rem;
  height: 5rem;
  color: var(--color-text-muted);
  opacity: 0.5;
}

.initial-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
}

.initial-text {
  font-size: 0.9375rem;
  color: var(--color-text-secondary);
  margin: 0;
  max-width: 400px;
}

/* Toast */
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem 1.5rem;
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9375rem;
  font-weight: 500;
  z-index: 1000;
}

.toast.success {
  border-color: var(--color-success);
  color: var(--color-success);
}

.toast.error {
  border-color: var(--color-error);
  color: var(--color-error);
}

.toast svg {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

/* Transitions */
.toast-enter-active,
.toast-leave-active {
  transition: all var(--transition-slow);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(1rem);
}

.work-card-enter-active {
  transition: all 0.4s ease-out;
}

.work-card-leave-active {
  transition: all 0.2s ease-in;
}

.work-card-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.work-card-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Responsive */
@media (max-width: 1024px) {
  .works-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}

@media (max-width: 768px) {
  .panel-header,
  .selector-section,
  .filter-section,
  .works-grid,
  .action-bar {
    padding-left: var(--spacing-md);
    padding-right: var(--spacing-md);
  }

  .stats-bar {
    grid-template-columns: 1fr;
    padding: var(--spacing-md);
  }

  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-tabs {
    width: 100%;
  }

  .search-box {
    flex: 1 1 auto;
  }

  .works-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: var(--spacing-sm);
  }

  .action-bar {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .works-grid {
    grid-template-columns: 1fr;
  }
}

/* Scrollbar */
.results-section::-webkit-scrollbar {
  width: 8px;
}

.results-section::-webkit-scrollbar-track {
  background: var(--color-surface);
}

.results-section::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 4px;
}

.results-section::-webkit-scrollbar-thumb:hover {
  background: var(--color-border-hover);
}
</style>
