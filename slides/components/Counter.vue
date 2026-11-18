<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ start?: number }>()
const count = ref(props.start ?? 0)
</script>

<template>
  <div class="flex items-center gap-4 text-2xl">
    <button class="px-4 py-1 border rounded" @click="count--">−</button>
    <span class="font-mono w-16 text-center">{{ count }}</span>
    <button class="px-4 py-1 border rounded" @click="count++">+</button>
  </div>
</template>
