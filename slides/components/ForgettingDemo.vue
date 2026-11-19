<script setup lang="ts">
import { computed, ref } from 'vue'

type Room = 'A' | 'B' | 'C'
const steps: { room: Room, label: string, x: number, y: number, face: number }[] = [
  { room: 'A', label: '① 거실 A', x: 110, y: 125, face: 180 },
  { room: 'B', label: '② 복도 B', x: 200, y: 125, face: 0 },
  { room: 'C', label: '③ 침실 C', x: 300, y: 125, face: 0 },
  { room: 'B', label: '④ 다시 복도 B', x: 200, y: 125, face: 180 },
  { room: 'A', label: '⑤ 다시 거실 A', x: 110, y: 125, face: 180 },
]
// showRecall: shows the "retrieve past view" toggle (Lyra 2.0 idea); off in the intro, for use in the method part
const props = withDefaults(defineProps<{ showRecall?: boolean }>(), { showRecall: false })
const CTX = 2 // illustrative context length
const step = ref(0)
const recall = ref(false)
const cur = computed(() => steps[step.value])
const trail = computed(() => {
  const pts = steps.slice(0, step.value + 1).map((s, i) => `${s.x} ${s.y + (i >= 3 ? 14 : 0)}`)
  return `M${pts.join(' L')}`
})
const revisit = computed(() => step.value === 4)
const viewKind = computed(() => {
  const r = cur.value.room
  if (r === 'A')
    return revisit.value && !recall.value ? 'living-forgot' : 'living'
  return r === 'B' ? 'hall' : 'bed'
})
function frameState(i: number) {
  if (i === step.value) return 'cur'
  if (revisit.value && recall.value && i === 0) return 'recall'
  if (i >= step.value - CTX && i < step.value) return 'ctx'
  return 'old'
}
const status = computed(() => {
  switch (step.value) {
    case 0: return '거실을 처음 봅니다. 파란 소파, 창문, 풍경화, 화분이 있습니다.'
    case 1: return '복도로 이동합니다. 모델은 직전 장면들을 보면서 다음 장면을 이어 만듭니다.'
    case 2: return '침실에 도착했습니다. 카메라가 움직일수록 오래된 장면은 참고 범위에서 밀려납니다.'
    case 3: return '다시 복도로 돌아갑니다. 처음 본 거실(①)은 이제 참고 범위 밖입니다.'
    default: return recall.value
      ? '3D 위치 정보로 "이 자리를 비췄던 과거 장면(①)"을 찾아와 참고 → 처음 본 거실과 같은 모습'
      : '참고할 거실 장면이 없어서 새로 지어냄 → 소파 색·위치, 창문, 그림이 처음과 달라짐'
  }
})
function go(d: number) { step.value = Math.min(4, Math.max(0, step.value + d)) }
</script>

<template>
  <div class="fd">
    <div class="left">
      <svg viewBox="0 0 400 250" class="plan">
        <rect x="10" y="10" width="150" height="230" rx="4" class="room" :class="{ here: cur.room === 'A' }" />
        <rect x="160" y="95" width="80" height="60" class="room" :class="{ here: cur.room === 'B' }" />
        <rect x="240" y="10" width="150" height="230" rx="4" class="room" :class="{ here: cur.room === 'C' }" />
        <text x="85" y="32" class="rl">거실 A</text>
        <text x="200" y="88" class="rl">복도 B</text>
        <text x="315" y="32" class="rl">침실 C</text>
        <rect x="24" y="150" width="28" height="70" rx="4" fill="#3b82f6" />
        <rect x="70" y="175" width="34" height="26" rx="3" fill="#a78b6d" />
        <circle cx="135" cy="218" r="10" fill="#3f8f4f" />
        <rect x="318" y="140" width="56" height="80" rx="4" fill="#a78bfa" />
        <rect x="256" y="24" width="20" height="60" rx="2" fill="#8d6e63" />
        <path :d="trail" fill="none" stroke="#5eead4" stroke-width="2.5" stroke-dasharray="6 5" />
        <g :transform="`translate(${cur.x} ${cur.y + (step >= 3 ? 14 : 0)}) rotate(${cur.face})`" class="cam">
          <path d="M0 0 L60 -28 L60 28 Z" fill="#fbbf24" opacity=".22" />
          <circle r="10" fill="#fbbf24" stroke="#0d1117" stroke-width="2" />
        </g>
      </svg>
      <div class="ctrl">
        <button :disabled="step === 0" @click="go(-1)">◀</button>
        <span class="lab">{{ cur.label }}</span>
        <button :disabled="step === 4" @click="go(1)">▶</button>
        <label v-if="props.showRecall" class="tg"><input v-model="recall" type="checkbox"> 과거 장면 찾아오기 <small>(Lyra 2.0 방식 미리보기)</small></label>
      </div>
      <div class="strip">
        <div v-for="(s, i) in steps.slice(0, step + 1)" :key="i" class="fr" :class="frameState(i)">
          <span>{{ s.label.split(' ')[0] }} {{ s.room }}</span>
        </div>
      </div>
      <div class="legend">
        <span><i class="sw cur" />지금 만드는 장면</span>
        <span><i class="sw ctx" />모델이 참고하는 범위</span>
        <span><i class="sw old" />범위 밖 (잊힘)</span>
        <span v-if="recall"><i class="sw recall" />3D로 찾아온 장면</span>
      </div>
    </div>

    <div class="right">
      <template v-if="revisit">
        <div class="pair">
          <div><div class="cap">① 처음 본 거실</div><RoomView kind="living" /></div>
          <div><div class="cap" :class="recall ? 'ok' : 'bad'">⑤ 다시 만든 거실</div><RoomView :kind="viewKind" :marks="true" /></div>
        </div>
      </template>
      <template v-else>
        <div class="cap">카메라에 보이는 장면</div>
        <RoomView :kind="viewKind" />
      </template>
      <p class="status" :class="{ bad: revisit && !recall, ok: revisit && recall }">{{ status }}</p>
    </div>
  </div>
</template>

<style scoped>
.fd { display: grid; grid-template-columns: 1fr 1fr; gap: 1.1rem; align-items: start; }
.plan { width: 100%; background: var(--lx-panel); border: 1px solid var(--lx-line); border-radius: 12px; }
.room { fill: #1c2633; stroke: #4b5563; stroke-width: 1.5; transition: fill .3s; }
.room.here { fill: #24364a; stroke: #fbbf24; }
.rl { font-size: 12px; fill: #cbd5e1; text-anchor: middle; }
.cam { transition: transform .45s ease; }
.ctrl { display: flex; align-items: center; gap: .5rem; margin-top: .45rem; flex-wrap: wrap; }
.ctrl button { padding: .15rem .6rem; border-radius: 6px; background: var(--lx-panel2); border: 1px solid var(--lx-line); }
.ctrl button:disabled { opacity: .3; }
.lab { min-width: 6.5rem; text-align: center; font-weight: 700; font-size: .85rem; }
.tg { font-size: .72rem; color: var(--lx-muted); display: flex; align-items: center; gap: .3rem; cursor: pointer; }
.tg small { font-size: .65rem; }
.strip { display: flex; gap: .3rem; margin-top: .45rem; }
.fr { font-size: .65rem; padding: .25rem .4rem; border-radius: 6px; border: 2px solid var(--lx-line); background: var(--lx-panel); white-space: nowrap; }
.fr.cur { border-color: #fff; } .fr.ctx { border-color: var(--lx-accent); } .fr.old { opacity: .4; } .fr.recall { border-color: #fb923c; }
.legend { display: flex; gap: .8rem; font-size: .62rem; color: var(--lx-muted); margin-top: .35rem; flex-wrap: wrap; }
.sw { display: inline-block; width: 9px; height: 9px; border-radius: 2px; margin-right: .25rem; border: 2px solid; }
.sw.cur { border-color: #fff; } .sw.ctx { border-color: var(--lx-accent); } .sw.old { border-color: var(--lx-line); } .sw.recall { border-color: #fb923c; }
.right { display: flex; flex-direction: column; gap: .4rem; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: .5rem; }
.cap { font-size: .72rem; color: var(--lx-muted); margin-bottom: .2rem; }
.cap.bad { color: var(--lx-bad); font-weight: 700; } .cap.ok { color: var(--lx-good); font-weight: 700; }
.status { font-size: .85rem; line-height: 1.45; margin: .2rem 0 0; }
.status.bad { color: #fca5a5; } .status.ok { color: #86efac; }
</style>
