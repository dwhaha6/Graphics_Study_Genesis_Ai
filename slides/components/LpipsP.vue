<script setup lang="ts">
import { ref } from 'vue'
// Paper Table 2 (3D scene generation), DL3DV, LPIPS-P (lower = better). Every method reconstructed with DAv3.
const rows = [
  { n: 'Yume-1.5 + DAv3', v: 0.598 },
  { n: 'VMem + DAv3', v: 0.593 },
  { n: 'GEN3C + DAv3', v: 0.504 },
  { n: 'CaM + DAv3', v: 0.433 },
  { n: 'SPMem + DAv3', v: 0.419 },
  { n: 'Lyra 2.0 + 원래 DAv3', v: 0.413, o: 1 },
  { n: 'Lyra 2.0 (Fine-tuned DAv3)', v: 0.381, o: 2 },
]
const max = 0.65
const hov = ref<number | null>(null)
</script>

<template>
  <div class="lp">
    <div v-for="(r, i) in rows" :key="r.n" class="row" :class="{ dim: hov !== null && hov !== i }" @mouseenter="hov = i" @mouseleave="hov = null">
      <span class="nm" :class="{ o: r.o }">{{ r.n }}</span>
      <div class="tr"><div class="bar" :style="{ width: `${(r.v / max) * 100}%`, background: r.o === 2 ? 'var(--lx-accent)' : r.o === 1 ? 'rgba(94,234,212,.5)' : '#8b949e' }" /></div>
      <span class="v" :class="{ o: r.o === 2 }">{{ r.v.toFixed(3) }}</span>
    </div>
  </div>
</template>

<style scoped>
.lp { font-size: .6rem; }
.row { display: grid; grid-template-columns: 8.6rem 1fr 2.1rem; align-items: center; gap: .35rem; height: 13px; transition: opacity .15s; }
.nm { white-space: nowrap; color: var(--lx-muted); }
.nm.o { color: var(--lx-text); font-weight: 700; }
.tr { height: 8px; background: #232a35; border-radius: 4px; overflow: hidden; }
.bar { height: 100%; border-radius: 4px; }
.v { text-align: right; font-variant-numeric: tabular-nums; }
.v.o { color: var(--lx-accent); font-weight: 700; }
.dim { opacity: .4; }
</style>
