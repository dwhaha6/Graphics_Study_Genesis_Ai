<script setup lang="ts">
import { computed, ref } from 'vue'

// Paper Figure 2 with highlight tabs. Regions are [x0, y0, x1, y1] in % of the figure image.
// Optional video (looped segment vstart..vend) is shown next to the text on tabs with vid: true.
type R = [number, number, number, number]
const props = defineProps<{ video?: string, poster?: string, vstart?: number, vend?: number }>()
const base = import.meta.env.BASE_URL
const tabs: { key: string, label: string, t: string, rs: R[], b: string[], vid?: boolean }[] = [
  {
    key: 'all', label: '전체', t: '그림 2 · 전체 흐름', rs: [],
    b: [
      '사진 1장에서 시작 → 사용자가 경로를 줄 때마다 <b>구간 하나씩</b> 만들기를 반복 → 마지막에 3D로',
      '<b>왼쪽</b>: 시스템 전체 흐름 · <b>오른쪽</b>: 구간 하나를 만드는 영상 모델 내부',
    ],
  },
  {
    key: 'input', label: '사용자 입력', vid: true, t: '사용자 입력', rs: [[1.2, 7.3, 41.0, 39.0], [0.5, 36.5, 28.3, 97.7]],
    b: [
      '지금까지 만든 point cloud를 보며 <b>다음 카메라 경로</b>를 그림 (텍스트 설명은 선택)',
    ],
  },
  {
    key: 'ret', label: '① Retrieve', t: '① Retrieve: 기억에서 찾기', rs: [[51.3, 14.0, 72.7, 97.2], [72.6, 62.3, 81.6, 77.2]],
    b: ['가려는 곳을 예전에 본 프레임을 <b>기억(Spatial memory)</b>에서 찾아옴'],
  },
  {
    key: 'gen', label: '② Generate', t: '② Generate: 새 구간 그리기', rs: [[28.7, 37.2, 40.2, 58.3], [72.4, 20.2, 99.7, 98.1]],
    b: ['찾아온 프레임 + 최근 프레임을 참고해 영상 모델이 <b>새 구간</b>을 그림'],
  },
  {
    key: 'upd', label: '③ Update', t: '③ Update: 기억에 추가', rs: [[62.3, 1.9, 96.0, 17.5], [52.4, 15.4, 71.4, 35.9], [51.7, 37.7, 63.6, 54.8], [20.7, 31.5, 29.2, 54.8]],
    b: ['새로 그린 프레임을 <b>기억에 추가</b> → 다시 사용자 입력으로 (반복)'],
  },
  {
    key: 'rec', label: '3D 복원', t: '3D 복원', rs: [[41.4, 3.3, 50.1, 97.4], [28.8, 68.2, 40.3, 89.2]],
    b: ['탐험이 끝나면 쌓인 영상으로 <b>3DGS · 메쉬</b>를 만듦'],
  },
]
const sel = ref('all')
const cur = computed(() => tabs.find(t => t.key === sel.value)!)
const showVid = computed(() => !!(cur.value.vid && props.video))
const url = (p: string) => (/^https?:\/\//.test(p) ? p : base + p)
function onMeta(e: Event) { (e.target as HTMLVideoElement).currentTime = props.vstart ?? 0 }
function onTime(e: Event) {
  const v = e.target as HTMLVideoElement
  if (props.vend != null && v.currentTime >= props.vend) v.currentTime = props.vstart ?? 0
}
</script>

<template>
  <div class="f2">
    <div class="tabs">
      <button v-for="t in tabs" :key="t.key" :class="{ on: sel === t.key }" @click="sel = t.key">{{ t.label }}</button>
    </div>
    <div class="fig">
      <img :src="`${base}lyra/fig/figure2.jpg`" draggable="false">
      <svg v-if="cur.rs.length" class="ov" viewBox="0 0 100 100" preserveAspectRatio="none">
        <defs>
          <mask :id="`f2m-${cur.key}`">
            <rect x="0" y="0" width="100" height="100" fill="white" />
            <rect v-for="(r, i) in cur.rs" :key="i" :x="r[0]" :y="r[1]" :width="r[2] - r[0]" :height="r[3] - r[1]" fill="black" />
          </mask>
        </defs>
        <rect x="0" y="0" width="100" height="100" fill="#0d1117" opacity=".7" :mask="`url(#f2m-${cur.key})`" />
        <rect v-for="(r, i) in cur.rs" :key="`o${i}`" :x="r[0]" :y="r[1]" :width="r[2] - r[0]" :height="r[3] - r[1]" class="hl" />
      </svg>
      <div v-if="showVid" class="ovv">
        <video :src="url(props.video!)" :poster="props.poster ? url(props.poster) : undefined"
          autoplay muted playsinline preload="auto" @loadedmetadata="onMeta" @timeupdate="onTime" />
        <span>실제 GUI 화면</span>
      </div>
    </div>
    <div class="ex">
      <div class="t">{{ cur.t }}</div>
      <ul><li v-for="(b, i) in cur.b" :key="i" v-html="b" /></ul>
    </div>
  </div>
</template>

<style scoped>
.f2 { display: flex; flex-direction: column; gap: .45rem; }
.tabs { display: flex; gap: .4rem; flex-wrap: wrap; }
.tabs button { font-size: .78rem; padding: .25rem .75rem; border-radius: 8px; border: 1px solid var(--lx-line); color: var(--lx-muted); background: var(--lx-panel); }
.tabs button.on { color: #0d1117; background: var(--lx-accent); border-color: var(--lx-accent); font-weight: 700; }
.fig { position: relative; border-radius: 8px; overflow: hidden; background: #fff; }
.fig img { display: block; width: 100%; }
.ov { position: absolute; inset: 0; width: 100%; height: 100%; }
.hl { fill: none; stroke: var(--lx-accent); stroke-width: 2.5; vector-effect: non-scaling-stroke; rx: .6; }
.ex { background: var(--lx-panel); border: 1px solid var(--lx-line); border-radius: 10px; padding: .5rem .8rem; min-height: 4.6rem; }
.ovv { position: absolute; top: 3%; bottom: 3%; right: 1.5%; aspect-ratio: 16 / 9; border-radius: 8px; overflow: hidden; border: 2px solid var(--lx-accent); box-shadow: 0 6px 24px rgba(0,0,0,.5); background: #000; }
.ovv video { width: 100%; height: 100%; object-fit: cover; display: block; }
.ovv span { position: absolute; left: .5rem; top: .4rem; font-size: .7rem; font-weight: 700; color: #0d1117; background: var(--lx-accent); padding: .05rem .45rem; border-radius: 5px; }
.ex .t { font-weight: 700; font-size: .9rem; color: var(--lx-accent); }
.ex ul { margin: .2rem 0 0; padding-left: 1.1rem; }
.ex li { font-size: .88rem; line-height: 1.55; }
.ex :deep(.mu) { color: var(--lx-muted); }
</style>
