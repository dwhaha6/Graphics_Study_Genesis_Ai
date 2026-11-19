<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { W, H, src, warp } from '../utils/warpScene'

// Concept demo of how warped canonical coordinates steer attention (§4.2, A.1).
// New-view tokens (queries) attend to tokens of a retrieved past frame (keys/values).
// 'coord': query carries the warped address, key carries its own address -> weight peaks where addresses match.
// 'none' : no address hint -> attention can only guess (here: broad weights around the same screen position).
// Output token = attention-weighted mix of past-frame patches (values are not modified).
const T = 8; const TX = W / T; const TY = H / T; const SHIFT = 0.8
const mode = ref<'none' | 'coord'>('coord')
const hov = ref<number | null>(null)
const srcCv = ref<HTMLCanvasElement>(); const outCv = ref<HTMLCanvasElement>()
const wp = warp(SHIFT)

const queries = Array.from({ length: TX * TY }, (_, q) => { // warped address of each new-view token (or null = hole)
  const tx = q % TX; const ty = Math.floor(q / TX); let su = 0; let sv = 0; let n = 0
  for (let y = 0; y < T; y++) {
    for (let x = 0; x < T; x++) {
      const i = wp[(ty * T + y) * W + tx * T + x]
      if (i >= 0) { su += i % W; sv += Math.floor(i / W); n++ }
    }
  }
  return { cx: tx * T + T / 2, cy: ty * T + T / 2, a: n > T * T / 2 ? { u: su / n, v: sv / n } : null }
})
const keys = Array.from({ length: TX * TY }, (_, k) => ({ cx: (k % TX) * T + T / 2 - .5, cy: Math.floor(k / TX) * T + T / 2 - .5 }))

const weights = computed(() => queries.map((q) => {
  let lg: number[]
  if (mode.value === 'coord') {
    if (!q.a) return null
    lg = keys.map(k => -((q.a!.u - k.cx) ** 2 + (q.a!.v - k.cy) ** 2) / (2 * 2.5 ** 2))
  }
  else {
    lg = keys.map(k => -((q.cx - k.cx) ** 2 + (q.cy - k.cy) ** 2) / (2 * 9 ** 2))
  }
  const m = Math.max(...lg); const e = lg.map(l => Math.exp(l - m)); const s = e.reduce((a, b) => a + b, 0)
  return e.map(x => x / s)
}))

function draw() {
  const sc = srcCv.value; const oc = outCv.value; if (!sc || !oc) return
  const si = sc.getContext('2d')!.createImageData(W, H)
  src.forEach((p, k) => { si.data[k * 4] = p.r; si.data[k * 4 + 1] = p.g; si.data[k * 4 + 2] = p.b; si.data[k * 4 + 3] = 255 })
  sc.getContext('2d')!.putImageData(si, 0, 0)
  const oi = oc.getContext('2d')!.createImageData(W, H)
  weights.value.forEach((w, q) => {
    const tx = q % TX; const ty = Math.floor(q / TX)
    for (let y = 0; y < T; y++) {
      for (let x = 0; x < T; x++) {
        const o = ((ty * T + y) * W + tx * T + x) * 4; let r = 0; let g = 0; let b = 0
        if (!w) { const hatch = (x + y) % 4 === 0; r = g = b = hatch ? 70 : 22 }
        else {
          w.forEach((wk, k) => {
            if (wk < 1e-4) return
            const p = src[(Math.floor(k / TX) * T + y) * W + (k % TX) * T + x]; r += wk * p.r; g += wk * p.g; b += wk * p.b
          })
        }
        oi.data[o] = r; oi.data[o + 1] = g; oi.data[o + 2] = b; oi.data[o + 3] = 255
      }
    }
  })
  oc.getContext('2d')!.putImageData(oi, 0, 0)
}
onMounted(draw)
watch(mode, draw)

function onMove(e: MouseEvent) {
  const r = (e.currentTarget as HTMLElement).getBoundingClientRect()
  const tx = Math.min(TX - 1, Math.floor((e.clientX - r.left) / r.width * TX)); const ty = Math.min(TY - 1, Math.floor((e.clientY - r.top) / r.height * TY))
  hov.value = ty * TX + tx
}
const hw = computed(() => (hov.value == null ? null : weights.value[hov.value]))
const top = computed(() => {
  if (!hw.value) return null
  const m = Math.max(...hw.value); return { pct: Math.round(m * 100), k: hw.value.indexOf(m) }
})
</script>

<template>
  <div class="ad">
    <div class="ctrl">
      <button :class="{ on: mode === 'none' }" @click="mode = 'none'">주소 힌트 없이</button>
      <button :class="{ on: mode === 'coord' }" @click="mode = 'coord'">주소 힌트를 Q·K에 더하면 (Lyra 2.0)</button>
    </div>
    <div class="pair">
      <div>
        <div class="cap">찾아온 과거 프레임 <span class="mu">· K · V · 주소 <b class="sy">C<sub>j</sub></b></span></div>
        <div class="cvw">
          <canvas ref="srcCv" :width="W" :height="H" />
          <svg :viewBox="`0 0 ${W} ${H}`" class="ov">
            <line v-for="i in TX - 1" :key="`x${i}`" :x1="i * T" :x2="i * T" y1="0" :y2="H" class="gl" />
            <line v-for="i in TY - 1" :key="`y${i}`" :y1="i * T" :y2="i * T" x1="0" :x2="W" class="gl" />
            <template v-if="hw">
              <rect v-for="(w, k) in hw" :key="k" :x="(k % TX) * T" :y="Math.floor(k / TX) * T" :width="T" :height="T" :opacity="Math.min(.9, w / Math.max(...hw) * .9)" class="hm" />
            </template>
          </svg>
        </div>
      </div>
      <div>
        <div class="cap">새 화면 토큰 <span class="mu">· Q · 주소 <b class="sy">Ĉ<sub>j</sub></b> · 마우스</span></div>
        <div class="cvw" @mousemove="onMove" @mouseleave="hov = null">
          <canvas ref="outCv" :width="W" :height="H" />
          <svg :viewBox="`0 0 ${W} ${H}`" class="ov">
            <rect v-if="hov != null" :x="(hov % TX) * T" :y="Math.floor(hov / TX) * T" :width="T" :height="T" class="sel" />
          </svg>
        </div>
      </div>
    </div>
    <p class="st">
      <template v-if="hov != null && !hw">이 토큰은 대응 없음 (과거에 안 보이던 곳) → 특정 과거 토큰에 끌리지 않고 영상 모델이 새로 그림</template>
      <template v-else-if="top && mode === 'coord'">왼쪽 하이라이트 = 보는 비중 · 주소가 같은 과거 토큰에 attention 집중 (최대 {{ top.pct }}%) → 그 토큰의 내용(V)을 가져와 정확한 자리에 그림</template>
      <template v-else-if="top">어디를 봐야 할지 몰라 여러 토큰을 넓게 봄 (최대 {{ top.pct }}%) → 흐리고, 카메라가 움직인 만큼 어긋남</template>
      <template v-else-if="mode === 'coord'">새 화면이 과거 프레임의 맞는 자리를 정확히 참고 · 빗금 = 대응 없음 → 새로 그림 · 오른쪽에 마우스를 올려 보세요</template>
      <template v-else>대응을 모르면 attention이 스스로 찾아야 함 → 시점이 크게 바뀌면 흐리고 어긋나기 쉬움</template>
    </p>
  </div>
</template>

<style scoped>
.ad { display: flex; flex-direction: column; gap: .35rem; }
.ctrl { display: flex; gap: .4rem; }
.ctrl button { font-size: .72rem; padding: .15rem .6rem; border-radius: 6px; background: var(--lx-panel2); border: 1px solid var(--lx-line); }
.ctrl button.on { background: var(--lx-accent); color: #0d1117; border-color: var(--lx-accent); font-weight: 700; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: .7rem; }
.cap { font-size: .74rem; font-weight: 700; margin-bottom: .2rem; }
.mu { color: var(--lx-muted); font-weight: 400; }
.sy { font-family: 'Times New Roman', serif; font-style: italic; color: var(--lx-accent); }
.cvw { position: relative; border-radius: 6px; overflow: hidden; border: 1px solid var(--lx-line); cursor: crosshair; }
.cvw canvas { display: block; width: 100%; image-rendering: pixelated; }
.ov { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.gl { stroke: rgba(255, 255, 255, .18); stroke-width: .3; }
.hm { fill: #5eead4; }
.sel { fill: none; stroke: #fff; stroke-width: 1; }
.st { font-size: .76rem; line-height: 1.5; margin: 0; min-height: 2.3rem; }
</style>
