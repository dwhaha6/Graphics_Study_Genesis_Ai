<script setup lang="ts">
import { computed, ref } from 'vue'

const n = ref(1) // number of generated segments
const MAX = 6
const CTX = 2 // segments the model can look at (illustrative)
const boxes = computed(() => Array.from({ length: n.value + 1 }, (_, i) => i))
function next() { n.value = n.value >= MAX ? 1 : n.value + 1 }
</script>

<template>
  <div class="chain">
    <div class="row">
      <template v-for="i in boxes" :key="i">
        <div
          class="box"
          :class="{
            photo: i === 0,
            ctx: i >= n - CTX && i < n,
            cur: i === n,
            old: i < n - CTX,
          }"
        >
          <div class="t">{{ i === 0 ? '입력 사진' : `구간 ${i}` }}</div>
          <div class="frames">
            <span v-for="k in (i === 0 ? 1 : 4)" :key="k" />
          </div>
        </div>
        <div v-if="i < n" class="arr">→</div>
      </template>
    </div>
    <div class="legend">
      <span><i class="sw cur" />지금 만드는 구간</span>
      <span><i class="sw ctx" />모델이 참고하는 범위 (context window)</span>
      <span><i class="sw old" />범위 밖으로 밀려난 구간 (참고 못 함)</span>
    </div>
    <button class="go" @click="next">{{ n >= MAX ? '처음부터' : '다음 구간 만들기 ▶' }}</button>
  </div>
</template>

<style scoped>
.chain { display: flex; flex-direction: column; gap: .6rem; }
.row { display: flex; align-items: center; gap: .35rem; min-height: 86px; flex-wrap: nowrap; }
.box { border: 2px solid var(--lx-line); border-radius: 10px; padding: .35rem .45rem; background: var(--lx-panel); transition: all .3s; }
.box .t { font-size: .7rem; color: var(--lx-muted); margin-bottom: .25rem; white-space: nowrap; }
.frames { display: flex; gap: 3px; }
.frames span { width: 18px; height: 30px; border-radius: 3px; background: #3b4656; }
.box.ctx { border-color: var(--lx-accent); } .box.ctx .frames span { background: #2f6f68; }
.box.photo { border-color: #fbbf24; } .box.photo .frames span { background: #fbbf24; width: 30px; }
.box.cur { border-color: #fff; box-shadow: 0 0 0 3px #ffffff22; } .box.cur .frames span { background: #e6edf3; }
.box.old { opacity: .45; }
.arr { color: var(--lx-muted); font-size: 1rem; }
.legend { display: flex; gap: 1.2rem; font-size: .72rem; color: var(--lx-muted); }
.sw { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: .35rem; border: 2px solid; }
.sw.cur { border-color: #fff; } .sw.ctx { border-color: var(--lx-accent); } .sw.old { border-color: var(--lx-line); opacity: .6; }
.go { align-self: flex-start; font-size: .8rem; padding: .3rem .9rem; border-radius: 8px; background: var(--lx-accent); color: #0d1117; font-weight: 700; }
</style>
