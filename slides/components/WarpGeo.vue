<script setup lang="ts">
import { computed, ref } from 'vue'

// Top-down concept demo of depth warping (forward warp):
// past camera A sees one 1D image row (pixel + depth). Each pixel is lifted to a 3D point and re-projected into new camera B.
const N = 56; const FOV = 64; const TAN = Math.tan(FOV / 2 * Math.PI / 180); const CY = 232
type Seg = { y: number, x0: number, x1: number, col: (x: number) => string, name: string }
const segs: Seg[] = [
  { name: '먼 건물', y: 30, x0: 0, x1: 440, col: x => (Math.floor(x / 26) % 2 ? '#a5b4c8' : '#475569') },
  { name: '집', y: 105, x0: 140, x1: 212, col: x => ((x - 140) % 18 < 7 ? '#fde68a' : '#c2410c') },
  { name: '기둥', y: 168, x0: 226, x1: 238, col: () => '#facc15' },
]
const s = ref(40)
const sel = ref(49)
const A = { x: 200, y: CY }
const B = computed(() => ({ x: 200 + s.value, y: CY }))

const ray = computed(() => Array.from({ length: N }, (_, c) => { // what A sees per pixel
  const xi = ((c + 0.5) / N * 2 - 1) * TAN
  let best: { t: number, x: number, y: number, col: string } | null = null
  for (const g of segs) {
    const t = (CY - g.y); const x = A.x + t * xi
    if (x >= g.x0 && x <= g.x1 && (!best || t < best.t)) best = { t, x, y: g.y, col: g.col(x) }
  }
  return best!
}))
const proj = (P: { x: number, y: number }) => {
  const d = CY - P.y; const xi = (P.x - B.value.x) / d / TAN
  return Math.abs(xi) <= 1 ? { c: Math.min(N - 1, Math.floor((xi + 1) / 2 * N)), d } : null
}
const warped = computed(() => { // per B pixel: source A pixel index or -1
  const out = new Array(N).fill(-1); const zb = new Array(N).fill(1e9)
  ray.value.forEach((p, c) => {
    const q = proj(p); if (!q) return
    if (q.d < zb[q.c]) { zb[q.c] = q.d; out[q.c] = c }
  })
  return out
})
const target = computed(() => { const p = ray.value[sel.value]; return { p, q: proj(p) } })
const visibleFromB = computed(() => target.value.q && warped.value[target.value.q.c] === sel.value)
const holes = computed(() => warped.value.filter(i => i < 0).length)
const wedge = (C: { x: number, y: number }) => `M${C.x} ${C.y} L${C.x - 200 * TAN} ${C.y - 200} M${C.x} ${C.y} L${C.x + 200 * TAN} ${C.y - 200}`
const pickB = (c: number) => { if (warped.value[c] >= 0) sel.value = warped.value[c] }
</script>

<template>
  <div class="wg">
    <div class="left">
      <svg viewBox="0 0 440 250" class="map">
        <template v-for="g in segs" :key="g.name">
          <line v-for="k in Math.ceil((g.x1 - g.x0) / 2)" :key="k" :x1="g.x0 + (k - 1) * 2" :x2="Math.min(g.x1, g.x0 + k * 2)" :y1="g.y" :y2="g.y" :stroke="g.col(g.x0 + (k - 1) * 2 + 1)" stroke-width="7" />
          <text :x="g.name === '기둥' ? g.x1 + 6 : g.x0 + 4" :y="g.y - 8" class="sl">{{ g.name }}</text>
        </template>
        <path :d="wedge(A)" class="fa" /><path :d="wedge(B)" class="fb" />
        <line :x1="A.x" :y1="A.y" :x2="target.p.x" :y2="target.p.y" class="ra" />
        <line v-if="target.q" :x1="target.p.x" :y1="target.p.y" :x2="B.x" :y2="B.y" class="rb" :class="{ blocked: !visibleFromB }" />
        <circle :cx="target.p.x" :cy="target.p.y" r="5" class="pt" />
        <polygon :points="`${A.x},${A.y - 9} ${A.x - 8},${A.y + 6} ${A.x + 8},${A.y + 6}`" fill="#e6edf3" />
        <polygon :points="`${B.x},${B.y - 9} ${B.x - 8},${B.y + 6} ${B.x + 8},${B.y + 6}`" fill="#5eead4" />
        <text :x="A.x + (s >= 0 ? -10 : 10)" :y="A.y + 4" class="cl" :text-anchor="s >= 0 ? 'end' : 'start'">A (과거, s)</text>
        <text :x="B.x + (s >= 0 ? 10 : -10)" :y="B.y + 4" class="cl b" :text-anchor="s >= 0 ? 'start' : 'end'">B (새 시점, *)</text>
      </svg>
      <div class="sld"><span>새 카메라 B 위치</span><input v-model.number="s" type="range" min="-90" max="90" step="2"></div>
    </div>
    <div class="right">
      <div class="cap">A가 찍은 과거 화면 <span class="mu">· 픽셀마다 깊이도 앎 · 칸에 마우스</span></div>
      <div class="strip">
        <div v-for="(p, c) in ray" :key="c" class="cell" :class="{ on: c === sel }" :style="{ background: p.col }" @mouseenter="sel = c" />
      </div>
      <div class="cap mt">B 화면으로 옮긴 결과 <span class="mu">· 검은 칸 = 옮겨 올 픽셀 없음 {{ holes }}칸</span></div>
      <div class="strip">
        <div v-for="(i, c) in warped" :key="c" class="cell" :class="{ on: target.q && visibleFromB && c === target.q.c, hole: i < 0 }" :style="i >= 0 ? { background: ray[i].col } : {}" @mouseenter="pickB(c)" />
      </div>
      <ol class="steps">
        <li><b>① 픽셀 p + 깊이 D<sub>s</sub>(p) → 3D 점 X</b> <span class="mu">흰 선: A 화면의 픽셀을 깊이만큼 뻗음</span></li>
        <li><b>② X를 B로 다시 찍기 → p*</b> <span class="mu">청록 점선: B 화면 어디에 오는지</span></li>
      </ol>
      <p class="st">
        <template v-if="!target.q">이 점은 B 화면 밖으로 나감</template>
        <template v-else-if="!visibleFromB">이 점은 B에서 보면 더 가까운 물체에 가려짐</template>
        <template v-else>{{ segs.find(g => g.y === target.p.y)?.name }}: A 화면 {{ sel }}번 칸 → B 화면 {{ target.q.c }}번 칸 · 가까울수록 많이 움직임</template>
      </p>
    </div>
  </div>
</template>

<style scoped>
.wg { display: grid; grid-template-columns: 1fr 1.05fr; gap: 1.1rem; align-items: start; }
.map { width: 100%; background: var(--lx-panel); border: 1px solid var(--lx-line); border-radius: 10px; }
.sl { font-size: 10px; fill: var(--lx-muted); }
.fa { stroke: #e6edf3; stroke-width: 1; stroke-dasharray: 3 4; opacity: .45; fill: none; }
.fb { stroke: #5eead4; stroke-width: 1; stroke-dasharray: 3 4; opacity: .6; fill: none; }
.ra { stroke: #e6edf3; stroke-width: 2; }
.rb { stroke: #5eead4; stroke-width: 2; stroke-dasharray: 5 4; }
.rb.blocked { stroke: var(--lx-bad); }
.pt { fill: #fff; stroke: #0d1117; stroke-width: 2; }
.cl { font-size: 10px; fill: #e6edf3; font-weight: 700; }
.cl.b { fill: #5eead4; }
.sld { display: flex; align-items: center; gap: .5rem; font-size: .7rem; color: var(--lx-muted); margin-top: .3rem; }
.sld input { flex: 1; accent-color: var(--lx-accent); }
.cap { font-size: .74rem; font-weight: 700; margin-bottom: .25rem; }
.cap.mt { margin-top: .7rem; }
.mu { color: var(--lx-muted); font-weight: 400; }
.strip { display: grid; grid-template-columns: repeat(56, 1fr); height: 34px; border-radius: 4px; overflow: hidden; border: 1px solid var(--lx-line); }
.cell { position: relative; }
.cell.hole { background: #000; }
.cell.on { outline: 2px solid #fff; outline-offset: -2px; z-index: 1; }
.steps { margin: .8rem 0 0; padding-left: 0; list-style: none; font-size: .76rem; line-height: 1.7; }
.st { font-size: .76rem; margin: .4rem 0 0; color: var(--lx-text); min-height: 1.2rem; }
</style>
