<template>
    <div class="floating-orb" :style="orbStyles"></div>
</template>

<script>
import { computed } from 'vue'

export default {
    name: 'FloatingOrb',
    props: {
        size: {
            type: Number,
            required: true
        },
        position: {
            type: Object,
            required: true
        },
        delay: {
            type: Number,
            default: 0
        }
    },
    setup(props) {
        const orbStyles = computed(() => ({
            width: `${props.size}px`,
            height: `${props.size}px`,
            animationDelay: `${props.delay}s`,
            ...props.position
        }))

        return {
            orbStyles
        }
    }
}
</script>