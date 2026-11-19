<script setup lang="ts">
import { computed, ref } from 'vue'

const tab = ref<1 | 2 | 3>(1)
const loops = ref(0)
const loopText = computed(() => [
  '생성한 프레임에 작은 오류(빨간 점)가 하나 생겼다고 해 봅시다.',
  '그 프레임이 3D 모형에 합쳐짐 → 모형 자체가 망가짐',
  '망가진 모형을 렌더링한 화면이 다음 생성의 조건으로 → 오류가 더 커짐',
  '돌수록 오류가 증폭됨 (error amplification)',
  '돌수록 오류가 증폭됨 (error amplification)',
][loops.value])
</script>

<template>
  <div class="mc">
    <div class="tabs">
      <button :class="{ on: tab === 1 }" @click="tab = 1">① 3D 모형에 쌓아서 참고</button>
      <button :class="{ on: tab === 2 }" @click="tab = 2">② 과거 프레임만 같이 보여주기</button>
      <button class="lyra" :class="{ on: tab === 3 }" @click="tab = 3">③ Lyra 2.0</button>
    </div>

    <!-- ① cumulative 3D representation -->
    <div v-if="tab === 1" class="body">
      <svg viewBox="0 0 440 250" class="dg">
        <defs><marker id="ah1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#9aa5b1" /></marker></defs>
        <g class="nd"><rect x="20" y="100" width="110" height="50" rx="10" /><text x="75" y="130">영상 모델</text></g>
        <g class="nd" :class="{ hurt: true }"><rect x="165" y="15" width="110" height="50" rx="10" /><text x="220" y="45">새 프레임</text></g>
        <g class="nd" :class="{ hurt: loops >= 1 }"><rect x="310" y="100" width="115" height="50" rx="10" /><text x="367" y="122">하나로 합친</text><text x="367" y="139">3D 모형</text></g>
        <g class="nd" :class="{ hurt: loops >= 2 }"><rect x="165" y="185" width="110" height="50" rx="10" /><text x="220" y="207">3D 모형을</text><text x="220" y="224">렌더링한 화면</text></g>
        <path d="M95 98 Q110 45 162 40" class="ar" marker-end="url(#ah1)" />
        <path d="M278 40 Q340 45 360 97" class="ar" marker-end="url(#ah1)" />
        <path d="M360 153 Q340 205 278 210" class="ar" marker-end="url(#ah1)" />
        <path d="M162 210 Q110 205 95 153" class="ar" marker-end="url(#ah1)" />
        <circle cx="272" cy="17" :r="Math.min(4 + loops * 2.5, 13)" class="blot" />
        <circle v-if="loops >= 1" cx="423" cy="102" :r="Math.min(2 + loops * 3, 14)" class="blot" />
        <circle v-if="loops >= 2" cx="272" cy="187" :r="Math.min(loops * 3.5, 14)" class="blot" />
        <text x="220" y="133" class="cnt">{{ loops }}바퀴</text>
      </svg>
      <div class="ex">
        <p class="who">예: GEN3C, <b>Lyra 1.0 (전작)</b></p>
        <p>생성한 프레임들을 <b>하나의 3D 모형</b>에 계속 쌓고, 그 모형을 렌더링한 화면을 보고 다음 프레임을 만듦</p>
        <p class="good">＋ 3D라는 확실한 공간 기준이 있음</p>
        <p class="badc">－ {{ loopText }}</p>
        <div class="btns">
          <button @click="loops = Math.min(4, loops + 1)">한 바퀴 더 돌리기 ▶</button>
          <button @click="loops = 0">처음으로</button>
        </div>
      </div>
    </div>

    <!-- ② history frames + camera pose only -->
    <div v-else-if="tab === 2" class="body">
      <svg viewBox="0 0 440 250" class="dg">
        <g transform="translate(15 40)">
          <rect width="150" height="110" rx="8" class="pic" />
          <polygon points="25,95 25,50 70,25 115,50 115,95" fill="#d6c3a5" />
          <rect x="55" y="62" width="22" height="33" fill="#dc2626" />
          <rect x="88" y="58" width="18" height="16" fill="#60a5fa" />
          <text x="75" y="-8" class="cap2">과거 프레임 (앞에서 본 집)</text>
        </g>
        <g transform="translate(275 40)">
          <rect width="150" height="110" rx="8" class="pic" />
          <polygon points="20,95 20,55 55,30 130,45 130,95" fill="#c9b38f" />
          <polygon points="20,95 20,55 55,30 55,95" fill="#d6c3a5" />
          <rect x="28" y="66" width="12" height="29" fill="#dc2626" />
          <rect x="85" y="60" width="26" height="16" fill="#e5e7eb" />
          <text x="75" y="-8" class="cap2">지금 그릴 시점 (옆에서 본 집)</text>
        </g>
        <path d="M95 125 C170 200 280 200 312 125" class="q" />
        <path d="M120 105 C190 30 300 40 370 105" class="q" />
        <text x="220" y="205" class="qm">?</text>
        <text x="245" y="58" class="qm">?</text>
        <text x="220" y="240" class="cap2">카메라 위치 숫자만 주고, 어디가 어디인지는 모델이 알아서 찾아야 함</text>
      </svg>
      <div class="ex">
        <p class="who">예: 카메라 포즈 임베딩 (CameraCtrl 방식)</p>
        <p>오래된 프레임을 그대로 모델에 넣고, 각 프레임의 <b>카메라 위치 정보</b>만 함께 알려줌</p>
        <p class="good">＋ 망가진 3D 모형을 거치지 않음</p>
        <p class="badc">－ 과거 프레임의 어느 부분이 지금 화면의 어디에 해당하는지 모델 내부(self-attention)가 스스로 알아내야 함 → 시점 차이가 크면 자주 실패</p>
      </div>
    </div>

    <!-- ③ Lyra 2.0 -->
    <div v-else class="body">
      <svg viewBox="0 0 440 250" class="dg">
        <defs><marker id="ah3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#5eead4" /></marker></defs>
        <text x="15" y="16" class="cap2" style="text-anchor: start">3D 기억: 프레임마다 따로 보관</text>
        <g v-for="i in 5" :key="i" :transform="`translate(15 ${22 + (i - 1) * 44})`">
          <rect width="95" height="38" rx="6" :class="['card', { pick: i === 2 || i === 4 }]" />
          <text x="10" y="24" class="fn">#{{ i * 37 }}</text>
          <circle v-for="d in 7" :key="d" :cx="45 + (d * 7) % 40" :cy="10 + (d * 11) % 22" r="2" :fill="i === 2 || i === 4 ? '#5eead4' : '#64748b'" />
        </g>
        <path d="M112 85 C150 85 150 110 178 112" class="ar3" marker-end="url(#ah3)" />
        <path d="M112 173 C150 173 150 140 178 138" class="ar3" marker-end="url(#ah3)" />
        <text x="145" y="64" class="tip">ⓐ 지금 시점에서 잘 보이는 프레임 고르기</text>
        <rect x="180" y="95" width="90" height="60" rx="8" class="tgt" />
        <line v-for="g in 3" :key="'v' + g" :x1="180 + g * 22.5" y1="95" :x2="180 + g * 22.5" y2="155" class="grid" />
        <line v-for="g in 2" :key="'h' + g" x1="180" :y1="95 + g * 20" x2="270" :y2="95 + g * 20" class="grid" />
        <text x="225" y="172" class="cap2">ⓑ 픽셀마다 대응 위치 표시</text>
        <path d="M272 125 L318 125" class="ar3" marker-end="url(#ah3)" />
        <rect x="320" y="92" width="108" height="66" rx="10" class="vm" />
        <text x="374" y="120" class="vmt">영상 모델이</text>
        <text x="374" y="138" class="vmt">직접 그림</text>
        <text x="374" y="190" class="cap2">외형은 생성 모델의 몫</text>
      </svg>
      <div class="ex">
        <p class="who lyra">Lyra 2.0: 두 방식의 장점만</p>
        <p>3D 정보는 <b>"길잡이"</b>로만 사용 (information routing)</p>
        <p>ⓐ 수백 프레임 전이라도 지금 시점과 <b>3D로 겹치는 과거 프레임</b>을 찾아옴</p>
        <p>ⓑ 그 프레임의 어느 픽셀이 지금 화면의 어디로 가는지 <b>대응 관계</b>를 알려줌</p>
        <p>그림(외형)은 3D 모형을 렌더링하지 않고 <b>영상 모델이 직접</b> 그림 → 3D 오류가 그대로 옮겨지지 않음</p>
        <p class="note">세부 방법은 Method 파트에서</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mc { display: flex; flex-direction: column; gap: .6rem; }
.tabs { display: flex; gap: .5rem; }
.tabs button { font-size: .8rem; padding: .3rem .8rem; border-radius: 8px; border: 1px solid var(--lx-line); color: var(--lx-muted); background: var(--lx-panel); }
.tabs button.on { color: #0d1117; background: #cbd5e1; border-color: #cbd5e1; font-weight: 700; }
.tabs button.lyra.on { background: var(--lx-accent); border-color: var(--lx-accent); }
.body { display: grid; grid-template-columns: 1.3fr 1fr; gap: 1.1rem; align-items: center; }
.dg { width: 100%; background: var(--lx-panel); border: 1px solid var(--lx-line); border-radius: 12px; }
.nd rect { fill: var(--lx-panel2); stroke: #4b5563; }
.nd text { fill: #e6edf3; font-size: 13px; text-anchor: middle; }
.nd.hurt rect { stroke: #ef4444; stroke-width: 2; transition: stroke .3s; }
.ar { fill: none; stroke: #9aa5b1; stroke-width: 2; }
.blot { fill: #ef4444; opacity: .85; transition: r .4s; }
.cnt { fill: var(--lx-muted); font-size: 12px; text-anchor: middle; }
.pic { fill: #e8f1f8; }
.cap2 { fill: var(--lx-muted); font-size: 11px; text-anchor: middle; }
.q { fill: none; stroke: #fbbf24; stroke-width: 2; stroke-dasharray: 5 5; }
.qm { fill: #fbbf24; font-size: 22px; font-weight: 700; text-anchor: middle; }
.card { fill: var(--lx-panel2); stroke: #4b5563; }
.card.pick { stroke: #5eead4; stroke-width: 2.5; }
.fn { fill: #9aa5b1; font-size: 10px; }
.ar3 { fill: none; stroke: #5eead4; stroke-width: 2; }
.tip { fill: #5eead4; font-size: 10.5px; }
.tgt { fill: #1f3b3a; stroke: #5eead4; }
.grid { stroke: #5eead4; opacity: .4; }
.vm { fill: #5eead4; }
.vmt { fill: #0d1117; font-size: 13px; font-weight: 700; text-anchor: middle; }
.ex p { margin: .3rem 0; font-size: .9rem; line-height: 1.45; }
.who { color: var(--lx-muted); font-size: .78rem !important; }
.who.lyra { color: var(--lx-accent); font-weight: 700; }
.good { color: #86efac; } .badc { color: #fca5a5; }
.note { color: var(--lx-muted); font-size: .72rem !important; }
.btns { display: flex; gap: .4rem; margin-top: .4rem; }
.btns button { font-size: .75rem; padding: .2rem .7rem; border-radius: 6px; background: var(--lx-panel2); border: 1px solid var(--lx-line); }
</style>
