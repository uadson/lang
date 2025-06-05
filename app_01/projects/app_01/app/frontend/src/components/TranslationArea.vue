<template>
    <div class="grid md:grid-cols-2 gap-6">
        <!-- Source Text -->
        <div class="space-y-3">
            <div class="flex items-center justify-between">
                <h3 class="text-white font-medium">
                    {{ sourceLanguage.flag }} {{ sourceLanguage.name }}
                </h3>
                <button @click="$emit('clear')" class="text-white/60 hover:text-white transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                        </path>
                    </svg>
                </button>
            </div>
            <textarea :value="sourceText" @input="$emit('update:sourceText', $event.target.value)"
                placeholder="Digite o texto para traduzir..."
                class="w-full h-32 glass-input rounded-xl p-4 text-white placeholder-white/50 resize-none focus:outline-none focus:ring-2 focus:ring-white/30 transition-all"></textarea>
            <div class="text-white/60 text-sm">
                {{ sourceText.length }} caracteres
            </div>
        </div>

        <!-- Translated Text -->
        <div class="space-y-3">
            <div class="flex items-center justify-between">
                <h3 class="text-white font-medium">
                    {{ targetLanguage.flag }} {{ targetLanguage.name }}
                </h3>
                <button @click="$emit('copy', translatedText)" class="text-white/60 hover:text-white transition-colors"
                    v-if="translatedText">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z">
                        </path>
                    </svg>
                </button>
            </div>
            <div class="w-full h-32 glass-input rounded-xl p-4 text-white relative overflow-hidden">
                <LoadingSpinner v-if="isTranslating" />
                <div v-else-if="translatedText" class="whitespace-pre-wrap">
                    {{ translatedText }}
                </div>
                <div v-else class="text-white/50 italic">
                    A tradução aparecerá aqui...
                </div>
            </div>
            <div class="text-white/60 text-sm">
                {{ translatedText.length }} caracteres
            </div>
        </div>
    </div>
</template>

<script>
import LoadingSpinner from './LoadingSpinner.vue'

export default {
    name: 'TranslationArea',
    components: {
        LoadingSpinner
    },
    props: {
        sourceText: String,
        translatedText: String,
        isTranslating: Boolean,
        sourceLanguage: Object,
        targetLanguage: Object
    },
    emits: ['update:sourceText', 'clear', 'copy']
}
</script>