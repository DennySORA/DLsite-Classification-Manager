<template>
  <div class="container">
    <div class="grid grid-cols-1 gap-2 px-5 pt-5">
      <div
        class="flex flex-col text-center rounded-3xl border-3 border-gray-800"
        v-for="i in data"
        :key="i"
      >
        <h1 class="text-4xl pb-8 font-bold">{{ i[0] }}</h1>
        <div
          class="flex grid grid-row-3 rounded-3xl border-2 border-gray-700"
          v-for="j in Object.values(i[1].work_item)"
          :key="j"
        >
          <br />
          <h2 class="text-2xl pb-8 font-bold">{{ j.name }} - {{ j.code }}</h2>
          <div class="flex">
            <div class="p-1" v-for="k in j.info.images" :key="k">
              <img
                class="max-h-92 h-auto min-h-72 w-7xl rounded-3xl border-2 border-gray-500 object-contain"
                :src="'image?path=' + j.info.path + '\\' + k"
              />
            </div>
          </div>
          <div class="flex flex-wrap font-bold rounded-3xl border-3 border-gray-600">
            <div class="p-5" v-for="k in Object.entries(j.info.tag)" :key="k">
              <div v-if="k[1]" class="flex">
                <h3 class="self-center text-2xl inline pr-8">{{ k[0] }}:</h3>
                <div
                  class="self-center mt-2 overflow-auto whitespace-pre-wrap max-h-50 inline-block max-w-screen mix-w-50"
                  v-if="typeof k[1] == 'string'"
                >{{ k[1] }}</div>
                <div
                  class="text-2xl px-3"
                  v-for="s in Object.entries(k[1])"
                  :key="s"
                  v-else
                >{{ s[0] }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'HomeIndex',
  setup() {
    let data = ref({});
    return {
      data
    }
  },
  mounted() {
    this.axios.get('/api?limit=1000').then((response) => {
      this.data = response.data;
      console.log(response.data)
    })
  },

}
</script>

