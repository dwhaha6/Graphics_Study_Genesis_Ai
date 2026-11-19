<script setup lang="ts">
import { computed, ref } from 'vue'

// Concept demo of the FramePack context layout used by Lyra 2.0:
// anchor f1k1 | spatial [f4k2 f1k1] | temporal [f16k4 f2k2 f1k1] | generate g20.
// Each tile = one latent frame; tile side shrinks with the kernel factor k. The conditioning box has a fixed width
// (fixed budget) and is right-aligned, so without compression the oldest items on the left get cut off.
const props = defineProps<{ src: string }>()
const base = import.meta.env.BASE_URL
const packed = ref(true)
const TW = 40

type Sec = { key: string, title: string, sub: string, parts: { n: number, k: number }[], cls: string }
const secs: Sec[] = [
  { key: 'a', title: '첫 사진', sub: '고정 기준점', parts: [{ n: 1, k: 1 }], cls: 'anc' },
  { key: 's', title: '찾아온 과거', sub: 'Part 3 · 5장', parts: [{ n: 4, k: 2 }, { n: 1, k: 1 }], cls: 'spa' },
  { key: 't', title: '직전 영상', sub: '← 오래됨 · 최근 →', parts: [{ n: 16, k: 4 }, { n: 2, k: 2 }, { n: 1, k: 1 }], cls: 'tem' },
]
let idx = 0
const tiles = secs.map(s => ({
  ...s,
  items: s.parts.flatMap(p => Array.from({ length: p.n }, () => ({ k: p.k, i: idx++ }))),
}))
const kl = (k: number) => (k === 1 ? '원본' : `${k}배 축소`)
const tileStyle = (k: number, i: number) => {
  const f = packed.value ? k : 1
  return { width: `${TW / f}px`, height: `${(TW / f) * 428 / 832}px`, backgroundImage: `url(${base + props.src})`, backgroundPosition: `${(i * 4) % 100}% 50%` }
}
const msg = computed(() => packed.value
  ? '멀수록 크게 묶어 거칠게 (토큰 적게) → 같은 칸 안에 첫 사진 + 찾아온 과거 + 직전 영상이 모두 들어감'
  : '모두 원본 크기 → 칸을 넘어서 최근 것만 남고, 첫 사진 · 찾아온 과거 · 오래된 과거가 잘림')
</script>

<template>
  <div class="fp">
    <div class="ctrl">
      <button :class="{ on: !packed }" @click="packed = false">모두 원본 크기로</button>
      <button :class="{ on: packed }" @click="packed = true">FramePack 압축</button>
    </div>
    <div class="row">
      <div class="box" :class="{ over: !packed }">
        <div class="boxlbl">조건으로 넣을 수 있는 양 (고정)</div>
        <div class="inner">
          <div v-for="s in tiles" :key="s.key" class="grp" :class="s.cls">
            <div class="sh"><b>{{ s.title }}</b><span>{{ s.sub }}</span></div>
            <div class="tl">
              <div v-for="it in s.items" :key="it.i" class="tile" :style="tileStyle(it.k, it.i)" />
            </div>
            <div class="ks">
              <template v-if="packed"><span v-for="(p, j) in s.parts" :key="j">{{ p.n }}칸 {{ kl(p.k) }}</span></template>
              <span v-else>{{ s.parts.reduce((a, p) => a + p.n, 0) }}칸 원본</span>
            </div>
          </div>
        </div>
      </div>
      <div class="arr">→</div>
      <div class="gen">
        <b>새로 만들 구간</b>
        <span>20칸 (80프레임)</span>
      </div>
    </div>
    <p class="st" :class="{ bad: !packed }">{{ msg }}</p>
  </div>
</template>

<style scoped>
.fp { display: flex; flex-direction: column; gap: .45rem; }
.ctrl { display: flex; gap: .4rem; }
.ctrl button { font-size: .74rem; padding: .18rem .7rem; border-radius: 6px; background: var(--lx-panel2); border: 1px solid var(--lx-line); }
.ctrl button.on { background: var(--lx-accent); color: #0d1117; border-color: var(--lx-accent); font-weight: 700; }
.row { display: flex; align-items: center; gap: .5rem; }
.box { position: relative; width: 640px; border: 2px dashed var(--lx-line); border-radius: 10px; padding: 1.3rem .6rem .5rem; overflow: hidden; transition: border-color .3s; }
.box.over { border-color: var(--lx-bad); }
.boxlbl { position: absolute; top: .25rem; left: .6rem; font-size: .66rem; color: var(--lx-muted); }
.inner { display: flex; justify-content: flex-end; align-items: flex-end; gap: .7rem; }
.grp { flex: none; display: flex; flex-direction: column; gap: .25rem; }
.sh { display: flex; flex-direction: column; font-size: .68rem; line-height: 1.25; white-space: nowrap; }
.sh span { color: var(--lx-muted); font-size: .6rem; }
.anc .sh b { color: var(--lx-warn); } .spa .sh b { color: #7cb3f0; } .tem .sh b { color: var(--lx-text); }
.tl { display: flex; align-items: flex-end; gap: 2px; height: 26px; }
.tile { flex: none; background-size: cover; border-radius: 2px; outline: 1px solid rgba(255, 255, 255, .25); transition: width .45s, height .45s; }
.anc .tile { outline: 2px solid var(--lx-warn); } .spa .tile { outline-color: #7cb3f0; }
.ks { display: flex; gap: .4rem; font-size: .58rem; color: var(--lx-muted); white-space: nowrap; }
.arr { color: var(--lx-muted); font-size: 1.2rem; }
.gen { display: flex; flex-direction: column; justify-content: center; padding: .6rem .7rem; border-radius: 10px; border: 2px solid var(--lx-accent); background: var(--lx-panel); font-size: .72rem; line-height: 1.35; white-space: nowrap; }
.gen span { color: var(--lx-muted); font-size: .64rem; }
.st { font-size: .8rem; margin: 0; min-height: 1.3rem; }
.st.bad { color: #fca5a5; }
</style>
