<script setup lang="ts">
// Plays when its slide is shown, pauses + rewinds when leaving (SlidevVideo), with base-path-safe URLs.
// start/end (seconds) play and loop only that part of the file, so one long official video can serve as a short preview.
const props = withDefaults(defineProps<{
  src: string
  poster?: string
  controls?: boolean
  loop?: boolean
  rate?: number
  start?: number
  end?: number
}>(), { controls: false, loop: true, rate: 1, start: 0 })

const base = import.meta.env.BASE_URL
const url = (p: string) => (/^https?:\/\//.test(p) ? p : base + p)

function onMeta(e: Event) {
  (e.target as HTMLVideoElement).playbackRate = props.rate
}
function onTime(e: Event) {
  if (props.end == null)
    return
  const v = e.target as HTMLVideoElement
  if (v.currentTime >= props.end) {
    if (props.loop)
      v.currentTime = props.start
    else
      v.pause()
  }
}
</script>

<template>
  <SlidevVideo
    autoplay
    autoreset="slide"
    :timestamp="start"
    :controls="controls"
    :poster="poster ? url(poster) : undefined"
    :loop="loop && end == null"
    muted
    playsinline
    preload="auto"
    @loadedmetadata="onMeta"
    @timeupdate="onTime"
  >
    <source :src="url(src)" type="video/mp4">
  </SlidevVideo>
</template>
