<template>
    <div class="flex items-center justify-center h-full">
        <div class="flex space-x-1">
            <div class="w-2 h-2 bg-white rounded-full animate-bounce"></div>
            <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'LoadingSpinner'
}
</script>