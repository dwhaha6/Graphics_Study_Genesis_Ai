<script setup lang="ts">
import { computed, ref } from 'vue'

const mode = ref<'real' | 'gen'>('real')

// cameras on a ring around the scene (real capture)
const ring = Array.from({ length: 10 }, (_, i) => {
  const a = (i / 10) * Math.PI * 2 - Math.PI / 2
  return { x: 200 + Math.cos(a) * 150, y: 130 + Math.sin(a) * 100, rot: (a * 180) / Math.PI + 180 }
})
// virtual cameras along a user path (generative), each looking at the place; the last ones look at the new area
const pts = [[40, 200], [85, 225], [140, 238], [200, 240], [262, 232], [318, 210], [360, 170], [385, 120]]
const path = pts.map(([x, y], i) => {
  const [tx, ty] = i >= 6 ? [355, 70] : [200, 130]
  return { x, y, rot: (Math.atan2(ty - y, tx - x) * 180) / Math.PI }
})
const pathD = computed(() => `M${path.map(p => `${p.x} ${p.y}`).join(' L')}`)
</script>

<template>
  <div class="cc">
    <div class="tabs">
      <button :class="{ on: mode === 'real' }" @click="mode = 'real'">기존: 직접 촬영해서 복원</button>
      <button :class="{ on: mode === 'gen' }" @click="mode = 'gen'">생성 기반 복원 (Generative Reconstruction)</button>
    </div>
    <div class="body">
      <svg viewBox="0 0 430 280" class="scene">
        <!-- the place (top-down) -->
        <rect x="150" y="95" width="100" height="70" rx="6" fill="#d6c3a5" stroke="#8b7355" />
        <rect x="185" y="135" width="20" height="30" fill="#7c5a3a" />
        <circle cx="130" cy="110" r="14" fill="#4d7c4a" />
        <circle cx="272" cy="150" r="11" fill="#4d7c4a" />
        <text x="200" y="88" text-anchor="middle" class="lbl">장소</text>

        <g v-if="mode === 'real'">
          <g v-for="(c, i) in ring" :key="'r' + i" :transform="`translate(${c.x} ${c.y}) rotate(${c.rot})`" class="pop" :style="{ animationDelay: `${i * 70}ms` }">
            <path d="M0 0 L26 -12 L26 12 Z" fill="#93c5fd" opacity=".25" />
            <rect x="-6" y="-6" width="12" height="12" rx="2" fill="#93c5fd" />
          </g>
          <text x="200" y="275" text-anchor="middle" class="lbl blue">파란 카메라 = 사람이 실제로 찍은 위치</text>
        </g>

        <g v-else>
          <!-- area that was never in the photo -->
          <rect x="300" y="40" width="110" height="60" rx="6" fill="none" stroke="#5eead4" stroke-dasharray="5 4" class="pop" style="animation-delay: 900ms" />
          <text x="355" y="74" text-anchor="middle" class="lbl teal pop" style="animation-delay: 900ms">사진에 없던 곳</text>
          <path :d="pathD" fill="none" stroke="#5eead4" stroke-width="2" stroke-dasharray="6 5" />
          <g v-for="(c, i) in path" :key="'g' + i" :transform="`translate(${c.x} ${c.y}) rotate(${c.rot})`" class="pop" :style="{ animationDelay: `${i === 0 ? 0 : 150 + i * 110}ms` }">
            <path d="M0 0 L26 -12 L26 12 Z" :fill="i === 0 ? '#fbbf24' : '#5eead4'" opacity=".25" />
            <rect x="-6" y="-6" width="12" height="12" rx="2" :fill="i === 0 ? '#fbbf24' : 'none'" :stroke="i === 0 ? 'none' : '#5eead4'" stroke-width="2" />
          </g>
          <text x="40" y="180" text-anchor="middle" class="lbl warn">사진 1장</text>
          <text x="215" y="275" text-anchor="middle" class="lbl teal">점선 = 사용자가 정한 카메라 경로 · 빈 카메라 = AI가 만든 가상 촬영</text>
        </g>
      </svg>

      <div class="explain">
        <template v-if="mode === 'real'">
          <div class="step"><b>1</b> 현장에 가서 여러 각도로 <span class="hl-b">직접 촬영</span></div>
          <div class="step"><b>2</b> 찍은 사진들로 3D 복원</div>
          <div class="step"><b>3</b> 찍은 곳만 3D로 만들 수 있음</div>
          <p class="note">많은 장면을 만들려면 그만큼 촬영이 필요함</p>
        </template>
        <template v-else>
          <div class="step"><b>1</b> <span class="hl-y">사진 1장</span> + 카메라가 지나갈 길</div>
          <div class="step"><b>2</b> 영상 생성 모델이 그 길을 걷는 영상을 만듦 = <span class="hl-t">가상 촬영</span></div>
          <div class="step"><b>3</b> 만든 영상의 프레임들로 3D 복원</div>
          <p class="note">촬영 없이 다양한 장면을 대량으로 만들 수 있고, 상상 속 장소도 가능</p>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cc { display: flex; flex-direction: column; gap: .6rem; }
.tabs { display: flex; gap: .5rem; }
.tabs button { font-size: .8rem; padding: .3rem .8rem; border-radius: 8px; border: 1px solid var(--lx-line); color: var(--lx-muted); background: var(--lx-panel); }
.tabs button.on { color: #0d1117; background: var(--lx-accent); border-color: var(--lx-accent); font-weight: 700; }
.body { display: grid; grid-template-columns: 1.15fr 1fr; gap: 1.2rem; align-items: center; }
.scene { width: 100%; background: var(--lx-panel); border: 1px solid var(--lx-line); border-radius: 12px; }
.lbl { font-size: 11px; fill: var(--lx-muted); }
.lbl.blue { fill: #93c5fd; } .lbl.teal { fill: #5eead4; } .lbl.warn { fill: #fbbf24; font-weight: 700; }
.explain { display: flex; flex-direction: column; gap: .55rem; }
.step { font-size: .95rem; line-height: 1.45; }
.step b { display: inline-grid; place-items: center; width: 1.4rem; height: 1.4rem; border-radius: 50%; background: var(--lx-panel2); border: 1px solid var(--lx-line); font-size: .75rem; margin-right: .4rem; }
.note { font-size: .8rem; color: var(--lx-muted); margin-top: .3rem; }
.hl-b { color: #93c5fd; font-weight: 700; } .hl-y { color: #fbbf24; font-weight: 700; } .hl-t { color: #5eead4; font-weight: 700; }
.pop { opacity: 0; animation: pop .35s ease forwards; }
@keyframes pop { to { opacity: 1; } }
</style>
