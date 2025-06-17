<template>
  <div class="bg-gray-200 flex items-center justify-center min-h-screen p-4">
    <form @submit.prevent="tranlationForm" class="bg-white p-6 rounded-xl shadow-lg w-full max-w-4xl space-y-6">
      <h2 class="text-2xl font-semibold text-center mb-4">Usando LLM para tradução de textos</h2>
      <div class="flex flex-wrap items-center justify-center gap-4">
        <label class="text-lg font-medium">Traduzir de</label>
        <select v-model="form.source_language_id"
          class="px-4 py-2 rounded-md border border-gray-300 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="">Selecione o idioma</option>
          <option v-for="lang in languages" :key="lang.id" :value="lang.id">
            {{ lang.name }}
          </option>
          <!-- Adicione outros idiomas aqui -->
        </select>
        <span class="text-lg font-medium">para</span>
        <select v-model="form.target_language_id"
          class="px-4 py-2 rounded-md border border-gray-300 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="">Selecione o idioma</option>
          <option v-for="lang in languages" :key="lang.id" :value="lang.id">
            {{ lang.name }}
          </option>
          <!-- Adicione outros idiomas aqui -->
        </select>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <textarea v-model="form.text"
          class="w-full h-60 p-4 border border-gray-300 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Digite o texto aqui..."></textarea>
        <textarea v-model="translatedText"
          class="w-full h-60 p-4 border border-gray-300 rounded-md resize-none bg-gray-100" readonly
          placeholder="Tradução aparecerá aqui..."></textarea>
      </div>

      <div class="text-center">
        <button
          class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-md text-lg shadow-md transition duration-200 ease-in-out">
          <span v-if="!isLoading" class="flex items-center justify-center">
            Traduzir
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="ml-2">
              <path d="M5 12h14" />
              <path d="m12 5 7 7-7 7" />
            </svg>
          </span>
          <span v-else class="flex items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            Traduzindo...
          </span>
        </button>
      </div>
    </form>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const languages = ref([])
const translatedText = ref("")
const isLoading = ref(false)
const form = ref({
  text: "",
  source_language_id: "",
  target_language_id: ""
})

const fetchLanguages = async () => {
  try {
    const response = await api.get('/languages/')
    languages.value = response.data
  } catch (error) {
    console.error('Erro ao buscar idiomas:', error)
  }
}

const tranlationForm = async () => {
  isLoading.value = true
  try {
    await api.post('/translate/', form.value)
    const response = await api.post('/translate/', form.value)
    translatedText.value = response.data.translated_text
  } catch (error) {
    console.error('Erro ao traduzir:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchLanguages)

</script>