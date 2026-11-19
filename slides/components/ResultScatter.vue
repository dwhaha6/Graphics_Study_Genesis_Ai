<script setup lang="ts">
import { computed, ref } from 'vue'

// Paper Table 1 (long video generation): Subjective Quality (x) vs Camera Controllability (y).
// Yume-1.5 / HY-WorldPlay have no camera-control score ("--") and are omitted. Ours DMD omitted (overlaps Ours).
type Pt = { n: string, x: number, y: number, ours?: boolean, dx?: number, dy?: number }
const data: Record<string, Pt[]> = {
  DL3DV: [
    { n: 'GEN3C', x: 24.60, y: 69.54 }, { n: 'CaM', x: 35.19, y: 42.71 }, { n: 'VMem', x: 18.54, y: 0.68 },
    { n: 'SPMem', x: 38.32, y: 62.05, dx: -26, dy: 4 }, { n: 'Lyra 2.0', x: 44.54, y: 64.67, ours: true },
  ],
  'Tanks and Temples': [
    { n: 'GEN3C', x: 21.75, y: 70.91 }, { n: 'CaM', x: 34.22, y: 31.86 }, { n: 'VMem', x: 16.21, y: 0.00 },
    { n: 'SPMem', x: 34.41, y: 45.07 }, { n: 'Lyra 2.0', x: 43.35, y: 63.87, ours: true },
  ],
}
const ds = ref<keyof typeof data>('DL3DV')
const W = 420; const H = 250; const L = 40; const R = 14; const T = 12; const B = 34
const x = (v: number) => L + v / 50 * (W - L - R)
const y = (v: number) => T + (1 - v / 80) * (H - T - B)
const pts = computed(() => data[ds.value])
const hov = ref<Pt | null>(null)
</script>

<template>
  <div class="rs">
    <div class="ctrl">
      <span class="lb">데이터셋</span>
      <button v-for="k in Object.keys(data)" :key="k" :class="{ on: ds === k }" @click="ds = k as keyof typeof data">{{ k }}</button>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" class="ch" @mouseleave="hov = null">
      <rect :x="x(40.5)" :y="y(80)" :width="x(50) - x(40.5)" :height="y(55) - y(80)" class="good" />
      <text :x="x(49.5)" :y="y(78)" class="gl" text-anchor="end">둘 다 좋음 ↗</text>
      <g v-for="g in [0, 20, 40, 60, 80]" :key="`y${g}`">
        <line :x1="L" :x2="W - R" :y1="y(g)" :y2="y(g)" class="grid" />
        <text :x="L - 6" :y="y(g) + 3" class="ax" text-anchor="end">{{ g }}</text>
      </g>
      <text v-for="g in [0, 10, 20, 30, 40, 50]" :key="`x${g}`" :x="x(g)" :y="H - B + 14" class="ax" text-anchor="middle">{{ g }}</text>
      <text :x="(L + W - R) / 2" :y="H - 4" class="at" text-anchor="middle">한 장면 화질 (Subjective Quality) →</text>
      <text :x="12" :y="(T + H - B) / 2" class="at" text-anchor="middle" :transform="`rotate(-90 12 ${(T + H - B) / 2})`">카메라 제어 →</text>
      <g v-for="p in pts" :key="p.n" @mouseenter="hov = p">
        <circle :cx="x(p.x)" :cy="y(p.y)" r="14" fill="transparent" />
        <circle :cx="x(p.x)" :cy="y(p.y)" :r="p.ours ? 7 : 5.5" :class="['mk', { ours: p.ours }]" />
        <text :x="x(p.x) + (p.dx ?? 0)" :y="y(p.y) - 10 + (p.dy ?? 0)" class="dl" :class="{ ours: p.ours }" text-anchor="middle">{{ p.n }}</text>
      </g>
    </svg>
    <div class="tip">
      <template v-if="hov">{{ hov.n }} · 화질 <b>{{ hov.x.toFixed(2) }}</b> · 카메라 제어 <b>{{ hov.y.toFixed(2) }}</b></template>
      <template v-else>점에 마우스를 올리면 값 · Yume-1.5, HY-WorldPlay는 카메라 제어 점수 없음 (명시적인 카메라 경로 조건을 지원하지 않음)</template>
    </div>
  </div>
</template>

<style scoped>
.rs { display: flex; flex-direction: column; gap: .3rem; }
.ctrl { display: flex; align-items: center; gap: .35rem; }
.lb { font-size: .7rem; color: var(--lx-muted); }
.ctrl button { font-size: .7rem; padding: .12rem .55rem; border-radius: 6px; background: var(--lx-panel2); border: 1px solid var(--lx-line); }
.ctrl button.on { background: var(--lx-accent); color: #0d1117; border-color: var(--lx-accent); font-weight: 700; }
.ch { width: 100%; background: var(--lx-panel); border: 1px solid var(--lx-line); border-radius: 10px; }
.grid { stroke: #30363d; stroke-width: 1; }
.ax { font-size: 9px; fill: var(--lx-muted); }
.at { font-size: 9.5px; fill: var(--lx-muted); }
.good { fill: #5eead4; opacity: .07; }
.gl { font-size: 9px; fill: var(--lx-accent); opacity: .8; }
.mk { fill: #8b949e; stroke: var(--lx-panel); stroke-width: 2; }
.mk.ours { fill: var(--lx-accent); }
.dl { font-size: 10px; fill: var(--lx-text); }
.dl.ours { font-weight: 700; fill: var(--lx-accent); }
.tip { font-size: .7rem; color: var(--lx-muted); min-height: 1.1rem; }
.tip b { color: var(--lx-text); }
</style>
