<script setup lang="ts">
import { computed, ref } from 'vue'

// Concept demo for §3 camera conditioning: depth warping loses its signal when the view no longer overlaps,
// Plücker rays are always computable from the camera. 2D top-down toy with a 70° FOV and pure rotation.
const props = defineProps<{ src: string }>()
const base = import.meta.env.BASE_URL
const FOV = 70
const a = ref(0)
const cx = 150; const cy = 106; const R = 92
const rad = (d: number) => d * Math.PI / 180
const pt = (d: number) => `${(cx + R * Math.sin(rad(d))).toFixed(1)} ${(cy - R * Math.cos(rad(d))).toFixed(1)}`
const wedge = (d: number) => `M${cx} ${cy} L${pt(d - FOV / 2)} A${R} ${R} 0 0 1 ${pt(d + FOV / 2)} Z`
const overlap = computed(() => Math.max(0, 1 - a.value / FOV))
const hue = (d: number) => Math.round(200 + d * 1.6)
const ray = computed(() => `linear-gradient(180deg, rgba(255,255,255,.28), rgba(0,0,0,.35)), linear-gradient(90deg, hsl(${hue(a.value - FOV / 2)} 70% 55%), hsl(${hue(a.value)} 70% 55%), hsl(${hue(a.value + FOV / 2)} 70% 55%))`)
const status = computed(() => {
  if (overlap.value >= 0.5) return '대부분 겹침 → 옮겨 그린 그림이 충분한 힌트 (논문: Wan 2.1에서는 이것만으로도 긴 경로의 카메라 제어가 정확)'
  if (overlap.value > 0) return '겹치는 부분이 줄어 옮겨 그린 힌트가 일부만 남음'
  return '겹침 0 → 옮겨 올 픽셀이 없어 힌트가 완전히 사라지고 화질도 크게 떨어짐 → Plücker ray가 "어디를 보는지"만은 계속 알려 줌'
})
</script>

<template>
  <div class="cc">
    <div class="left">
      <svg viewBox="0 0 300 200" class="top">
        <rect x="112" y="6" width="40" height="22" rx="3" class="obj" />
        <rect x="166" y="4" width="46" height="26" rx="3" class="obj" />
        <rect x="262" y="78" width="28" height="44" rx="3" class="obj b" />
        <rect x="216" y="172" width="46" height="22" rx="3" class="obj c" />
        <rect x="10" y="80" width="28" height="44" rx="3" class="obj d" />
        <path :d="wedge(0)" class="prev" />
        <path :d="wedge(a)" class="tgt" />
        <circle :cx="cx" :cy="cy" r="7" fill="#fbbf24" stroke="#0d1117" stroke-width="2" />
        <text x="8" y="180" class="lg"><tspan class="g">■</tspan> 직전 프레임이 본 곳</text>
        <text x="8" y="194" class="lg"><tspan class="bl">■</tspan> 새로 찍을 시점</text>
      </svg>
      <div class="ctrl">
        <span class="lab">카메라 회전 {{ a }}°</span>
        <input v-model.number="a" type="range" min="0" max="180" step="5">
      </div>
      <p class="status">{{ status }}</p>
    </div>
    <div class="right">
      <div>
        <div class="cap">① Depth-based warping <span class="mu">(GEN3C 방식)</span></div>
        <div class="thumb warp"><img v-show="overlap > 0" :src="base + props.src" :style="{ transform: `translateX(${-(1 - overlap) * 100}%)` }" draggable="false"></div>
        <div class="bar"><i :style="{ width: `${overlap * 100}%` }" class="g" /></div>
        <div class="mu sm">직전 프레임을 깊이로 새 시점에 옮겨 그린 그림 · 검은 곳 = 옮겨 올 픽셀 없음 · 남은 힌트 {{ Math.round(overlap * 100) }}%</div>
      </div>
      <div>
        <div class="cap">② Plücker ray <span class="mu">(CameraCtrl 방식)</span></div>
        <div class="thumb" :style="{ background: ray }" />
        <div class="bar"><i style="width: 100%" class="bl" /></div>
        <div class="mu sm">픽셀마다 "어느 방향을 보는 광선인지"를 숫자로 (여기선 색으로 표시) · 카메라만 알면 항상 계산됨 · 색·모양 정보는 없음</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cc { display: grid; grid-template-columns: 1fr 1.1fr; gap: 1.1rem; align-items: start; }
.left { display: flex; flex-direction: column; gap: .35rem; }
.top { width: 100%; background: var(--lx-panel); border: 1px solid var(--lx-line); border-radius: 12px; }
.obj { fill: #8d7b68; } .obj.b { fill: #6b8f71; } .obj.c { fill: #7c6fa8; } .obj.d { fill: #a0705f; }
.prev { fill: #22c55e; fill-opacity: .18; stroke: #22c55e; stroke-width: 1.5; stroke-dasharray: 5 4; }
.tgt { fill: #3b82f6; fill-opacity: .22; stroke: #60a5fa; stroke-width: 2; transition: d .2s; }
.lg { fill: var(--lx-muted); font-size: 10px; }
.lg .g { fill: #22c55e; } .lg .bl { fill: #60a5fa; }
.ctrl { display: flex; align-items: center; gap: .6rem; }
.ctrl input { flex: 1; accent-color: var(--lx-accent); }
.lab { font-weight: 700; font-size: .8rem; min-width: 6.5rem; }
.right { display: flex; flex-direction: column; gap: .55rem; }
.cap { font-weight: 700; font-size: .85rem; margin-bottom: .2rem; }
.thumb { aspect-ratio: 832 / 200; border-radius: 8px; overflow: hidden; border: 1px solid var(--lx-line); }
.thumb.warp { background: #000; }
.thumb img { width: 100%; height: 100%; object-fit: cover; transition: transform .2s; }
.bar { height: 6px; background: var(--lx-panel2); border-radius: 3px; margin-top: .3rem; overflow: hidden; }
.bar i { display: block; height: 100%; transition: width .2s; }
.bar .g { background: #22c55e; } .bar .bl { background: #60a5fa; }
.mu { color: var(--lx-muted); font-weight: 400; }
.sm { font-size: .7rem; line-height: 1.4; margin-top: .2rem; }
.status { font-size: .78rem; line-height: 1.45; margin: .1rem 0 0; min-height: 2.3rem; }
</style>
