<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { W, H, src, warp, addr } from '../utils/warpScene'

// Concept demo of §4.2 canonical coordinate warping: warp RGB (holes/cracks get copied) vs warp only the
// source address (u, v) -> per new-view pixel a correspondence "frame j, pixel (u, v)" + warped depth.
const mode = ref<'rgb' | 'coord'>('coord')
const t = ref(0.8)
const hov = ref<{ x: number, y: number } | null>(null)
const srcCv = ref<HTMLCanvasElement>(); const tgtCv = ref<HTMLCanvasElement>()
const warped = computed(() => warp(t.value))
const holes = computed(() => Math.round(warped.value.filter(i => i < 0).length / (W * H) * 100))

function paint(cv: HTMLCanvasElement | undefined, pick: (k: number) => number) {
  if (!cv) return
  const ctx = cv.getContext('2d')!; const img = ctx.createImageData(W, H)
  for (let k = 0; k < W * H; k++) {
    const i = pick(k); const o = k * 4
    if (i >= 0) {
      const c = mode.value === 'rgb' ? src[i] : addr(i % W, Math.floor(i / W))
      img.data[o] = c.r; img.data[o + 1] = c.g; img.data[o + 2] = c.b
    }
    img.data[o + 3] = 255
  }
  ctx.putImageData(img, 0, 0)
}
function draw() { paint(srcCv.value, k => k); paint(tgtCv.value, k => warped.value[k]) }
onMounted(draw)
watch([mode, t], draw)

function onMove(e: MouseEvent) {
  const r = (e.currentTarget as HTMLElement).getBoundingClientRect()
  hov.value = { x: Math.min(W - 1, Math.floor((e.clientX - r.left) / r.width * W)), y: Math.min(H - 1, Math.floor((e.clientY - r.top) / r.height * H)) }
}
const match = computed(() => {
  if (!hov.value) return null
  const i = warped.value[hov.value.y * W + hov.value.x]
  if (i < 0) return { hole: true as const }
  const u = i % W; const v = Math.floor(i / W)
  return { hole: false as const, u, v, nu: (u / (W - 1) * 2 - 1).toFixed(2), nv: (v / (H - 1) * 2 - 1).toFixed(2), d: src[i].z }
})
</script>

<template>
  <div class="cw">
    <div class="ctrl">
      <button :class="{ on: mode === 'rgb' }" @click="mode = 'rgb'">그림(RGB)을 옮기면</button>
      <button :class="{ on: mode === 'coord' }" @click="mode = 'coord'">주소를 옮기면 (Lyra 2.0)</button>
      <span class="lb">카메라 이동</span>
      <input v-model.number="t" type="range" min="0" max="1.6" step="0.1">
    </div>
    <div class="pair">
      <div>
        <div class="cap">찾아온 과거 프레임 j <span v-if="mode === 'coord'" class="mu">· 색 = 주소 <b class="sy">C<sub>j</sub></b> (u, v)</span><span v-else class="mu">· 실제 그림</span></div>
        <div class="cvw">
          <canvas ref="srcCv" :width="W" :height="H" />
          <svg v-if="match && !match.hole" :viewBox="`0 0 ${W} ${H}`" class="ov"><circle :cx="match.u + .5" :cy="match.v + .5" r="3.4" class="mk" /></svg>
        </div>
      </div>
      <div>
        <div class="cap">새 시점으로 warping <b v-if="mode === 'coord'" class="sy">Ĉ<sub>j</sub></b> <span class="mu">· 검은 곳 = 대응 없음 {{ holes }}%</span></div>
        <div class="cvw" @mousemove="onMove" @mouseleave="hov = null">
          <canvas ref="tgtCv" :width="W" :height="H" />
          <svg v-if="hov" :viewBox="`0 0 ${W} ${H}`" class="ov"><circle :cx="hov.x + .5" :cy="hov.y + .5" r="3.4" class="mk" /></svg>
        </div>
      </div>
    </div>
    <div class="st">
      <template v-if="match && match.hole">이 픽셀은 과거 프레임에서 안 보이던 곳 → 대응 없음 → 영상 모델이 새로 그림</template>
      <template v-else-if="match">
        새 화면 이 픽셀에 저장되는 값 = <span class="vec"><b>u</b> {{ match.nu }}</span><span class="vec"><b>v</b> {{ match.nv }}</span><span class="vec"><b>j</b> Spatial Slot 번호</span><span class="vec"><b>Depth</b> {{ match.d.toFixed(1) }}</span>
        <span class="mu">→ "과거 프레임 j의 저 픽셀과 같은 곳"</span>
      </template>
      <template v-else-if="mode === 'rgb'">그림을 옮기면 기둥·벤치 뒤에 구멍, 경계가 깨진 그림이 됨 → 이걸 조건으로 주면 모델이 결함까지 재생성할 수 있음</template>
      <template v-else>외형 정보 없이 "몇 번 Spatial Slot의 어느 픽셀인지"만 옮김 → 새 화면 전체의 <b>대응표</b> · 오른쪽에 마우스를 올려 보세요</template>
    </div>
  </div>
</template>

<style scoped>
.cw { display: flex; flex-direction: column; gap: .35rem; }
.ctrl { display: flex; align-items: center; gap: .4rem; flex-wrap: wrap; }
.ctrl button { font-size: .72rem; padding: .15rem .6rem; border-radius: 6px; background: var(--lx-panel2); border: 1px solid var(--lx-line); }
.ctrl button.on { background: var(--lx-accent); color: #0d1117; border-color: var(--lx-accent); font-weight: 700; }
.ctrl .lb { font-size: .7rem; color: var(--lx-muted); margin-left: .5rem; }
.ctrl input { flex: 1; min-width: 6rem; accent-color: var(--lx-accent); }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: .7rem; }
.cap { font-size: .74rem; font-weight: 700; margin-bottom: .2rem; }
.mu { color: var(--lx-muted); font-weight: 400; }
.sy { font-family: 'Times New Roman', serif; font-style: italic; color: var(--lx-accent); }
.cvw { position: relative; border-radius: 6px; overflow: hidden; border: 1px solid var(--lx-line); cursor: crosshair; }
.cvw canvas { display: block; width: 100%; image-rendering: pixelated; }
.ov { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.mk { fill: none; stroke: #fff; stroke-width: 1.2; }
.st { font-size: .76rem; line-height: 1.6; min-height: 2.6rem; }
.vec { display: inline-block; margin: 0 .2rem; padding: 0 .4rem; border-radius: 5px; background: var(--lx-panel2); border: 1px solid var(--lx-line); font-family: ui-monospace, monospace; font-size: .7rem; }
.vec b { color: var(--lx-accent); }
</style>
