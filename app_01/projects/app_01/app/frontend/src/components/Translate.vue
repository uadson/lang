<template>
  <div class="min-h-screen p-4 relative overflow-hidden gradient-bg">
    <!-- Floating Orbs -->
    <FloatingOrb v-for="(orb, index) in orbs" :key="index" :size="orb.size" :position="orb.position"
      :delay="orb.delay" />

    <!-- Main Container -->
    <div class="max-w-4xl mx-auto pt-8">
      <!-- Header -->
      <PageHeader />

      <!-- Main Translation Card -->
      <div class="glass rounded-3xl p-8 mb-6 shine">
        <!-- Language Selectors -->
        <LanguageSelector :sourceLanguage="sourceLanguage" :targetLanguage="targetLanguage" :languages="languages"
          @update:sourceLanguage="sourceLanguage = $event" @update:targetLanguage="targetLanguage = $event"
          @swap="swapLanguages" />

        <!-- Text Areas -->
        <TranslationArea :sourceText="sourceText" :translatedText="translatedText" :isTranslating="isTranslating"
          :sourceLanguage="getLanguageInfo(sourceLanguage)" :targetLanguage="getLanguageInfo(targetLanguage)"
          @update:sourceText="handleSourceTextUpdate" @clear="clearText" @copy="copyToClipboard" />

        <!-- Action Button -->
        <div class="mt-6 text-center">
          <button @click="translateText" :disabled="!sourceText.trim() || isTranslating"
            class="glass-button px-8 py-3 rounded-xl text-white font-medium disabled:opacity-50 disabled:cursor-not-allowed shine">
            <span v-if="isTranslating">
              🔄 Traduzindo...
            </span>
            <span v-else>
              ✨ Traduzir
            </span>
          </button>
        </div>
      </div>

      <!-- Feature Cards -->
      <FeatureCards />
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import FloatingOrb from './FloatingOrb.vue'
import PageHeader from './PageHeader.vue'
import LanguageSelector from './LanguageSelector.vue'
import TranslationArea from './TranslationArea.vue'
import FeatureCards from './FeatureCards.vue'
import { useTranslator } from '../composables/useTranslator'
import { languages } from '../data/languages'

export default {
  name: 'TranslatorPage',
  components: {
    FloatingOrb,
    PageHeader,
    LanguageSelector,
    TranslationArea,
    FeatureCards
  },
  setup() {
    const orbs = ref([
      { size: 80, position: { top: '10%', left: '10%' }, delay: 0 },
      { size: 120, position: { top: '60%', right: '15%' }, delay: 2 },
      { size: 60, position: { bottom: '20%', left: '20%' }, delay: 4 }
    ])

    const {
      sourceText,
      translatedText,
      sourceLanguage,
      targetLanguage,
      isTranslating,
      translateText,
      swapLanguages,
      clearText,
      copyToClipboard
    } = useTranslator()

    const getLanguageInfo = (code) => {
      return languages.find(lang => lang.code === code) || { name: 'Selecione o idioma', flag: '🌐' }
    }

    const handleSourceTextUpdate = (text) => {
      sourceText.value = text
      if (text.trim()) {
        translateText()
      }
    }

    return {
      orbs,
      sourceText,
      translatedText,
      sourceLanguage,
      targetLanguage,
      isTranslating,
      languages,
      translateText,
      swapLanguages,
      clearText,
      copyToClipboard,
      getLanguageInfo,
      handleSourceTextUpdate
    }
  }
}
</script>