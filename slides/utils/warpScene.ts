// Tiny procedural street scene with known per-pixel depth, shared by CoordWarp and AttnDemo.
// Forward warp = sideways camera move: each source pixel shifts by F * t / depth (z-buffered).
export const W = 120
export const H = 72
export const F = 24
export type Px = { r: number, g: number, b: number, z: number }

export const src: Px[] = (() => {
  const out: Px[] = []
  for (let v = 0; v < H; v++) {
    for (let u = 0; u < W; u++) {
      let p: Px = { r: 150 + v * 1.6, g: 200 + v * 0.7, b: 255, z: 60 } // sky
      const far = [[0, 22, 30], [20, 40, 22], [44, 70, 27], [66, 96, 20], [92, 120, 26]]
      for (const [a, b, top] of far) if (u >= a && u < b && v >= top && v < 58) p = { r: 120, g: 132, b: 150, z: 30 }
      if (u >= 14 && u < 64 && v >= 18 && v < 58) { // house
        const win = (u - 14) % 10 >= 3 && (u - 14) % 10 < 7 && (v - 18) % 12 >= 4 && (v - 18) % 12 < 9
        const door = u >= 34 && u < 42 && v >= 44
        p = door ? { r: 90, g: 55, b: 35, z: 10 } : win ? { r: 255, g: 226, b: 150, z: 10 } : { r: 176, g: 98, b: 62, z: 10 }
        if (v < 21) p = { r: 120, g: 60, b: 50, z: 10 }
      }
      if (v >= 58) { // ground plane
        const z = 120 / (v - 40); const X = (u - 60) * z / F
        const stripe = v >= 63 && v < 68 && Math.floor(X * 1.2) % 2 === 0
        p = stripe ? { r: 225, g: 225, b: 225, z } : { r: 95, g: 98, b: 104, z }
      }
      if (u >= 88 && u < 108 && v >= 50 && v < 62) p = { r: 59, g: 130, b: 246, z: 4 } // bench
      if (u >= 77 && u < 80 && v >= 9 && v < 64) p = { r: 40, g: 46, b: 56, z: 3 } // lamp post
      if (u >= 72 && u < 85 && v >= 6 && v < 10) p = { r: 250, g: 204, b: 21, z: 3 } // lamp head
      out.push(p)
    }
  }
  return out
})()

/** per target pixel: index of the source pixel that lands there, or -1 (no correspondence) */
export function warp(t: number): Int32Array {
  const idx = new Int32Array(W * H).fill(-1); const zb = new Float32Array(W * H).fill(1e9)
  for (let v = 0; v < H; v++) {
    for (let u = 0; u < W; u++) {
      const i = v * W + u; const p = src[i]
      const u2 = Math.round(u - F * t / p.z)
      if (u2 < 0 || u2 >= W) continue
      const j = v * W + u2
      if (p.z < zb[j]) { zb[j] = p.z; idx[j] = i }
    }
  }
  return idx
}

/** address color code: u -> red, v -> green (faint grid every 12 px so shifts are visible) */
export function addr(u: number, v: number) {
  const k = (u % 12 === 0 || v % 12 === 0) ? 0.55 : 1
  return { r: Math.round((40 + u / W * 215) * k), g: Math.round((40 + v / H * 215) * k), b: Math.round(140 * k) }
}
