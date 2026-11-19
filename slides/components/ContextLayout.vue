<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import katex from 'katex'

// §3 / §4.2 context layout: f1k1 | f4k2 f1k1 | f16k4 f2k2 f1k1 | g20.
// "fnkm = n frames compressed with spatial subsampling factor m" -> tile side = base / m (tokens / m²).
// Hover a notation token or a card to link the two.
type G = 'anchor' | 'spatial' | 'temporal' | 'gen'
type Tok = { id: string, g: G, txt: string, tip: string }
const toks: Tok[] = [
  { id: 'a', g: 'anchor', txt: 'f1k1', tip: '입력 이미지 I₀ 1장 · 원본 해상도 · 매 구간 항상 포함' },
  { id: 's1', g: 'spatial', txt: 'f4k2', tip: 'spatial memory 이미지 4장 · 공간축 2배 추가 압축 → 1장당 Token ¼' },
  { id: 's2', g: 'spatial', txt: 'f1k1', tip: 'spatial memory 이미지 1장 · 원본 해상도 (공식 코드: greedy가 첫 번째로 고른 = 새 시점을 가장 많이 덮는 이미지)' },
  { id: 't1', g: 'temporal', txt: 'f16k4', tip: '오래된 Latent Frame 16개 · 공간축 4배 추가 압축 → 1개당 Token 1/16 (16개 = 원본 1장 분량)' },
  { id: 't2', g: 'temporal', txt: 'f2k2', tip: '그다음 Latent Frame 2개 · 공간축 2배 추가 압축 → 1개당 Token ¼' },
  { id: 't3', g: 'temporal', txt: 'f1k1', tip: '가장 최근 Latent Frame 1개 · 추가 압축 없음' },
  { id: 'g', g: 'gen', txt: 'g20', tip: '생성 대상 20 Latent Frames (RGB 80장) · 노이즈에서 시작' },
]
const groups: { g: G, en: string, ko: string, cnt: string, part: string, add?: { t: string, sym?: string, post?: string }[] }[] = [
  { g: 'anchor', en: 'Anchor', ko: '입력 이미지 I₀', cnt: '1장', part: 'Part 4' },
  { g: 'spatial', en: 'Spatial', ko: 'spatial memory에서 가져온 이미지', cnt: '5장', part: 'Part 3', add: [{ t: '좌표맵', sym: 'C' }] },
  { g: 'temporal', en: 'Temporal', ko: '최근 생성한 프레임', cnt: '최근 19 Latent Frames', part: 'Part 4' },
  { g: 'gen', en: 'Generation', ko: '생성할 구간 (노이즈 latent)', cnt: '생성 대상 20 Latent Frames (RGB 80장)', part: '생성', add: [{ t: 'Warped 좌표맵 및 Depth', sym: 'Ĉ', post: '(4채널)' }, { t: 'Warped RGB' }] },
]
const under: Record<G, string> = { anchor: 'anchor', spatial: 'spatial slots', temporal: 'temporal slots', gen: 'generate' }
const hv = ref<string | null>(null) // token id or group key
const on = (tok: string, g: G) => !hv.value || hv.value === tok || hv.value === g
const tip = computed(() => toks.find(t => t.id === hv.value)?.tip ?? null)
const noise = ref('')
onMounted(() => {
  const c = document.createElement('canvas'); c.width = 6; c.height = 6; const x = c.getContext('2d')!
  for (let i = 0; i < 36; i++) { x.fillStyle = `hsl(${Math.random() * 360} 55% ${35 + Math.random() * 35}%)`; x.fillRect(i % 6, Math.floor(i / 6), 1, 1) }
  noise.value = c.toDataURL()
})
const shade = (i: number) => 0.55 + ((i * 37) % 9) / 22
// each tile = one whole frame shrunk (not a cut piece): show the scene photo, shifted per frame like a moving camera
const pic = `url(${import.meta.env.BASE_URL}lyra/fig/street_clean.jpg)`
const sPos = [8, 70, 30, 92, 50] // retrieved: from scattered times
const fr = (pos: number) => ({ backgroundImage: pic, backgroundPosition: `${pos}% 50%` })
const vel = katex.renderToString('v_\\theta(\\mathbf{z}_t,\\,t,\\,\\mathbf{c})\\ \\approx\\ \\boldsymbol{\\epsilon}-\\mathbf{z}_0', { throwOnError: false })
</script>

<template>
  <div class="cl">
    <div class="row grid">
      <div v-for="gr in groups" :key="gr.g" class="col" :class="gr.g">
        <div class="card" :class="{ dim: hv && !on('', gr.g) && !toks.some(t => t.id === hv && t.g === gr.g) }" @mouseenter="hv = gr.g" @mouseleave="hv = null">
          <div class="hd"><b>{{ gr.en }}</b><span class="pt">{{ gr.part }}</span></div>
          <div class="ko">{{ gr.ko }}</div>
          <div class="tiles">
            <template v-if="gr.g === 'anchor'">
              <div class="t k1 ph" :class="{ off: !on('a', 'anchor') }" :style="{ backgroundImage: pic, backgroundSize: 'cover' }"><i>I₀</i></div>
            </template>
            <template v-else-if="gr.g === 'spatial'">
              <div class="grid2" :class="{ off: !on('s1', 'spatial') }"><div v-for="i in 4" :key="i" class="t k2 ph" :style="fr(sPos[i - 1])" /></div>
              <div class="t k1 ph" :class="{ off: !on('s2', 'spatial') }" :style="fr(sPos[4])" />
            </template>
            <template v-else-if="gr.g === 'temporal'">
              <div class="grid4" :class="{ off: !on('t1', 'temporal') }"><div v-for="i in 16" :key="i" class="t k4 ph" :style="fr((i - 1) * 4)" /></div>
              <div class="col2" :class="{ off: !on('t2', 'temporal') }"><div v-for="i in 2" :key="i" class="t k2 ph" :style="fr(64 + i * 6)" /></div>
              <div class="t k1 ph" :class="{ off: !on('t3', 'temporal') }" :style="fr(84)" />
            </template>
            <template v-else>
              <div class="deck" :class="{ off: !on('g', 'gen') }">
                <div v-for="i in 20" :key="i" class="t k1 nz" :style="{ left: `${(i - 1) * 2.4}px`, backgroundImage: i === 20 ? `url(${noise})` : 'none' }" />
              </div>
            </template>
          </div>
          <div class="cnt">{{ gr.cnt }}</div>
          <div v-if="gr.add" class="adds"><span v-for="a in gr.add" :key="a.t" class="add">+ {{ a.t }}<i v-if="a.sym"> {{ a.sym }}<sub>j</sub></i><i v-if="a.sym === 'Ĉ'">, D̂<sub>j</sub></i><template v-if="a.post"> {{ a.post }}</template></span></div>
        </div>
        <div class="stem" />
      </div>
    </div>
    <div class="dit">
      <b>DiT Self-Attention</b> <span class="mu">· 네 그룹의 토큰을 한 시퀀스로 처리 (Wan 2.1 14B) · 모든 토큰에 + Plücker Ray (카메라 광선 정보, Q/K 주입)</span>
    </div>
    <div class="outp">↓ 생성 구간 latent의 <b>velocity</b> 예측 <span class="kx" v-html="vel" /> <span class="mu">→ 35 step 반복해서 노이즈 제거</span></div>
    <div class="nota">
      <span class="pl">논문 표기</span>
      <div class="seq grid">
        <div v-for="gr in groups" :key="gr.g" class="brace" :class="gr.g">
          <div class="tk">
            <span v-for="t in toks.filter(t => t.g === gr.g)" :key="t.id" class="tok" :class="{ hl: hv === t.id || hv === gr.g }" @mouseenter="hv = t.id" @mouseleave="hv = null">{{ t.txt }}</span>
          </div>
          <div class="ub">{{ under[gr.g] }}</div>
        </div>
      </div>
      <div class="tipl">
        <template v-if="tip"><b>{{ toks.find(t => t.id === hv)?.txt }}</b> = {{ tip }}</template>
        <template v-else><code>fnkm</code> = Latent Frame n개를 공간축 m배 추가 압축하여 Token화 (§3) · 작은 칸 = 프레임 한 장을 <b class="w">통째로 줄인 것</b> (잘라낸 조각 아님)</template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cl { display: flex; flex-direction: column; }
.grid { display: grid; grid-template-columns: 125px 215px 230px 250px; column-gap: 1rem; justify-content: center; }
.col { display: flex; flex-direction: column; align-items: center; }
.col .card { flex: 1; display: flex; flex-direction: column; }
.col .tiles { flex: 1; }
.stem { height: 20px; }
.card { width: 100%; box-sizing: border-box; border: 1.5px solid var(--c); background: color-mix(in srgb, var(--c) 10%, transparent); border-radius: 10px; padding: .4rem .65rem .35rem; transition: opacity .15s; cursor: default; }
.card.dim { opacity: .35; }
.anchor { --c: #a78bfa; } .spatial { --c: #60a5fa; } .temporal { --c: #6fcf97; } .gen { --c: #f0a35e; }
.hd { display: flex; justify-content: space-between; align-items: baseline; gap: .6rem; }
.hd b { color: var(--c); font-size: 1.1rem; }
.pt { white-space: nowrap; font-size: .58rem; color: var(--lx-muted); border: 1px solid var(--lx-line); border-radius: 4px; padding: 0 .3rem; }
.ko { white-space: nowrap; font-size: .72rem; color: var(--lx-muted); margin-bottom: .35rem; }
.tiles { display: flex; align-items: center; justify-content: center; gap: 9px; height: 64px; }
.t { background: var(--c); border-radius: 3px; }
.ph { background-size: auto 100%; background-repeat: no-repeat; box-shadow: inset 0 0 0 1.5px var(--c); }
.k4.ph { box-shadow: inset 0 0 0 1px var(--c); }
.k1 i { color: #fff !important; text-shadow: 0 0 4px #000, 0 0 2px #000; }
.tipl .w { font-family: inherit; color: var(--lx-text); }
.k1 { width: 64px; height: 64px; display: grid; place-items: center; }
.k1 i { font-style: italic; font-family: 'Times New Roman', serif; font-size: 1.25rem; color: #1b1340; }
.k2 { width: 30px; height: 30px; }
.k4 { width: 14.5px; height: 14.5px; border-radius: 2px; }
.grid2 { display: grid; grid-template-columns: repeat(2, 30px); gap: 4px; }
.grid4 { display: grid; grid-template-columns: repeat(4, 14.5px); gap: 2px; }
.col2 { display: flex; flex-direction: column; gap: 4px; }
.off { opacity: .15; }
.deck { position: relative; width: 114px; height: 64px; }
.nz { position: absolute; top: 0; background-size: cover; image-rendering: pixelated; border: 1px solid #f0a35e99; background-color: #4a2c12; }
.cnt { font-size: .8rem; margin-top: .35rem; }
.adds { display: flex; flex-wrap: wrap; gap: .1rem .5rem; margin-top: .1rem; }
.add { font-size: .64rem; color: var(--lx-accent); }
.add i { font-family: 'Times New Roman', serif; font-size: .8rem; }
.stem { width: 2px; height: 14px; background: #4b5563; }
.dit { text-align: center; padding: .5rem; border-radius: 10px; border: 1.5px solid #6b7fa8; background: #1c2333; font-size: 1rem; width: calc(125px + 215px + 230px + 250px + 3rem); margin: 0 auto; box-sizing: border-box; }
.mu { color: var(--lx-muted); font-weight: 400; font-size: .72rem; }
.outp { text-align: center; font-size: .86rem; margin-top: .4rem; }
.outp b { color: #f0a35e; }
.kx :deep(.katex) { font-size: 1.05em; }
.nota { margin-top: 1rem; border-top: 1px dashed var(--lx-line); padding-top: .5rem; position: relative; }
.pl { display: inline-block; margin-bottom: .25rem; font-size: .6rem; font-weight: 700; letter-spacing: .06em; color: #0d1117; background: #cbd5e1; border-radius: 4px; padding: 0 .35rem; }

.brace { display: flex; flex-direction: column; align-items: center; }
.tk { display: flex; gap: .35rem; padding-bottom: 2px; border-bottom: 2px solid var(--c); border-radius: 0 0 6px 6px; padding-inline: .3rem; }
.tok { font-family: "Fira Code", Consolas, ui-monospace, monospace; font-size: 1rem; padding: 0 .2rem; border-radius: 4px; cursor: pointer; }
.tok.hl { background: var(--c); color: #0d1117; }
.ub { font-size: .68rem; color: var(--c); margin-top: .1rem; }
.tipl { text-align: center; font-size: .8rem; min-height: 1.2rem; margin-top: .35rem; }
.tipl b { font-family: ui-monospace, monospace; color: var(--lx-accent); }
.tipl code { background: none; color: var(--lx-text); }
</style>
