<template>
  <div class="w-full rounded-2xl border border-gray-600 max-h-[85vh] flex flex-col" style="background: rgba(15, 15, 25, 0.95); backdrop-filter: blur(25px);">
    <!-- 標籤篩選標題與模式切換 -->
    <div class="flex items-center justify-between p-6 pb-4 flex-shrink-0">
      <h3 class="text-xl font-bold text-text-primary font-multilingual flex items-center">
        <svg class="w-6 h-6 mr-3 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.99 1.99 0 013 12V7a4 4 0 014-4z" />
        </svg>
        標籤篩選器
      </h3>
      
      <!-- 篩選模式切換 -->
      <div class="flex items-center space-x-2">
        <span class="text-sm text-text-muted font-multilingual">篩選模式:</span>
        <div class="relative inline-flex rounded-full p-1 border border-gray-600" style="background: rgba(30, 30, 40, 0.9);">
          <button
            @click="filterMode = 'OR'"
            :class="[
              'relative px-4 py-2 text-sm font-medium rounded-full transition-all duration-300 font-multilingual',
              filterMode === 'OR' 
                ? 'text-white' 
                : 'text-text-muted hover:text-text-secondary'
            ]"
            :style="filterMode === 'OR' ? { backgroundColor: '#00D2FF', boxShadow: '0 0 20px rgba(0, 210, 255, 0.5)' } : {}"
          >
            OR 模式
          </button>
          <button
            @click="filterMode = 'AND'"
            :class="[
              'relative px-4 py-2 text-sm font-medium rounded-full transition-all duration-300 font-multilingual',
              filterMode === 'AND' 
                ? 'text-white' 
                : 'text-text-muted hover:text-text-secondary'
            ]"
            :style="filterMode === 'AND' ? { backgroundColor: '#FF006E', boxShadow: '0 0 20px rgba(181, 55, 242, 0.5)' } : {}"
          >
            AND 模式
          </button>
        </div>
      </div>
    </div>

    <!-- 標籤搜索框 -->
    <div class="px-6 pb-4 flex-shrink-0">
      <div class="relative">
        <input
          v-model="tagSearch"
          type="text"
          placeholder="搜索標籤..."
          class="input-field w-full pl-10 pr-8 text-sm"
        >
        <div class="absolute left-3 top-1/2 transform -translate-y-1/2">
          <svg class="w-4 h-4 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <div v-if="tagSearch" class="absolute right-3 top-1/2 transform -translate-y-1/2">
          <button @click="tagSearch = ''" class="text-text-muted hover:text-text-secondary">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- 已選標籤 -->
    <div class="px-6 pb-4 flex-shrink-0 h-24 min-h-24">
      <div v-if="selectedTags.length > 0" class="h-full">
        <div class="flex items-center justify-between mb-2">
          <label class="block text-sm font-medium text-text-secondary">已選標籤 ({{ selectedTags.length }})</label>
          <button 
            @click="clearSelectedTags" 
            class="px-3 py-1.5 bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 text-white text-xs font-medium rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center space-x-1"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            <span>清除全部</span>
          </button>
        </div>
        <div class="grid grid-cols-5 gap-2 h-16 overflow-y-auto scrollbar-thin">
          <div 
            v-for="tag in selectedTags" 
            :key="tag"
            class="flex items-center justify-between px-2 py-1 rounded-lg text-xs font-medium h-6"
            :class="filterMode === 'AND' 
              ? 'bg-gradient-to-r from-violet-500 to-purple-500 text-white shadow-sm border border-violet-400' 
              : 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-sm border border-blue-400'"
          >
            <span class="flex-1 truncate pr-1 text-xs">{{ tag }}</span>
            <button @click="removeTag(tag)" class="text-white hover:text-gray-200 flex-shrink-0">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div v-else class="h-full flex items-center justify-center text-sm text-text-muted">
        選擇標籤來開始篩選...
      </div>
    </div>

    <!-- 可選標籤控制 -->
    <div class="px-6 space-y-3 flex-1 min-h-0" :style="{ marginBottom: showComboPanel ? '0' : '4px' }">
      <div class="flex items-center justify-between">
        <label class="block text-sm font-medium text-text-secondary">
          可選標籤 ({{ filteredTags.length }})
        </label>
      </div>
      
      <!-- 分類選擇 -->
      <div class="space-y-2">
        <button
          @click="selectedCategory = 'all'"
          :class="[
            'w-full px-3 py-2 text-sm rounded-lg transition-all duration-200 font-multilingual text-left',
            selectedCategory === 'all' 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-700 text-text-muted hover:bg-gray-600'
          ]"
        >
          🏷️ 全部分類
        </button>
        
        <div class="grid grid-cols-6 gap-2">
          <button
            v-for="(category, key) in tagCategories"
            :key="key"
            @click="toggleCategory(key)"
            :class="[
              'px-2 py-2 text-sm rounded-xl transition-all duration-300 flex flex-col items-center justify-center font-multilingual min-h-14 transform hover:scale-105',
              selectedCategory === key 
                ? 'bg-gradient-to-br from-yellow-400 via-yellow-300 to-yellow-400 text-yellow-900 shadow-xl ring-2 ring-yellow-300 ring-opacity-60 font-semibold' 
                : 'bg-gradient-to-br from-green-400 via-green-300 to-green-400 text-green-900 hover:from-green-500 hover:via-green-400 hover:to-green-500 hover:text-green-100 shadow-lg backdrop-blur-sm'
            ]"
            :title="category.name"
          >
            <span class="text-base mb-1 drop-shadow-sm">{{ category.icon }}</span>
            <span class="text-xs text-center leading-tight font-medium">{{ category.name }}</span>
          </button>
        </div>
      </div>
      
      <!-- 標籤列表 -->
      <div :class="[
        'overflow-y-auto scrollbar-thin transition-all duration-300',
        showComboPanel ? 'max-h-48' : 'max-h-64'
      ]">
        <div v-if="categorizedFilteredTags.length === 0" class="text-center py-4 text-text-muted text-sm">
          沒有找到符合的標籤
        </div>
        
        <div v-else class="grid grid-cols-7 gap-2 pb-2">
          <button 
            v-for="tag in categorizedFilteredTags.slice(0, 140)" 
            :key="tag.name"
            :class="[
              'px-2 py-2 rounded-lg transition-all duration-300 flex flex-col items-center justify-center font-multilingual min-h-16 text-center transform hover:scale-105',
              selectedTags.includes(tag.name) 
                ? (filterMode === 'AND' 
                  ? 'bg-gradient-to-br from-fuchsia-600 to-violet-700 border border-fuchsia-400 text-white shadow-xl ring-2 ring-white ring-opacity-20' 
                  : 'bg-gradient-to-br from-blue-600 to-indigo-700 border border-blue-400 text-white shadow-xl ring-2 ring-white ring-opacity-20')
                : 'bg-gradient-to-br from-slate-600 to-slate-700 text-slate-200 hover:from-slate-500 hover:to-slate-600 hover:text-white shadow-lg border border-slate-500 hover:border-slate-400'
            ]"
            @click="toggleTag(tag.name)"
            :title="tag.name"
          >
            <span class="text-xs font-medium leading-tight line-clamp-2 mb-1 drop-shadow-sm">{{ tag.name }}</span>
            <span class="text-xs opacity-80 bg-black bg-opacity-30 px-1 py-0.5 rounded text-gray-200 backdrop-blur-sm">({{ tag.count }})</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 組合功能區域 - 可展開/收起設計 -->
    <div class="relative border-t border-gray-600 bg-gray-900 bg-opacity-60 backdrop-blur-sm rounded-b-2xl flex-shrink-0">
      <!-- 組合管理標題 - 可點擊展開/收起 -->
      <div class="px-6 py-3 cursor-pointer hover:bg-gray-800 hover:bg-opacity-50 transition-colors duration-200" @click="showComboPanel = !showComboPanel">
        <div class="flex items-center justify-between">
          <h4 class="text-sm font-medium text-text-secondary flex items-center">
            <svg class="w-4 h-4 mr-2 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            標籤組合管理
            <span v-if="savedCombos.length > 0" class="ml-2 px-2 py-0.5 text-xs bg-purple-600 bg-opacity-20 text-purple-300 rounded-full">
              {{ savedCombos.length }}
            </span>
          </h4>
          <div class="flex items-center space-x-2">
            <span class="text-xs text-text-muted">{{ showComboPanel ? '收起' : '展開' }}</span>
            <svg 
              :class="['w-4 h-4 text-text-muted transition-transform duration-300', showComboPanel ? 'rotate-180' : '']"
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>
      
      <!-- 展開的組合管理面板 - 向上展開覆蓋標籤區域 -->
      <div 
        v-if="showComboPanel" 
        class="absolute bottom-full left-0 right-0 bg-gray-900 bg-opacity-98 backdrop-blur-md border border-gray-600 rounded-t-2xl shadow-2xl animate-slide-up overflow-y-auto scrollbar-thin"
        style="backdrop-filter: blur(20px); border-bottom: none; z-index: 9999; max-height: 400px;"
      >
        <!-- 儲存新組合 -->
        <div v-if="selectedTags.length > 0" class="px-6 py-4 border-b border-gray-600">
          <div class="space-y-3">
            <label class="text-sm font-medium text-text-secondary">儲存當前標籤組合</label>
            <div class="flex space-x-2">
              <input
                v-model="newComboName"
                type="text"
                :placeholder="selectedTags.length > 0 ? `輸入組合名稱... (留空則自動產生: ${generateComboName()})` : '輸入組合名稱...'"
                class="input-field flex-1 text-sm py-2 px-3"
                style="transform: none !important; transition: none !important;"
                @keyup.enter="saveTagCombo"
              >
              <button 
                @click="saveTagCombo" 
                :disabled="selectedTags.length === 0"
                class="px-4 py-2 bg-gradient-to-r from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 disabled:bg-gray-600 disabled:cursor-not-allowed text-yellow-900 font-semibold rounded-lg transition-colors duration-200 text-sm shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                儲存 ({{ selectedTags.length }})
              </button>
            </div>
          </div>
        </div>
        
        <!-- 已儲存的組合 -->
        <div v-if="savedCombos.length > 0" class="px-6 py-4 border-b border-gray-600">
          <div class="space-y-3">
            <label class="text-sm font-medium text-text-secondary">已儲存組合 ({{ savedCombos.length }})</label>
            <div class="grid grid-cols-3 gap-2 max-h-32 overflow-y-auto scrollbar-thin">
              <div 
                v-for="combo in savedCombos" 
                :key="combo.id"
                class="flex items-center justify-between bg-blue-500 bg-opacity-20 border border-blue-400 border-opacity-40 text-blue-300 px-3 py-2 rounded-lg shadow-sm backdrop-blur-sm hover:bg-opacity-30 transition-all duration-200"
              >
                <button 
                  @click="loadTagCombo(combo)"
                  class="flex-1 text-left hover:text-white transition-colors min-w-0"
                >
                  <div class="text-sm font-medium truncate">{{ combo.name }}</div>
                  <div class="text-xs opacity-75">{{ combo.tags.length }} 標籤 • {{ combo.mode }}</div>
                </button>
                <button 
                  @click="deleteTagCombo(combo.id)"
                  class="flex items-center justify-center w-6 h-6 hover:bg-red-500 hover:bg-opacity-20 rounded-full transition-colors group ml-2 flex-shrink-0"
                >
                  <svg class="w-4 h-4 text-red-400 group-hover:text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 快捷動作 -->
        <div class="px-6 py-4">
          <div class="flex justify-end">
            <button @click="showComboPanel = false" class="px-4 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded-lg transition-colors duration-200 text-sm font-medium">
              收起
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
  allTags: {
    type: Array,
    default: () => []
  },
  modelValue: {
    type: Object,
    default: () => ({
      selectedTags: [],
      filterMode: 'AND'
    })
  }
})

const emit = defineEmits(['update:modelValue', 'apply', 'reset'])

// 響應式數據
const selectedTags = ref([...props.modelValue.selectedTags])
const filterMode = ref(props.modelValue.filterMode)
const tagSearch = ref('')
const newComboName = ref('')
const savedCombos = ref([])
const selectedCategory = ref('all')
const showComboPanel = ref(false)

// 標籤分類定義
const tagCategories = {
  character: {
    name: '角色特徵',
    icon: '👤',
    color: 'bg-pink-600',
    modernColor: 'bg-gradient-to-br from-pink-500 via-rose-500 to-pink-600',
    tags: ['ロリ', 'ショタ', 'お姉さん', '熟女', '人妻', '妹', '姉妹', '母親', '娘', '女教師', 'OL', 'メイド', 'ナース', 'シスター', '巫女', 'ギャル', 'ツンデレ', 'ボクっ娘', 'メスガキ', '不良/ヤンキー', 'お嬢様', '芸能人/アイドル/モデル']
  },
  bodyType: {
    name: '體型特徵',
    icon: '💪',
    color: 'bg-blue-600',
    modernColor: 'bg-gradient-to-br from-blue-500 via-cyan-500 to-blue-600',
    tags: ['巨乳/爆乳', '貧乳/微乳', 'つるぺた', 'ツルペタ', 'スレンダー', 'ムチムチ', 'ぷに', 'ぼて腹/妊婦', '複乳/怪乳/超乳', '筋肉', '長身', '体格差', 'ニューハーフ', 'フタナリ']
  },
  appearance: {
    name: '外觀特徵',
    icon: '✨',
    color: 'bg-purple-600',
    modernColor: 'bg-gradient-to-br from-purple-500 via-violet-500 to-purple-600',
    tags: ['ショートカット', 'ロングヘア', 'ツインテール', 'ポニーテール', '短髪', '金髪', '黒髪', 'メガネ', 'ピアス/装飾品', '褐色/日焼け', 'ネコミミ', '獣耳', 'エルフ/妖精', 'ニーソックス', 'ガーター', 'ストッキング', '靴下']
  },
  costume: {
    name: '服裝道具',
    icon: '👗',
    color: 'bg-green-600',
    modernColor: 'bg-gradient-to-br from-emerald-500 via-green-500 to-emerald-600',
    tags: ['制服', 'セーラー服', 'スクール水着', '水着', 'ブルマ', '体操着', 'コスプレ', 'バニーガール', 'レオタード', '下着', 'パンツ', 'エプロン', 'ゴスロリ', '着物/和服', '着衣', 'ミニスカ', 'スパッツ', '首輪/鎖/拘束具']
  },
  relationship: {
    name: '關係設定',
    icon: '💕',
    color: 'bg-red-600',
    modernColor: 'bg-gradient-to-br from-red-500 via-pink-500 to-red-600',
    tags: ['近親相姦', '近親もの', '実姉', '義妹', '義母', '兄', '弟', '叔父/義父', '父', '幼なじみ', '恋人同士', '先輩/後輩', '同級生/同僚', '同居', '同棲', '年上', '年下攻め', '歳の差', '教師', '学生']
  },
  situation: {
    name: '情境場景',
    icon: '🏠',
    color: 'bg-indigo-600',
    modernColor: 'bg-gradient-to-br from-indigo-500 via-blue-500 to-indigo-600',
    tags: ['学校/学園', 'オフィス/職場', '屋外', '青姦', '露出', '電車', '売春/援交', '風俗/ソープ', '寝取り', '寝取られ', '寝取らせ', '浮気', '痴漢', '盗撮', '監禁', '閉じ込め', '時間停止']
  },
  genre: {
    name: '作品類型',
    icon: '📚',
    color: 'bg-yellow-600',
    modernColor: 'bg-gradient-to-br from-yellow-500 via-amber-500 to-yellow-600',
    tags: ['ファンタジー', 'SF', 'ホラー', 'ギャグ', 'コメディ', 'ラブコメ', 'シリアス', 'ほのぼの', 'サスペンス', 'バイオレンス', 'オカルト', '歴史/時代物', '東方Project', '3D作品', 'アニメ']
  },
  play: {
    name: '性愛行為',
    icon: '🔞',
    color: 'bg-orange-600',
    modernColor: 'bg-gradient-to-br from-orange-500 via-red-500 to-orange-600',
    tags: ['中出し', 'パイズリ', 'フェラチオ', 'イラマチオ', '手コキ', '足コキ', 'アナル', 'クンニ', '口内射精', '顔射', 'ぶっかけ', 'ごっくん/食ザー', '複数プレイ/乱交', '輪姦', 'ハーレム', '逆ハーレム']
  },
  fetish: {
    name: '特殊性癖',
    icon: '🎭',
    color: 'bg-teal-600',
    modernColor: 'bg-gradient-to-br from-teal-500 via-cyan-500 to-teal-600',
    tags: ['おっぱい', 'お尻/ヒップ', '脚', '乳首/乳輪', '乳首責め', '母乳', '搾乳', '潮吹き', '放尿/おしっこ', 'おもらし', '浣腸', 'スカトロ', '尿道', '拡張', 'フィストファック', 'ニプルファック']
  },
  bdsm: {
    name: 'BDSM調教',
    icon: '⛓️',
    color: 'bg-gray-600',
    modernColor: 'bg-gradient-to-br from-gray-500 via-slate-500 to-gray-600',
    tags: ['調教', '拘束', '緊縛', 'ボンデージ', 'ムチ/縄/蝋燭', 'スパンキング', '拷問', '奴隷', '羞恥/恥辱', '屈辱', '下僕', 'しつけ', '命令/無理矢理', '強制/無理矢理', '言葉責め', '焦らし']
  },
  mental: {
    name: '精神狀態',
    icon: '🧠',
    color: 'bg-rose-600',
    modernColor: 'bg-gradient-to-br from-rose-500 via-pink-500 to-rose-600',
    tags: ['催眠', '洗脳', 'トランス/暗示', '薬物', '快楽堕ち', '悪堕ち', '退廃/背徳/インモラル', '無表情', 'アヘ顔', '連続絶頂', '性転換(TS)', '人体改造']
  },
  fantasy: {
    name: '奇幻要素',
    icon: '🧙',
    color: 'bg-violet-600',
    modernColor: 'bg-gradient-to-br from-violet-500 via-purple-500 to-violet-600',
    tags: ['魔法', '魔法使い/魔女', '魔法少女', '変身ヒロイン', '触手', '異種姦', '異種えっち', '蟲姦', '獣姦', '機械姦', 'ロボット/アンドロイド', '人外娘/モンスター娘', 'サキュバス/淫魔', '天使/悪魔', '妖怪', '幽霊', 'ゾンビ']
  },
  extreme: {
    name: '極端內容',
    icon: '⚠️',
    color: 'bg-red-800',
    modernColor: 'bg-gradient-to-br from-red-700 via-red-800 to-red-900',
    tags: ['レイプ', '逆レイプ', '逆レ', 'リョナ', '猟奇', '血液/流血', '狂気', '鬼畜', '丸呑み', '産卵', '出産', '妊娠/孕ませ', '腹パン', '畜えち', '合意なし', '鬱']
  }
}

// 計算屬性
const filteredTags = computed(() => {
  if (!tagSearch.value) return props.allTags
  
  const search = tagSearch.value.toLowerCase()
  return props.allTags.filter(tag => 
    tag.name.toLowerCase().includes(search)
  )
})

const categorizedFilteredTags = computed(() => {
  if (selectedCategory.value === 'all') {
    return filteredTags.value
  }
  
  const categoryTags = tagCategories[selectedCategory.value]?.tags || []
  return filteredTags.value.filter(tag =>
    categoryTags.some(categoryTag => 
      categoryTag.toLowerCase() === tag.name.toLowerCase()
    )
  )
})

const getCategoryTags = (categoryKey) => {
  const categoryTags = tagCategories[categoryKey]?.tags || []
  const filtered = filteredTags.value.filter(tag => {
    return categoryTags.some(categoryTag => 
      categoryTag.toLowerCase() === tag.name.toLowerCase()
    )
  })
  
  return filtered.sort((a, b) => b.count - a.count)
}

const getUncategorizedTags = () => {
  const allCategoryTags = new Set()
  Object.values(tagCategories).forEach(category => {
    category.tags.forEach(tag => {
      allCategoryTags.add(tag.toLowerCase())
    })
  })
  
  const uncategorized = filteredTags.value.filter(tag => {
    return !allCategoryTags.has(tag.name.toLowerCase())
  })
  
  return uncategorized.sort((a, b) => b.count - a.count)
}

// 方法
const toggleTag = (tagName) => {
  const index = selectedTags.value.indexOf(tagName)
  if (index === -1) {
    selectedTags.value.push(tagName)
  } else {
    selectedTags.value.splice(index, 1)
  }
  emitUpdate()
}

const toggleCategory = (categoryKey) => {
  if (selectedCategory.value === categoryKey) {
    // 如果點擊當前已選中的分類，回到全部分類
    selectedCategory.value = 'all'
  } else {
    // 選擇新的分類
    selectedCategory.value = categoryKey
  }
}

const removeTag = (tagName) => {
  const index = selectedTags.value.indexOf(tagName)
  if (index !== -1) {
    selectedTags.value.splice(index, 1)
    emitUpdate()
  }
}

const clearSelectedTags = () => {
  selectedTags.value = []
  emitUpdate()
}

const emitUpdate = () => {
  emit('update:modelValue', {
    selectedTags: [...selectedTags.value],
    filterMode: filterMode.value
  })
}

const applyFilter = () => {
  emit('apply', {
    selectedTags: [...selectedTags.value],
    filterMode: filterMode.value
  })
}

const resetFilter = () => {
  selectedTags.value = []
  filterMode.value = 'AND'
  tagSearch.value = ''
  emitUpdate()
  emit('reset')
}

// 自動產生組合名稱
const generateComboName = () => {
  if (selectedTags.value.length === 0) return ''
  
  // 如果只有一個標籤，直接使用該標籤名稱
  if (selectedTags.value.length === 1) {
    return selectedTags.value[0]
  }
  
  // 如果有多個標籤，找出最常見的分類
  const categoryMap = new Map()
  
  selectedTags.value.forEach(tagName => {
    // 找出標籤所屬的分類
    for (const [categoryKey, category] of Object.entries(tagCategories)) {
      if (category.tags.some(tag => tag.toLowerCase() === tagName.toLowerCase())) {
        const count = categoryMap.get(categoryKey) || 0
        categoryMap.set(categoryKey, count + 1)
        break
      }
    }
  })
  
  // 找出最多標籤的分類
  let dominantCategory = null
  let maxCount = 0
  for (const [categoryKey, count] of categoryMap.entries()) {
    if (count > maxCount) {
      maxCount = count
      dominantCategory = categoryKey
    }
  }
  
  // 產生名稱
  if (dominantCategory && maxCount >= 2) {
    const categoryName = tagCategories[dominantCategory].name
    return `${categoryName}組合 (${selectedTags.value.length}個)`
  } else {
    // 如果沒有明顯的主導分類，使用第一個標籤 + 等
    return `${selectedTags.value[0]} 等 ${selectedTags.value.length} 個標籤`
  }
}

// 標籤組合相關方法
const saveTagCombo = () => {
  if (selectedTags.value.length === 0) return
  
  // 如果沒有輸入名稱，自動產生
  const comboName = newComboName.value.trim() || generateComboName()
  
  const combo = {
    id: Date.now(),
    name: comboName,
    tags: [...selectedTags.value],
    mode: filterMode.value,
    createdAt: new Date().toISOString()
  }
  
  savedCombos.value.push(combo)
  newComboName.value = ''
  
  // 保存到 localStorage
  localStorage.setItem('tagCombos', JSON.stringify(savedCombos.value))
}

const loadTagCombo = (combo) => {
  selectedTags.value = [...combo.tags]
  filterMode.value = combo.mode
  emitUpdate()
}

const deleteTagCombo = (comboId) => {
  const index = savedCombos.value.findIndex(combo => combo.id === comboId)
  if (index !== -1) {
    savedCombos.value.splice(index, 1)
    localStorage.setItem('tagCombos', JSON.stringify(savedCombos.value))
  }
}

// 監聽器
watch(filterMode, () => {
  emitUpdate()
})

watch(() => props.modelValue, (newValue) => {
  selectedTags.value = [...newValue.selectedTags]
  filterMode.value = newValue.filterMode
}, { deep: true })

// 生命週期
onMounted(() => {
  // 從 localStorage 載入保存的組合
  const saved = localStorage.getItem('tagCombos')
  if (saved) {
    try {
      savedCombos.value = JSON.parse(saved)
    } catch (e) {
      console.error('Failed to load saved tag combos:', e)
    }
  }
})
</script>

<style scoped>
.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background: rgba(0, 210, 255, 0.5);
  border-radius: 3px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 210, 255, 0.7);
}

.animate-slide-up {
  animation: slideUp 0.3s ease-out forwards;
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