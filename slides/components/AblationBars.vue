<script setup lang="ts">
import { ref } from 'vue'

// Paper Table 3 (Ablation, Tanks and Temples): 3 of 7 metrics. All three are 0-100 scores, higher = better.
const series = [
  { k: 'ours', n: 'Lyra 2.0', c: 'var(--lx-accent)' },
  { k: 'fp', n: 'FramePack 없이', c: '#8b949e' },
  { k: 'sa', n: 'Self-Aug 없이', c: '#e07a7a' },
] as const
const metrics = [
  { n: 'Style Consistency', d: '첫 프레임과 마지막 프레임의 스타일 유사성 (드리프트)', v: { ours: 85.07, fp: 80.61, sa: 77.98 } },
  { n: 'Camera Controllability', d: '지정한 카메라 경로의 추종 정확도', v: { ours: 63.87, fp: 62.62, sa: 53.92 } },
  { n: 'Subjective Quality', d: '개별 프레임의 시각적 품질', v: { ours: 43.35, fp: 45.27, sa: 47.88 } },
]
const hov = ref<string | null>(null)
</script>

<template>
  <div class="ab">
    <div class="lg">
      <span v-for="s in series" :key="s.k" :class="{ dim: hov && hov !== s.k }" @mouseenter="hov = s.k" @mouseleave="hov = null"><i :style="{ background: s.c }" />{{ s.n }}</span>
    </div>
    <div v-for="m in metrics" :key="m.n" class="mt">
      <div class="mn"><b>{{ m.n }}</b> ↑ <span>{{ m.d }}</span></div>
      <div v-for="s in series" :key="s.k" class="row" :class="{ dim: hov && hov !== s.k }" @mouseenter="hov = s.k" @mouseleave="hov = null">
        <div class="track"><div class="bar" :style="{ width: `${m.v[s.k]}%`, background: s.c }" /></div>
        <span class="val" :class="{ ours: s.k === 'ours' }">{{ m.v[s.k].toFixed(2) }}</span>
      </div>
    </div>
    <div class="eff">
      <span class="et">Self-Augmentation의 효과</span>
      <span><b>+7.09</b> 스타일 일관성</span>
      <span><b>+9.95</b> 카메라 제어</span>
    </div>
  </div>
</template>

<style scoped>
.ab { font-size: .7rem; }
.lg { display: flex; gap: .8rem; margin-bottom: .35rem; }
.lg span { display: inline-flex; align-items: center; gap: .3rem; cursor: default; }
.lg i { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
.mt { margin-bottom: .35rem; }
.mn { margin-bottom: .12rem; }
.mn b { font-size: .76rem; }
.mn span { color: var(--lx-muted); margin-left: .3rem; font-size: .64rem; }
.row { display: grid; grid-template-columns: 1fr 2.6rem; align-items: center; gap: .4rem; height: 12px; margin-bottom: 3px; }
.track { height: 9px; background: #232a35; border-radius: 5px; overflow: hidden; }
.bar { height: 100%; border-radius: 5px; }
.val { font-variant-numeric: tabular-nums; text-align: right; font-size: .66rem; }
.val.ours { color: var(--lx-accent); font-weight: 700; }
.dim { opacity: .35; }
.eff { display: flex; align-items: baseline; gap: 1rem; border-top: 1px solid var(--lx-line); padding-top: .35rem; margin-top: .1rem; }
.et { color: var(--lx-accent); font-size: .68rem; }
.eff b { font-size: 1rem; }
</style>
