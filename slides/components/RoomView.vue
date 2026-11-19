<script setup lang="ts">
// Simple illustrated camera views for the spatial-forgetting demo.
defineProps<{ kind: 'living' | 'living-forgot' | 'hall' | 'bed', marks?: boolean }>()
</script>

<template>
  <svg viewBox="0 0 300 190" class="rv">
    <!-- living room (as first seen) -->
    <g v-if="kind === 'living'">
      <rect width="300" height="130" fill="#e8dcc4" />
      <polygon points="0,130 300,130 300,190 0,190" fill="#9c7650" />
      <rect x="20" y="22" width="70" height="58" fill="#bfe3f5" stroke="#fff" stroke-width="4" />
      <line x1="55" y1="22" x2="55" y2="80" stroke="#fff" stroke-width="3" />
      <rect x="120" y="24" width="62" height="42" fill="#9cc58a" stroke="#6b4f35" stroke-width="4" />
      <polygon points="124,62 145,38 160,52 170,44 178,62" fill="#4d7c4a" />
      <rect x="95" y="84" width="112" height="26" rx="6" fill="#2563eb" />
      <rect x="92" y="106" width="118" height="30" rx="6" fill="#3b82f6" />
      <rect x="86" y="96" width="14" height="40" rx="5" fill="#1d4ed8" />
      <rect x="202" y="96" width="14" height="40" rx="5" fill="#1d4ed8" />
      <line x1="240" y1="68" x2="240" y2="140" stroke="#444" stroke-width="3" />
      <polygon points="226,70 254,70 249,52 231,52" fill="#fde68a" />
      <rect x="262" y="146" width="24" height="24" rx="3" fill="#b45309" />
      <circle cx="274" cy="134" r="14" fill="#3f8f4f" />
      <circle cx="264" cy="124" r="9" fill="#4ca35d" />
      <circle cx="284" cy="122" r="9" fill="#4ca35d" />
    </g>

    <!-- living room re-imagined after being forgotten -->
    <g v-else-if="kind === 'living-forgot'">
      <rect width="300" height="130" fill="#cfd8e3" />
      <polygon points="0,130 300,130 300,190 0,190" fill="#7a6a5a" />
      <rect x="212" y="26" width="66" height="52" fill="#bfe3f5" stroke="#fff" stroke-width="4" />
      <circle cx="150" cy="46" r="20" fill="#fff" stroke="#333" stroke-width="3" />
      <line x1="150" y1="46" x2="150" y2="32" stroke="#333" stroke-width="3" />
      <line x1="150" y1="46" x2="160" y2="52" stroke="#333" stroke-width="3" />
      <rect x="18" y="90" width="100" height="24" rx="6" fill="#b91c1c" />
      <rect x="14" y="110" width="108" height="30" rx="6" fill="#dc2626" />
      <rect x="150" y="128" width="60" height="18" rx="3" fill="#6b4f35" />
      <g v-if="marks" fill="none" stroke="#f87171" stroke-width="2.5" stroke-dasharray="6 4">
        <ellipse cx="68" cy="113" rx="62" ry="34" />
        <ellipse cx="150" cy="46" rx="30" ry="28" />
        <ellipse cx="245" cy="52" rx="42" ry="36" />
      </g>
    </g>

    <!-- hallway -->
    <g v-else-if="kind === 'hall'">
      <polygon points="0,0 300,0 190,55 110,55" fill="#efe7da" />
      <polygon points="0,0 110,55 110,140 0,190" fill="#d6cbb8" />
      <polygon points="300,0 190,55 190,140 300,190" fill="#cbbfa9" />
      <rect x="110" y="55" width="80" height="85" fill="#e3d8c4" />
      <polygon points="0,190 110,140 190,140 300,190" fill="#8b6b4a" />
      <polygon points="28,48 72,64 72,150 28,170" fill="#7c5a3a" />
      <polygon points="270,48 228,64 228,150 270,170" fill="#7c5a3a" />
      <rect x="136" y="80" width="28" height="60" fill="#6b4f35" />
    </g>

    <!-- bedroom -->
    <g v-else>
      <rect width="300" height="130" fill="#dfe7d8" />
      <polygon points="0,130 300,130 300,190 0,190" fill="#8f7a64" />
      <rect x="22" y="24" width="52" height="46" fill="#bfe3f5" stroke="#fff" stroke-width="4" />
      <rect x="60" y="78" width="170" height="26" rx="4" fill="#6d4c41" />
      <rect x="60" y="100" width="170" height="48" rx="6" fill="#a78bfa" />
      <rect x="72" y="92" width="44" height="16" rx="6" fill="#fff" />
      <rect x="174" y="92" width="44" height="16" rx="6" fill="#fff" />
      <rect x="246" y="28" width="46" height="112" rx="3" fill="#8d6e63" />
      <line x1="269" y1="28" x2="269" y2="140" stroke="#5d4037" stroke-width="2" />
    </g>
  </svg>
</template>

<style scoped>
.rv { width: 100%; border-radius: 8px; display: block; }
</style>
