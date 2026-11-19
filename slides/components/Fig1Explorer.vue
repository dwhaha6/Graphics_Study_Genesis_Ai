<script setup lang="ts">
import { computed, ref } from 'vue'

const base = import.meta.env.BASE_URL
type Key = 'top' | 'mid' | 'bot'
const regions: Record<Key, {
  top: number, h: number, title: string, ko: string, items: string[]
  videos: { name: string, src: string }[], vnote: string
}> = {
  top: {
    top: 0,
    h: 48.5,
    title: 'Single-Image to Expansive 3D Worlds',
    ko: '사진 1장에서 넓은 3D 세계로',
    items: [
      '왼쪽: 입력 사진(Input image)에서 출발해 생성한 영상 프레임 (화살표 방향으로 진행)',
      '실내: 서재에서 출발 → <b>Look back</b>에서 처음 서재를 다시 돌아봐도 같은 모습 → 계단·복도로 이동',
      '거리: 골목을 따라 <b>약 90 m</b> 이동 (그림 속 한 사례이지 최대 거리는 아님)',
      '오른쪽: 생성 영상으로 만든 point cloud(색 화살표 = 카메라 경로)와 3DGS 렌더링',
    ],
    videos: [{ name: '실내 (서재·계단)', src: 'lyra/videos/explore_indoor.mp4' }, { name: '거리 (골목)', src: 'lyra/videos/explore_street.mp4' }],
    vnote: '그림과 같은 장면 · 대각선 왼쪽 위 = 3DGS 렌더링, 오른쪽 아래 = 생성 영상',
  },
  mid: {
    top: 48.5,
    h: 34.5,
    title: 'Generalization Across Diverse Domains',
    ko: '다양한 장면에서도 동작',
    items: [
      '맨 왼쪽: 입력 사진 / 나머지: 3D로 복원한 결과(3DGS)를 여러 시점에서 렌더링',
      '중세 유럽 마을, 구름 위 동양 건축, 거대한 로봇 조각상이 있는 건물',
      '실제로 없는 <b>상상 속 장면</b>도 3D로 만들 수 있음',
    ],
    videos: [{ name: '동양 사원', src: 'lyra/videos/explore_temple.mp4' }, { name: '사막의 로봇', src: 'lyra/videos/explore_robot.mp4' }],
    vnote: '공식 페이지의 다른 예시 (그림 속 장면과는 다름)',
  },
  bot: {
    top: 83,
    h: 17,
    title: 'Simulation-Ready 3D Assets for Embodied AI',
    ko: '로봇 시뮬레이션에 바로 쓰는 3D',
    items: [
      '실제 <b>Street View 거리 사진</b>에서 출발 → 집 현관까지 생성',
      '이미지 편집 모델로 <b>문이 열린 사진</b>을 만들어 실내까지 이어서 생성',
      '3DGS·메쉬로 내보내 로봇 시뮬레이터(NVIDIA Isaac Sim)에서 사용',
    ],
    videos: [{ name: '거리 → 시뮬레이션', src: 'lyra/videos/street_to_sim.mp4' }],
    vnote: '그림과 같은 사례 · 공식 페이지 영상',
  },
}
const sel = ref<Key>('top')
const vi = ref(0)
const r = computed(() => regions[sel.value])
function pick(k: Key) { sel.value = k; vi.value = 0 }
</script>

<template>
  <div class="fx">
    <div class="figwrap">
      <img :src="base + 'lyra/fig/figure1.jpg'" alt="논문 Figure 1" draggable="false">
      <button
        v-for="(v, k) in regions" :key="k"
        class="hot" :class="{ on: sel === k }"
        :style="{ top: v.top + '%', height: v.h + '%' }"
        @click="pick(k as Key)"
      />
    </div>
    <div class="info">
      <div class="t">{{ r.ko }}</div>
      <div class="en">{{ r.title }}</div>
      <ul><li v-for="(it, i) in r.items" :key="i" v-html="it" /></ul>
      <div v-if="r.videos.length > 1" class="vt">
        <button v-for="(v, i) in r.videos" :key="v.src" :class="{ on: vi === i }" @click="vi = i">{{ v.name }}</button>
      </div>
      <LVideo :key="r.videos[vi].src" :src="r.videos[vi].src" class="vid" />
      <div class="vn">{{ r.vnote }}</div>
    </div>
  </div>
</template>

<style scoped>
.fx { display: grid; grid-template-columns: 368px 1fr; gap: 1.2rem; align-items: start; }
.figwrap { position: relative; height: 420px; aspect-ratio: 2400 / 2736; overflow: hidden; border-radius: 6px; }
.figwrap img { width: 100%; height: 100%; border-radius: 6px; }
.hot { position: absolute; left: 0; width: 100%; border: 2px solid transparent; border-radius: 6px; background: transparent; transition: all .2s; }
.hot:hover { border-color: #5eead488; }
.hot.on { border-color: var(--lx-accent); box-shadow: 0 0 0 9999px #0d1117aa; }
.t { font-size: 1.15rem; font-weight: 700; }
.en { font-size: .72rem; color: var(--lx-accent); margin-bottom: .3rem; }
ul { margin: 0 0 .5rem; padding-left: 1.1rem; }
li { font-size: .78rem; line-height: 1.45; margin: .15rem 0; }
.vt { display: flex; gap: .4rem; margin-bottom: .3rem; }
.vt button { font-size: .7rem; padding: .15rem .6rem; border-radius: 6px; border: 1px solid var(--lx-line); background: var(--lx-panel); color: var(--lx-muted); }
.vt button.on { background: var(--lx-accent); color: #0d1117; font-weight: 700; }
.vid { width: 100%; max-height: 210px; border-radius: 8px; background: #000; }
.vn { font-size: .62rem; color: var(--lx-muted); margin-top: .2rem; }
</style>
