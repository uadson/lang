<template>
    <div class="flex items-center justify-between mb-6 flex-wrap gap-4">
        <div class="flex-1 min-w-[200px]">
            <label class="block text-white font-medium mb-2">
                Traduzir de
            </label>
            <select :value="sourceLanguage" @change="$emit('update:sourceLanguage', $event.target.value)"
                class="w-full glass-dropdown rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-white/30 transition-all">
                <option v-for="lang in languages" :key="lang.code" :value="lang.code" class="bg-gray-800 text-white">
                    {{ lang.flag }} {{ lang.name }}
                </option>
            </select>
        </div>

        <!-- Swap Button -->
        <button @click="$emit('swap')"
            class="glass-button rounded-full p-3 text-white hover:text-blue-200 transition-all transform hover:rotate-180 duration-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m0-4l4-4"></path>
            </svg>
        </button>

        <div class="flex-1 min-w-[200px]">
            <label class="block text-white font-medium mb-2">
                para
            </label>
            <select :value="targetLanguage" @change="$emit('update:targetLanguage', $event.target.value)"
                class="w-full glass-dropdown rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-white/30 transition-all">
                <option v-for="lang in languages" :key="lang.code" :value="lang.code" class="bg-gray-800 text-white">
                    {{ lang.flag }} {{ lang.name }}
                </option>
            </select>
        </div>
    </div>
</template>

<script>
export default {
    name: 'LanguageSelector',
    props: {
        sourceLanguage: String,
        targetLanguage: String,
        languages: Array
    },
    emits: ['update:sourceLanguage', 'update:targetLanguage', 'swap']
}
</script>