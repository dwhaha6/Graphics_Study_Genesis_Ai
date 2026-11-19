<script setup lang="ts">
import { ref } from 'vue'

// Paper appendix figure (target-view coverage vs. number of retrieved frames), mean values re-plotted.
const data = [28.9, 36.3, 39.5, 41.4, 42.6, 43.4, 44.0, 44.4, 44.7, 45.0]
const W = 300; const H = 150; const L = 26; const R = 8; const T = 8; const B = 26; const PAD = 16; const YMAX = 60
const x = (n: number) => L + PAD + (n - 1) / 9 * (W - L - R - 2 * PAD)
const y = (v: number) => T + (1 - v / YMAX) * (H - T - B)
const path = data.map((v, i) => `${i ? 'L' : 'M'}${x(i + 1).toFixed(1)} ${y(v).toFixed(1)}`).join(' ')
const labeled = [1, 5, 10]
const hover = ref<number | null>(null)
</script>

<template>
  <div class="nc">
    <div class="ttl">가져온 장수 → 목표 화면 커버율 (%) <span class="mu">· 논문 실험 평균</span></div>
    <svg :viewBox="`0 0 ${W} ${H}`" class="ch" @mouseleave="hover = null">
      <g v-for="g in [0, 20, 40, 60]" :key="g">
        <line :x1="L" :x2="W - R" :y1="y(g)" :y2="y(g)" class="grid" />
        <text :x="L - 5" :y="y(g) + 3" class="ax" text-anchor="end">{{ g }}</text>
      </g>
      <text v-for="n in 10" :key="`x${n}`" :x="x(n)" :y="H - B + 13" class="ax" text-anchor="middle">{{ n }}</text>
      <text :x="(L + W - R) / 2" :y="H - 2" class="ax" text-anchor="middle">가져온 과거 프레임 수 (장)</text>
      <line v-if="hover" :x1="x(hover)" :x2="x(hover)" :y1="T" :y2="H - B" class="cross" />
      <path :d="path" class="ln" />
      <circle v-for="(v, i) in data" :key="i" :cx="x(i + 1)" :cy="y(v)" :r="i + 1 === 5 ? 4.5 : 3" :class="['mk', { five: i + 1 === 5 }]" />
      <text v-for="n in labeled" :key="`l${n}`" :x="x(n)" :y="y(data[n - 1]) - 9" class="dl" text-anchor="middle">{{ data[n - 1].toFixed(1) }}%</text>
      <rect v-for="n in 10" :key="`h${n}`" :x="x(n) - 12" :y="T" width="24" :height="H - T - B" fill="transparent" @mouseenter="hover = n" />
    </svg>
    <div class="tip">
      <template v-if="hover">{{ hover }}장 → 커버율 <b>{{ data[hover - 1].toFixed(1) }}%</b></template>
      <template v-else>5장 <b>42.6%</b> · 10장으로 두 배 늘려도 <b>45.0%</b></template>
    </div>
  </div>
</template>

<style scoped>
.nc { display: flex; flex-direction: column; gap: .2rem; }
.ttl { font-size: .78rem; font-weight: 700; }
.mu { color: var(--lx-muted); font-weight: 400; }
.ch { width: 100%; }
.grid { stroke: #30363d; stroke-width: 1; }
.ax { font-size: 8.5px; fill: var(--lx-muted); }
.ln { fill: none; stroke: #3987e5; stroke-width: 2; }
.mk { fill: #3987e5; stroke: var(--lx-panel); stroke-width: 2; }
.mk.five { fill: var(--lx-accent); }
.dl { font-size: 9px; fill: var(--lx-text); font-weight: 700; }
.cross { stroke: var(--lx-muted); stroke-width: 1; stroke-dasharray: 3 3; }
.tip { font-size: .72rem; color: var(--lx-muted); min-height: 1.1rem; }
.tip b { color: var(--lx-text); }
</style>
