<script setup lang="ts">
defineProps<{ src: string, alt?: string }>()
const base = import.meta.env.BASE_URL
</script>

<template>
  <img :src="base + src" :alt="alt ?? ''" draggable="false">
</template>
