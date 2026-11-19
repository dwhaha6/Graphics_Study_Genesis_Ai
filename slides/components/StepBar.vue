<script setup lang="ts">
// Small progress bar for a multi-slide part: highlights the current step.
defineProps<{ steps: string[], cur: number }>()
</script>

<template>
  <div class="sb">
    <template v-for="(s, i) in steps" :key="i">
      <span :class="{ on: i === cur, done: i < cur }">{{ s }}</span>
      <i v-if="i < steps.length - 1">›</i>
    </template>
  </div>
</template>

<style scoped>
.sb { position: absolute; top: 1.15rem; right: 2.2rem; display: flex; align-items: center; gap: .35rem; font-size: .64rem; color: var(--lx-muted); }
.sb span { padding: .08rem .45rem; border-radius: 999px; border: 1px solid var(--lx-line); }
.sb span.done { color: var(--lx-text); }
.sb span.on { color: #0d1117; background: var(--lx-accent); border-color: var(--lx-accent); font-weight: 700; }
.sb i { font-style: normal; opacity: .6; }
</style>
