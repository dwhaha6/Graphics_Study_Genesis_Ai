<script setup lang="ts">
import { computed, ref } from 'vue'

type Mode = 'train' | 'infer' | 'self'
const props = defineProps<{ src: string, modes?: Mode[] }>()
const has = (m: Mode) => !props.modes || props.modes.includes(m)
const base = import.meta.env.BASE_URL
const mode = ref<Mode>('train')
const clean = 'none'
const dirty = 'sepia(.2) hue-rotate(-12deg) saturate(1.3) blur(1px) contrast(1.12)'
const worse = 'sepia(.4) hue-rotate(-24deg) saturate(1.6) blur(2px) contrast(1.22)'

const view = computed(() => {
  if (mode.value === 'train') {
    return {
      hist: { f: clean, tag: '정답 영상', cls: 'ok' },
      out: { f: clean, tag: '정답 다음 구간', cls: 'ok' },
      text: '학습할 때는 과거 장면으로 항상 깨끗한 정답 영상을 줍니다.',
      sub: '모델은 "깨끗한 과거"만 보고 연습합니다.',
    }
  }
  if (mode.value === 'infer') {
    return {
      hist: { f: dirty, tag: '모델이 만든 결과 (조금 틀림)', cls: 'warn' },
      out: { f: worse, tag: '오류가 이어짐', cls: 'bad' },
      text: '실제로 쓸 때는 과거 장면이 모델 자신이 만든, 조금씩 틀린 결과입니다.',
      sub: '연습 때 본 적 없는 상황 → 오류를 고치지 못하고 다음 구간으로 넘김 (학습-실사용 차이)',
    }
  }
  return {
    hist: { f: dirty, tag: '일부러 흐트러뜨린 뒤 모델이 한 번에 복원한 결과', cls: 'warn' },
    out: { f: clean, tag: '그래도 정답 다음 구간', cls: 'ok' },
    text: '학습 중 70% 확률로, 과거 장면을 모델 자신의 "조금 틀린 결과"로 바꿔서 줍니다.',
    sub: '목표는 항상 깨끗한 정답 → 틀린 과거를 받아도 바로잡는 법을 배움. 추가 계산은 아주 적음',
  }
})
</script>

<template>
  <div class="sa">
    <div class="tabs">
      <button v-if="has('train')" :class="{ on: mode === 'train' }" @click="mode = 'train'">{{ props.modes ? '학습할 때' : '기존 학습' }}</button>
      <button v-if="has('infer')" :class="{ on: mode === 'infer' }" @click="mode = 'infer'">실제로 쓸 때</button>
      <button v-if="has('self')" class="lyra" :class="{ on: mode === 'self' }" @click="mode = 'self'">Self-Augmentation 학습</button>
    </div>
    <div class="flow">
      <div class="node">
        <div class="lbl">과거 장면 (조건)</div>
        <div class="img" :class="view.hist.cls"><img :src="base + props.src" :style="{ filter: view.hist.f }" draggable="false"></div>
        <div class="tag" :class="view.hist.cls">{{ view.hist.tag }}</div>
      </div>
      <div class="arr">→</div>
      <div class="model">영상 모델</div>
      <div class="arr">→</div>
      <div class="node">
        <div class="lbl">{{ mode === 'infer' ? '만들어진 다음 구간' : '학습 목표 (다음 구간)' }}</div>
        <div class="img" :class="view.out.cls"><img :src="base + props.src" :style="{ filter: view.out.f, transform: 'translateX(-8%) scale(1.2)' }" draggable="false"></div>
        <div class="tag" :class="view.out.cls">{{ view.out.tag }}</div>
      </div>
    </div>
    <p class="txt">{{ view.text }}</p>
    <p class="sub">{{ view.sub }}</p>
  </div>
</template>

<style scoped>
.sa { display: flex; flex-direction: column; gap: .5rem; }
.tabs { display: flex; gap: .5rem; }
.tabs button { font-size: .8rem; padding: .3rem .8rem; border-radius: 8px; border: 1px solid var(--lx-line); color: var(--lx-muted); background: var(--lx-panel); }
.tabs button.on { color: #0d1117; background: #cbd5e1; border-color: #cbd5e1; font-weight: 700; }
.tabs button.lyra.on { background: var(--lx-accent); border-color: var(--lx-accent); }
.flow { display: flex; align-items: center; gap: .6rem; }
.node { width: 230px; }
.lbl { font-size: .7rem; color: var(--lx-muted); margin-bottom: .2rem; }
.img { aspect-ratio: 832 / 428; overflow: hidden; border-radius: 8px; border: 3px solid; }
.img img { width: 100%; height: 100%; object-fit: cover; transition: filter .35s; }
.img.ok { border-color: var(--lx-good); } .img.warn { border-color: #fb923c; } .img.bad { border-color: var(--lx-bad); }
.tag { font-size: .7rem; margin-top: .2rem; font-weight: 700; min-height: 2.1em; }
.tag.ok { color: #86efac; } .tag.warn { color: #fdba74; } .tag.bad { color: #fca5a5; }
.arr { color: var(--lx-muted); font-size: 1.2rem; }
.model { padding: .9rem .8rem; border-radius: 10px; background: var(--lx-panel2); border: 1px solid #4b5563; font-weight: 700; font-size: .85rem; white-space: nowrap; }
.txt { font-size: .92rem; margin: .1rem 0 0; }
.sub { font-size: .8rem; color: var(--lx-muted); margin: 0; }
</style>
