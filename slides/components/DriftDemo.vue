<script setup lang="ts">
import { computed, ref } from 'vue'

const props = defineProps<{ src: string }>()
const base = import.meta.env.BASE_URL
const MAX = 8
const k = ref(0)

// camera moves the same way on both sides; only the right side accumulates synthesis errors (illustrative)
const pan = (i: number) => `translateX(${-i * 2.2}%) scale(1.25)`
const drift = (i: number) =>
  `sepia(${i * 0.05}) hue-rotate(${i * -4}deg) saturate(${1 + i * 0.09}) contrast(${1 + i * 0.05}) blur(${i * 0.2}px)`
const warp = (i: number) => `${pan(i)} skewX(${i * 0.7}deg) scaleY(${1 - i * 0.01})`
const status = computed(() => {
  if (k.value === 0) return '두 화면 모두 같은 사진에서 출발합니다.'
  if (k.value <= 3) return '카메라가 옆으로 움직이는 것은 정상. 오른쪽은 아주 작은 차이가 생기기 시작합니다.'
  if (k.value <= 6) return '작은 오류가 다음 구간으로 넘어가며 색이 틀어지고 흐려집니다.'
  return '색, 선명도, 형태가 처음 사진과 눈에 띄게 달라졌습니다.'
})
const strip = computed(() => Array.from({ length: k.value + 1 }, (_, i) => i))
</script>

<template>
  <div class="dd">
    <div class="pair">
      <div>
        <div class="cap ok">이상적: 시점만 바뀜</div>
        <div class="frame"><img :src="base + props.src" :style="{ transform: pan(k) }" draggable="false"></div>
      </div>
      <div>
        <div class="cap bad">드리프트: 오류가 쌓임</div>
        <div class="frame"><img :src="base + props.src" :style="{ transform: warp(k), filter: drift(k) }" draggable="false"></div>
      </div>
    </div>
    <div class="ctrl">
      <span class="lab">구간 {{ k }}</span>
      <input v-model.number="k" type="range" min="0" :max="MAX">
      <button @click="k = Math.min(MAX, k + 1)">다음 구간 ▶</button>
      <button @click="k = 0">처음으로</button>
    </div>
    <div class="strip">
      <div v-for="i in strip" :key="i" class="th"><img :src="base + props.src" :style="{ transform: warp(i), filter: drift(i) }" draggable="false"></div>
    </div>
    <p class="status">{{ status }}</p>
  </div>
</template>

<style scoped>
.dd { display: flex; flex-direction: column; gap: .45rem; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: .9rem; }
.cap { font-size: .78rem; font-weight: 700; margin-bottom: .25rem; }
.cap.ok { color: var(--lx-good); } .cap.bad { color: var(--lx-bad); }
.frame { aspect-ratio: 832 / 428; overflow: hidden; border-radius: 10px; border: 1px solid var(--lx-line); }
.frame img, .th img { width: 100%; height: 100%; object-fit: cover; transition: transform .35s, filter .35s; transform-origin: 30% 50%; }
.ctrl { display: flex; align-items: center; gap: .6rem; }
.ctrl input { flex: 1; accent-color: var(--lx-accent); }
.ctrl button { font-size: .75rem; padding: .2rem .7rem; border-radius: 6px; background: var(--lx-panel2); border: 1px solid var(--lx-line); }
.lab { font-weight: 700; font-size: .8rem; min-width: 3.5rem; }
.strip { display: flex; gap: .3rem; height: 38px; }
.th { width: 62px; height: 36px; overflow: hidden; border-radius: 4px; border: 1px solid var(--lx-line); }
.status { font-size: .82rem; margin: 0; color: #e5e7eb; }
</style>
