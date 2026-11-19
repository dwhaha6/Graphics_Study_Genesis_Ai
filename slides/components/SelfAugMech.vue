<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

// Concept demo of §4.3 self-augmentation. Real method works on VAE latents:
// z_t = (1 - t) z0 + t eps (t ~ U(0, 0.5), with prob. p_aug = 0.7), one-step denoise z~0 = z_t - t v, used as history.
// Here: noise mixing is done on pixels, and the imperfect one-step result is imitated with blur + color shift.
const props = defineProps<{ src: string }>()
const base = import.meta.env.BASE_URL
const t = ref(0.3)
const aug = ref(true)
const draws = ref<boolean[]>([])
const cv = ref<HTMLCanvasElement>()
const W = 208; const H = 107
let pix: Uint8ClampedArray | null = null
const gauss = (() => { // fixed-seed gaussian field
  let s = 7; const r = () => { s = (s * 16807) % 2147483647; return s / 2147483647 }
  return Array.from({ length: W * H * 3 }, () => Math.sqrt(-2 * Math.log(r() + 1e-9)) * Math.cos(2 * Math.PI * r()))
})()

function draw() {
  const c = cv.value; if (!c || !pix) return
  const ctx = c.getContext('2d')!; const img = ctx.createImageData(W, H); const tt = aug.value ? t.value : 0
  for (let k = 0; k < W * H; k++) {
    for (let ch = 0; ch < 3; ch++) img.data[k * 4 + ch] = (1 - tt) * pix[k * 4 + ch] + tt * (128 + 90 * gauss[k * 3 + ch])
    img.data[k * 4 + 3] = 255
  }
  ctx.putImageData(img, 0, 0)
}
onMounted(() => {
  const im = new Image(); im.src = base + props.src
  im.onload = () => {
    const off = document.createElement('canvas'); off.width = W; off.height = H
    const o = off.getContext('2d')!; o.drawImage(im, 0, 0, W, H); pix = o.getImageData(0, 0, W, H).data; draw()
  }
})
watch([t, aug], draw)

const recon = () => {
  const tt = aug.value ? t.value : 0
  return `blur(${tt * 5}px) saturate(${1 + tt * .9}) hue-rotate(${-tt * 40}deg) contrast(${1 + tt * .25})`
}
function sample() {
  aug.value = Math.random() < 0.7
  if (aug.value) t.value = Math.round(Math.random() * 50) / 100
  draws.value = [...draws.value, aug.value].slice(-10)
}
</script>

<template>
  <div class="sm">
    <div class="ctrl">
      <button class="dice" @click="sample">학습 샘플 하나 뽑기</button>
      <span class="lb">섞는 노이즈 양 t <span style="opacity:.7">(~U(0, 0.5))</span></span>
      <input v-model.number="t" type="range" min="0" max="0.5" step="0.01" :disabled="!aug">
      <b class="tv">{{ aug ? t.toFixed(2) : '–' }}</b>
      <span class="hist">
        <i v-for="(d, i) in draws" :key="i" :class="{ on: d }" />
        <span v-if="draws.length" class="mu">● 교체 ○ 그대로</span>
      </span>
    </div>
    <div class="flow">
      <div class="node">
        <div class="lbl">① 정답 과거 <i class="sy">z₀<sup>hist</sup></i></div>
        <div class="img ok"><img :src="base + props.src" draggable="false"></div>
      </div>
      <div class="arr" :class="{ off: !aug }">+노이즈</div>
      <div class="node" :class="{ dim: !aug }">
        <div class="lbl">② 노이즈 섞기 <i class="sy">z<sub>t</sub><sup>hist</sup></i></div>
        <div class="img"><canvas ref="cv" :width="W" :height="H" /></div>
      </div>
      <div class="arr" :class="{ off: !aug }">One-Step<br>Denoising<br><span style="opacity:.75">(DiT Forward 1회)</span></div>
      <div class="node">
        <div class="lbl">③ {{ aug ? '조금 틀린 과거' : '정답 과거 그대로' }} <i class="sy">{{ aug ? 'z̃₀' : 'z₀' }}<sup>hist</sup></i> → 조건</div>
        <div class="img" :class="aug ? 'warn' : 'ok'"><img :src="base + props.src" :style="{ filter: recon() }" draggable="false"></div>
      </div>
      <div class="arr">→</div>
      <div class="model">영상<br>모델<br><i class="sy">v<sub>θ</sub></i></div>
      <div class="arr">→</div>
      <div class="node">
        <div class="lbl">④ 학습 목표 <i class="sy">z₀<sup>cur</sup></i></div>
        <div class="img ok"><img :src="base + props.src" style="transform: translateX(-8%) scale(1.2)" draggable="false"></div>
        <div class="tag">항상 깨끗한 정답</div>
      </div>
    </div>
    <p class="st">
      <template v-if="aug">이번 샘플: 과거를 모델 자신이 만든 "조금 틀린 결과"로 바꿔서 줌 (70% 확률) · 노이즈가 클수록 복원 오차가 커질 수 있음</template>
      <template v-else>이번 샘플: 과거를 그대로 줌 (30% 확률)</template>
    </p>
  </div>
</template>

<style scoped>
.sm { display: flex; flex-direction: column; gap: .45rem; }
.ctrl { display: flex; align-items: center; gap: .45rem; }
.dice { font-size: .74rem; padding: .2rem .75rem; border-radius: 6px; background: var(--lx-accent); color: #0d1117; font-weight: 700; }
.lb { font-size: .7rem; color: var(--lx-muted); margin-left: .4rem; }
.ctrl input { width: 9rem; accent-color: var(--lx-accent); }
.tv { font-size: .78rem; width: 2.2rem; }
.hist { display: flex; align-items: center; gap: 3px; margin-left: .3rem; }
.hist i { width: 9px; height: 9px; border-radius: 50%; border: 1.5px solid var(--lx-warn); }
.hist i.on { background: var(--lx-warn); }
.mu { color: var(--lx-muted); font-size: .62rem; margin-left: .35rem; }
.flow { display: flex; align-items: center; gap: .35rem; }
.node { position: relative; width: 170px; flex: none; transition: opacity .3s; }
.node.dim { opacity: .3; }
.lbl { font-size: .66rem; color: var(--lx-muted); margin-bottom: .2rem; white-space: nowrap; }
.img { aspect-ratio: 832 / 428; overflow: hidden; border-radius: 7px; border: 3px solid var(--lx-line); }
.img img, .img canvas { display: block; width: 100%; height: 100%; object-fit: cover; transition: filter .3s; }
.img.ok { border-color: var(--lx-good); } .img.warn { border-color: #fb923c; }
.tag { position: absolute; top: 100%; left: 0; font-size: .7rem; margin-top: .25rem; font-weight: 800; color: #0d1117; background: #86efac; border-radius: 4px; padding: 0 .4rem; }
.arr { font-size: .62rem; color: var(--lx-muted); text-align: center; line-height: 1.25; flex: none; transition: opacity .3s; }
.arr.off { opacity: .3; }
.model { padding: .7rem .5rem; border-radius: 10px; background: var(--lx-panel2); border: 1px solid #4b5563; font-weight: 700; font-size: .78rem; text-align: center; line-height: 1.3; flex: none; }
.st { font-size: .78rem; margin: .9rem 0 0; min-height: 1.2rem; }
.sy { font-style: italic; color: var(--lx-accent); font-family: "Times New Roman", serif; font-size: .8rem; margin-left: .15rem; }
</style>
