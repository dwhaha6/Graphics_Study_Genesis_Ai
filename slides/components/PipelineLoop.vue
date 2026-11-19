<script setup lang="ts">
import { computed, ref } from 'vue'

// Concept walk-through of the retrieve-generate-update loop (§4.1, Fig. 2). Counts use 80 frames per step (Appendix A.3).
const phase = ref(0) // 0 input, 1 retrieve, 2 generate, 3 update, 4 export
const segs = ref(0) // generated segments
const mem = ref(0) // segments already written to memory
const info = [
  { t: '사용자 입력', d: '3D 화면에서 지금까지 만든 point cloud를 보며 카메라가 갈 경로를 그림. 새로 채울 내용을 텍스트로 적을 수도 있음.' },
  { t: '① Retrieve: 기억에서 찾기', d: '가려는 시점에서 보일 곳을 예전에 찍은 프레임을 기억에서 찾아옴 (최대 5장).' },
  { t: '② Generate: 새 구간 그리기', d: '찾아온 프레임, 최근 프레임, 카메라 정보를 보고 영상 모델이 노이즈에서 새 구간 80프레임을 그림.' },
  { t: '③ Update: 기억에 추가', d: '새 프레임을 영상에 쌓고, 프레임마다 깊이를 추정해 기억에 저장 → 3D 화면의 point cloud도 넓어짐. 다시 사용자 입력으로.' },
  { t: '마무리: 3D로 내보내기', d: '탐험이 끝나면 쌓인 영상 프레임 전체로 3DGS · 메쉬를 만듦.' },
]
const cur = computed(() => info[phase.value])
const on = (...p: number[]) => p.includes(phase.value)

function next() {
  if (phase.value === 4) { phase.value = 0; return }
  if (phase.value === 3) { phase.value = 0; return }
  phase.value++
  if (phase.value === 2) segs.value++
  if (phase.value === 3) mem.value++
}
function exportNow() { if (mem.value > 0) phase.value = 4 }
function reset() { phase.value = 0; segs.value = 0; mem.value = 0 }
</script>

<template>
  <div class="pl">
    <svg viewBox="0 0 470 268" class="dg">
      <defs>
        <marker id="plA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#9aa5b1" /></marker>
        <marker id="plB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#5eead4" /></marker>
      </defs>
      <!-- input -->
      <g class="nd" :class="{ on: on(0) }"><rect x="120" y="6" width="230" height="44" rx="10" /><text x="235" y="25">사용자 입력</text><text x="235" y="41" class="sm">처음: 사진 1장 · 매번: 카메라 경로 + 텍스트(선택)</text></g>
      <!-- loop nodes -->
      <g class="nd" :class="{ on: on(1) }"><rect x="8" y="82" width="140" height="50" rx="10" /><text x="78" y="103">① Retrieve</text><text x="78" y="120" class="sm">기억에서 과거 프레임 찾기</text></g>
      <g class="nd" :class="{ on: on(2) }"><rect x="165" y="82" width="140" height="50" rx="10" /><text x="235" y="103">② Generate</text><text x="235" y="120" class="sm">새 구간 80프레임 생성</text></g>
      <g class="nd" :class="{ on: on(3) }"><rect x="322" y="82" width="140" height="50" rx="10" /><text x="392" y="103">③ Update</text><text x="392" y="120" class="sm">깊이 추정 → 기억에 추가</text></g>
      <!-- memory + frames + output -->
      <g class="nd mem" :class="{ on: on(1, 3) }"><rect x="8" y="170" width="297" height="44" rx="10" /><text x="156" y="189">Spatial memory (기억)</text><text x="156" y="205" class="sm">프레임마다 깊이 · 카메라를 따로 저장 · 계속 커짐</text></g>
      <g class="nd" :class="{ on: on(3, 4) }"><rect x="322" y="170" width="140" height="44" rx="10" /><text x="392" y="189">쌓인 영상 프레임</text><text x="392" y="205" class="sm">Video frames</text></g>
      <g class="nd out" :class="{ on: on(4) }"><rect x="322" y="230" width="140" height="34" rx="10" /><text x="392" y="252">3DGS · 메쉬</text></g>
      <!-- arrows -->
      <path d="M150 50 L105 80" class="ar" :class="{ hot: on(1) }" :marker-end="on(1) ? 'url(#plB)' : 'url(#plA)'" />
      <path d="M150 107 L163 107" class="ar" :class="{ hot: on(2) }" :marker-end="on(2) ? 'url(#plB)' : 'url(#plA)'" />
      <path d="M307 107 L320 107" class="ar" :class="{ hot: on(3) }" :marker-end="on(3) ? 'url(#plB)' : 'url(#plA)'" />
      <path d="M392 80 C392 40 380 28 352 28" class="ar" :class="{ hot: on(0) && mem > 0 }" :marker-end="on(0) && mem > 0 ? 'url(#plB)' : 'url(#plA)'" />
      <text x="410" y="52" class="lb">반복</text>
      <path d="M78 168 L78 134" class="ar" :class="{ hot: on(1) }" :marker-end="on(1) ? 'url(#plB)' : 'url(#plA)'" />
      <path d="M345 134 L290 168" class="ar" :class="{ hot: on(3) }" :marker-end="on(3) ? 'url(#plB)' : 'url(#plA)'" />
      <path d="M410 134 L410 168" class="ar" :class="{ hot: on(3) }" :marker-end="on(3) ? 'url(#plB)' : 'url(#plA)'" />
      <path d="M392 216 L392 228" class="ar" :class="{ hot: on(4) }" :marker-end="on(4) ? 'url(#plB)' : 'url(#plA)'" />
    </svg>

    <div class="stats">
      <span>만든 구간 <b>{{ segs }}</b>개 · 새로 만든 프레임 <b>{{ segs * 80 }}</b>장</span>
      <span>기억에 들어간 구간 <b>{{ mem }}</b>개 <small>(+ 입력 사진)</small></span>
    </div>
    <div class="ex">
      <div class="t">{{ cur.t }}</div>
      <div class="d">{{ cur.d }}</div>
    </div>
    <div class="btns">
      <button class="go" @click="next">{{ phase === 3 ? '다음 경로로 ▶' : phase === 4 ? '처음 단계로' : '다음 단계 ▶' }}</button>
      <button :disabled="mem === 0" @click="exportNow">3D로 내보내기</button>
      <button @click="reset">처음부터</button>
    </div>
  </div>
</template>

<style scoped>
.pl { display: flex; flex-direction: column; gap: .4rem; }
.dg { width: 100%; background: var(--lx-panel); border: 1px solid var(--lx-line); border-radius: 12px; }
.nd rect { fill: var(--lx-panel2); stroke: #4b5563; stroke-width: 1.5; transition: all .25s; }
.nd text { fill: #e6edf3; font-size: 13px; font-weight: 700; text-anchor: middle; }
.nd text.sm { fill: var(--lx-muted); font-size: 9.5px; font-weight: 400; }
.nd.mem rect { fill: #2a2416; }
.nd.out rect { fill: #2b2140; }
.nd.on rect { stroke: var(--lx-accent); stroke-width: 3; }
.ar { fill: none; stroke: #9aa5b1; stroke-width: 1.8; transition: stroke .25s; }
.ar.hot { stroke: var(--lx-accent); stroke-width: 2.6; }
.lb { fill: var(--lx-muted); font-size: 10px; }
.stats { display: flex; gap: 1.2rem; font-size: .78rem; color: var(--lx-muted); }
.stats b { color: var(--lx-accent); font-size: .95rem; }
.ex { background: var(--lx-panel); border: 1px solid var(--lx-line); border-radius: 10px; padding: .45rem .7rem; min-height: 4.1rem; }
.ex .t { font-weight: 700; font-size: .88rem; color: var(--lx-accent); }
.ex .d { font-size: .82rem; line-height: 1.45; margin-top: .15rem; }
.btns { display: flex; gap: .4rem; }
.btns button { font-size: .75rem; padding: .25rem .75rem; border-radius: 7px; background: var(--lx-panel2); border: 1px solid var(--lx-line); }
.btns button:disabled { opacity: .4; cursor: default; }
.btns .go { background: var(--lx-accent); color: #0d1117; font-weight: 700; border-color: var(--lx-accent); }
</style>
