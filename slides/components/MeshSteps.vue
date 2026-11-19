<script setup lang="ts">
import { ref } from 'vue'

// 2D cross-section illustration of the paper's mesh step (§4.4, App. A.4):
// depth per view -> normals from depth gradient -> oriented points -> SDF on a grid -> marching cubes (here: marching squares).
// Everything below is actually computed (sphere tracing, point-to-plane SDF, marching squares), not hand-drawn.
const W = 160, H = 100
const rects: number[][] = [[-10, 88, 170, 120], [148, -10, 170, 120], [95, 62, 125, 88]] // solid: floor, back wall, box
function sdRect(px: number, py: number, r: number[]) {
  const [x0, y0, x1, y1] = r
  const dx = Math.abs(px - (x0 + x1) / 2) - (x1 - x0) / 2
  const dy = Math.abs(py - (y0 + y1) / 2) - (y1 - y0) / 2
  return Math.hypot(Math.max(dx, 0), Math.max(dy, 0)) + Math.min(Math.max(dx, dy), 0)
}
const sdf = (x: number, y: number) => Math.min(...rects.map(r => sdRect(x, y, r)))

const cam = { x: 12, y: 36 }
const N = 34, a0 = -13 * Math.PI / 180, a1 = 56 * Math.PI / 180, am = (a0 + a1) / 2, f = 17
type Hit = { x: number, y: number, nx: number, ny: number, t: number, qx: number, qy: number }
const hits: Hit[] = []
for (let i = 0; i < N; i++) {
  const a = a0 + (a1 - a0) * i / (N - 1), dx = Math.cos(a), dy = Math.sin(a)
  let t = 0
  for (let k = 0; k < 200; k++) { const s = sdf(cam.x + t * dx, cam.y + t * dy); if (s < 0.02 || t > 400) break; t += s }
  const x = cam.x + t * dx, y = cam.y + t * dy, e = 0.3
  let nx = sdf(x + e, y) - sdf(x - e, y), ny = sdf(x, y + e) - sdf(x, y - e)
  const l = Math.hypot(nx, ny) || 1; nx /= l; ny /= l
  const q = f / Math.cos(a - am)
  hits.push({ x, y, nx, ny, t, qx: cam.x + q * dx, qy: cam.y + q * dy })
}
const tMin = Math.min(...hits.map(h => h.t)), tMax = Math.max(...hits.map(h => h.t))
const gray = (t: number) => { const v = Math.round(235 - 190 * (t - tMin) / (tMax - tMin)); return `rgb(${v},${v},${v})` }
const strip = hits.map((h, i) => {
  const p = hits[Math.max(i - 1, 0)], n = hits[Math.min(i + 1, N - 1)]
  return { x1: (p.qx + h.qx) / 2, y1: (p.qy + h.qy) / 2, x2: (n.qx + h.qx) / 2, y2: (n.qy + h.qy) / 2, c: gray(h.t) }
})
const frustum = `${cam.x},${cam.y} ${hits[0].qx},${hits[0].qy} ${hits[N - 1].qx},${hits[N - 1].qy}`

// SDF at grid vertices from the oriented points (point-to-plane distance to the nearest point), truncated
const g = 5, T = 9
const cols = W / g + 1, rows = H / g + 1
const S: (number | null)[][] = []
for (let j = 0; j < rows; j++) {
  S.push([])
  for (let i = 0; i < cols; i++) {
    const vx = i * g, vy = j * g
    let best = Infinity, h: Hit | null = null
    for (const p of hits) { const d = Math.hypot(vx - p.x, vy - p.y); if (d < best) { best = d; h = p } }
    S[j].push(best > T || !h ? null : (vx - h.x) * h.nx + (vy - h.y) * h.ny)
  }
}
const cells: { x: number, y: number, c: string }[] = []
for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
  const s = S[j][i]; if (s === null) continue
  const a = Math.min(Math.abs(s) / T, 1) * 0.55 + 0.12
  cells.push({ x: i * g - g / 2, y: j * g - g / 2, c: s >= 0 ? `rgba(96,165,250,${a})` : `rgba(245,158,11,${a})` })
}
// marching squares on the zero level
const segs: number[][] = []
const lerp = (p: number[], q: number[], sp: number, sq: number) => { const t = sp / (sp - sq); return [p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])] }
for (let j = 0; j < rows - 1; j++) for (let i = 0; i < cols - 1; i++) {
  const v = [S[j][i], S[j][i + 1], S[j + 1][i + 1], S[j + 1][i]]
  if (v.some(x => x === null)) continue
  const s = v as number[]
  const P = [[i * g, j * g], [(i + 1) * g, j * g], [(i + 1) * g, (j + 1) * g], [i * g, (j + 1) * g]]
  const pts: number[][] = []
  for (let k = 0; k < 4; k++) { const k2 = (k + 1) % 4; if ((s[k] < 0) !== (s[k2] < 0)) pts.push(lerp(P[k], P[k2], s[k], s[k2])) }
  for (let k = 0; k + 1 < pts.length; k += 2) segs.push([...pts[k], ...pts[k + 1]])
}
const solid = rects.map(([x0, y0, x1, y1]) => ({ x: x0, y: y0, w: x1 - x0, h: y1 - y0 }))

const hov = ref<number | null>(null)
const steps = [
  { t: '① Depth → Normal', d: '픽셀별 깊이 · 기울기로 Normal' },
  { t: '② SDF', d: '표면까지 거리 · 바깥 <b class="pos">+</b> / 안쪽 <b class="neg">−</b>' },
  { t: '③ Mesh', d: 'SDF = 0인 곳 → Marching Cubes' },
]
</script>

<template>
  <div class="ms">
    <template v-for="(st, k) in steps" :key="k">
      <div v-if="k" class="ar">→</div>
      <div class="pn" :class="{ dim: hov !== null && hov !== k }" @mouseenter="hov = k" @mouseleave="hov = null">
        <svg :viewBox="`0 0 ${W} ${H}`">
          <rect x="0" y="0" :width="W" :height="H" fill="#0b1017" />
          <template v-if="k === 0">
            <rect v-for="(r, i) in solid" :key="i" :x="r.x" :y="r.y" :width="r.w" :height="r.h" fill="#1c2430" />
            <polygon :points="frustum" fill="rgba(148,163,184,.12)" />
            <line v-for="(h, i) in hits" :key="'r' + i" :x1="h.qx" :y1="h.qy" :x2="h.x" :y2="h.y" stroke="#94a3b8" stroke-opacity=".22" stroke-width=".5" />
            <line v-for="(s, i) in strip" :key="'s' + i" :x1="s.x1" :y1="s.y1" :x2="s.x2" :y2="s.y2" :stroke="s.c" stroke-width="6" />
            <line v-for="(h, i) in hits" :key="'n' + i" :x1="h.x" :y1="h.y" :x2="h.x + 5 * h.nx" :y2="h.y + 5 * h.ny" stroke="#fbbf24" stroke-width=".8" />
            <circle v-for="(h, i) in hits" :key="'p' + i" :cx="h.x" :cy="h.y" r="1.2" fill="var(--lx-accent)" />
            <text x="2" y="51" class="sv">카메라</text>
          </template>
          <template v-else-if="k === 1">
            <rect v-for="(c, i) in cells" :key="i" :x="c.x" :y="c.y" :width="g" :height="g" :fill="c.c" stroke="#0b1017" stroke-width=".4" />
            <circle v-for="(h, i) in hits" :key="'p' + i" :cx="h.x" :cy="h.y" r=".9" fill="#e2e8f0" />
          </template>
          <template v-else>
            <rect v-for="(c, i) in cells" :key="i" :x="c.x" :y="c.y" :width="g" :height="g" fill="none" stroke="#334155" stroke-width=".35" />
            <line v-for="(s, i) in segs" :key="i" :x1="s[0]" :y1="s[1]" :x2="s[2]" :y2="s[3]" stroke="var(--lx-accent)" stroke-width="1.8" stroke-linecap="round" />
          </template>
        </svg>
        <div class="tt">{{ st.t }}</div>
        <div class="dd" v-html="st.d" />
      </div>
    </template>
  </div>
</template>

<style scoped>
.ms { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; align-items: start; gap: .3rem; }
.pn { transition: opacity .15s; }
.pn svg { width: 100%; display: block; border-radius: 5px; border: 1px solid var(--lx-line); }
.ar { color: var(--lx-muted); font-size: 1rem; padding-top: 2.3rem; }
.tt { font-size: .68rem; font-weight: 700; margin-top: .2rem; }
.dd { font-size: .58rem; color: var(--lx-muted); line-height: 1.35; }
.dd :deep(.pos) { color: #60a5fa; }
.dd :deep(.neg) { color: #f59e0b; }
.sv { font-size: 6px; fill: #94a3b8; }
.dim { opacity: .4; }
</style>
