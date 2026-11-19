<script setup lang="ts">
import { computed, ref } from 'vue'

// Concept demo of §4.2 geometry-aware retrieval in a 2D top-down room.
// Each past frame keeps its own visible points (per-frame cache). For a target camera we project all cached
// points, keep only the nearest per target pixel (occlusion, threshold δ), count visible points per frame (φ),
// then pick frames either by score or by greedy coverage (Lyra 2.0, up to N frames).
type Cam = { x: number, y: number, h: number }
const FOV = 70; const NB = 48; const TB = 24; const DEL = 3
const seg = (a: number[], b: number[], step = 4) => {
  const n = Math.max(1, Math.round(Math.hypot(b[0] - a[0], b[1] - a[1]) / step))
  return Array.from({ length: n }, (_, k) => [a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n])
}
const walls = [[[20, 20], [280, 20]], [[280, 20], [280, 200]], [[280, 200], [20, 200]], [[20, 200], [20, 20]]]
const pillar = [[[138, 98], [162, 98]], [[162, 98], [162, 122]], [[162, 122], [138, 122]], [[138, 122], [138, 98]]]
const pts = [...walls, ...pillar].flatMap(s => seg(s[0], s[1]))

const frames: (Cam & { id: string, c: string })[] = [
  { id: 'A', x: 80, y: 125, h: -8, c: '#3987e5' },
  { id: 'B', x: 88, y: 128, h: -4, c: '#d95926' },
  { id: 'C', x: 235, y: 120, h: 8, c: '#199e70' },
  { id: 'D', x: 240, y: 185, h: -75, c: '#c98500' },
  { id: 'E', x: 60, y: 185, h: 70, c: '#d55181' },
  { id: 'F', x: 60, y: 50, h: 100, c: '#9085e9' },
]
const targets: (Cam & { name: string })[] = [
  { name: '1', x: 150, y: 195, h: 0 },
  { name: '2', x: 215, y: 150, h: -50 },
  { name: '3', x: 100, y: 150, h: 40 },
]

function inView(c: Cam) {
  const out: { i: number, a: number, d: number }[] = []
  pts.forEach(([px, py], i) => {
    const dx = px - c.x; const dy = py - c.y
    let a = Math.atan2(dx, -dy) * 180 / Math.PI - c.h
    a = ((a + 180) % 360 + 360) % 360 - 180
    if (Math.abs(a) <= FOV / 2) out.push({ i, a, d: Math.hypot(dx, dy) })
  })
  return out
}
const bin = (a: number, n: number) => Math.min(n - 1, Math.floor((a + FOV / 2) / FOV * n))
function visible(c: Cam) {
  const v = inView(c); const zb = new Map<number, number>()
  v.forEach(p => { const b = bin(p.a, NB); zb.set(b, Math.min(zb.get(b) ?? 1e9, p.d)) })
  return new Set(v.filter(p => p.d <= zb.get(bin(p.a, NB))! + DEL).map(p => p.i))
}
const cache = frames.map(f => visible(f)) // per-frame cache, never fused

const tIdx = ref(0)
const mode = ref<'score' | 'greedy'>('greedy')
const N = ref(2)

const stats = computed(() => {
  const t = targets[tIdx.value]
  const vd = new Map(inView(t).map(p => [p.i, p]))
  const zb = new Map<number, number>()
  cache.forEach(s => s.forEach((i) => {
    const p = vd.get(i); if (!p) return
    const b = bin(p.a, TB); zb.set(b, Math.min(zb.get(b) ?? 1e9, p.d))
  }))
  return cache.map((s) => {
    const bins = new Set<number>(); const shown: number[] = []
    s.forEach((i) => {
      const p = vd.get(i); if (!p) return
      const b = bin(p.a, TB)
      if (p.d - zb.get(b)! < DEL) { bins.add(b); shown.push(i) }
    })
    return { phi: shown.length, bins, shown }
  })
})
const pick = computed(() => {
  const st = stats.value; const chosen: number[] = []; const cov = new Set<number>()
  for (let k = 0; k < N.value; k++) {
    const cand = st.map((s, i) => ({ i, s })).filter(o => !chosen.includes(o.i))
    const gain = (o: { s: { bins: Set<number> } }) => [...o.s.bins].filter(b => !cov.has(b)).length
    const best = mode.value === 'score'
      ? cand.sort((p, q) => q.s.phi - p.s.phi)[0]
      : cand.sort((p, q) => gain(q) - gain(p))[0]
    if (!best || (mode.value === 'greedy' && gain(best) === 0) || best.s.phi === 0) break
    chosen.push(best.i); best.s.bins.forEach(b => cov.add(b))
  }
  return { chosen, cov }
})
const cells = computed(() => Array.from({ length: TB }, (_, b) => {
  const f = pick.value.chosen.find(i => stats.value[i].bins.has(b))
  return f == null ? null : frames[f]
}))
const coverage = computed(() => Math.round(pick.value.cov.size / TB * 100))

const wedge = (c: Cam, r: number) => {
  const p = (d: number) => `${(c.x + r * Math.sin((c.h + d) * Math.PI / 180)).toFixed(1)} ${(c.y - r * Math.cos((c.h + d) * Math.PI / 180)).toFixed(1)}`
  return `M${c.x} ${c.y} L${p(-FOV / 2)} L${p(FOV / 2)} Z`
}
const ray = (c: Cam, d: number, r: number) => `M${c.x} ${c.y} L${(c.x + r * Math.sin((c.h + d) * Math.PI / 180)).toFixed(1)} ${(c.y - r * Math.cos((c.h + d) * Math.PI / 180)).toFixed(1)}`
const tgt = computed(() => targets[tIdx.value])
</script>

<template>
  <div class="rd">
    <div class="ctrl">
      <span class="lb">목표 시점</span>
      <button v-for="(t, i) in targets" :key="t.name" :class="{ on: tIdx === i }" @click="tIdx = i">{{ t.name }}</button>
      <span class="lb sp">고르는 방식</span>
      <button :class="{ on: mode === 'score' }" @click="mode = 'score'">Score순</button>
      <button :class="{ on: mode === 'greedy' }" @click="mode = 'greedy'">Greedy (Lyra)</button>
      <span class="lb sp">장수</span>
      <button v-for="n in 5" :key="n" class="n" :class="{ on: N === n }" @click="N = n">{{ n }}</button>
    </div>
    <svg viewBox="0 0 300 220" class="map">
      <path :d="ray(tgt, -FOV / 2, 260)" class="tray" /><path :d="ray(tgt, FOV / 2, 260)" class="tray" />
      <line v-for="(w, i) in walls" :key="`w${i}`" :x1="w[0][0]" :y1="w[0][1]" :x2="w[1][0]" :y2="w[1][1]" class="wall" />
      <rect x="138" y="98" width="24" height="24" class="pil" />
      <template v-for="i in pick.chosen" :key="`p${i}`">
        <circle v-for="k in stats[i].shown" :key="k" :cx="pts[k][0]" :cy="pts[k][1]" r="2.6" :fill="frames[i].c" />
      </template>
      <g v-for="(f, i) in frames" :key="f.id" :opacity="pick.chosen.includes(i) ? 1 : .35">
        <path :d="wedge(f, 22)" :fill="f.c" fill-opacity=".35" :stroke="f.c" stroke-width="1.5" />
        <circle :cx="f.x" :cy="f.y" r="3.5" :fill="f.c" />
        <text :x="f.x - 9" :y="f.y + 12" class="fl">{{ f.id }}</text>
      </g>
      <path :d="wedge(tgt, 16)" fill="#e6edf3" />
      <text :x="tgt.x" :y="tgt.y + 13" class="tl">목표</text>
    </svg>
    <div class="strip">
      <div v-for="(c, b) in cells" :key="b" class="cell" :style="c ? { background: c.c } : {}">{{ c ? c.id : '' }}</div>
    </div>
    <div class="foot">
      <span>목표 시점 화면 <b>{{ coverage }}%</b> 채움 · 빈칸 = 선택된 과거 프레임에서 대응 정보를 확보하지 못한 곳</span>
      <span class="phi">Visibility Score φ <template v-for="(f, i) in frames" :key="f.id"><i :class="{ on: pick.chosen.includes(i) }">{{ f.id }} {{ stats[i].phi }}</i></template></span>
    </div>
  </div>
</template>

<style scoped>
.rd { display: flex; flex-direction: column; gap: .35rem; }
.ctrl { display: flex; align-items: center; gap: .25rem; flex-wrap: nowrap; white-space: nowrap; }
.ctrl .lb { font-size: .7rem; color: var(--lx-muted); }
.ctrl .sp { margin-left: .35rem; }
.ctrl button { font-size: .66rem; padding: .1rem .42rem; border-radius: 6px; background: var(--lx-panel2); border: 1px solid var(--lx-line); }
.ctrl button.n { padding: .1rem .38rem; }
.ctrl button.on { background: var(--lx-accent); color: #0d1117; border-color: var(--lx-accent); font-weight: 700; }
.map { width: 100%; height: 222px; background: var(--lx-panel); border: 1px solid var(--lx-line); border-radius: 10px; }
.wall { stroke: #6b7280; stroke-width: 2; }
.pil { fill: #4b5563; }
.tray { stroke: #e6edf3; stroke-width: 1; stroke-dasharray: 4 4; opacity: .55; }
.fl { font-size: 10px; font-weight: 700; fill: #e6edf3; }
.tl { font-size: 9px; fill: #e6edf3; text-anchor: middle; font-weight: 700; }
.strip { display: grid; grid-template-columns: repeat(24, 1fr); gap: 2px; }
.cell { height: 18px; border-radius: 3px; background: #2a313b; font-size: .58rem; font-weight: 700; color: #fff; display: grid; place-items: center; transition: background .2s; }
.foot { display: flex; justify-content: space-between; gap: .6rem; font-size: .7rem; color: var(--lx-muted); flex-wrap: wrap; }
.foot b { color: var(--lx-accent); font-size: .85rem; }
.phi i { font-style: normal; margin-left: .45rem; }
.phi i.on { color: var(--lx-text); font-weight: 700; }
</style>
