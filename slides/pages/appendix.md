---
layout: default
---

<div class="kicker">부록 · 추론 가속</div>

# DMD 증류: 35 step → 4 step

<p class="lead">Anti-Drifting과는 별개인 <span class="em">추론 가속</span> 기법 · Self-Augmentation은 증류 중에도 유지</p>

<div class="grid gap-6 mt-4" style="grid-template-columns: 1fr 1fr; align-items: start">
  <div class="panel" style="font-size: .76rem">
    <div class="em" style="margin-bottom: .5rem">80프레임 1회 생성 시간 <span class="muted">(GB200 1장, 깊이 추정 · 검색 포함)</span></div>
    <div class="tb"><span>기본 · 35 step + CFG</span><div class="tr"><div class="bb" style="width: 100%; background: #8b949e" /></div><b>약 194초</b></div>
    <div class="tb"><span>DMD · 4 step, CFG 증류</span><div class="tr"><div class="bb" style="width: 7.7%; background: var(--lx-accent)" /></div><b class="em">약 15초</b></div>
    <div class="muted" style="margin-top: .5rem; font-size: .68rem">CFG: 조건 있는 예측 / 없는 예측을 두 번 계산 → 증류로 한 번에</div>
  </div>
  <div style="font-size: .74rem">
    <table class="dm">
      <thead><tr><th></th><th></th><th>Subjective<br>Quality ↑</th><th>Style<br>Consistency ↑</th><th>Camera<br>Ctrl. ↑</th></tr></thead>
      <tbody>
        <tr><td class="ds">DL3DV</td><td class="nm">Lyra 2.0</td><td>44.54</td><td>87.46</td><td>64.67</td></tr>
        <tr class="d"><td class="ds"></td><td class="nm">DMD</td><td>45.21</td><td>88.57</td><td>65.64</td></tr>
        <tr><td class="ds">Tanks and Temples</td><td class="nm">Lyra 2.0</td><td>43.35</td><td>85.07</td><td>63.87</td></tr>
        <tr class="d"><td class="ds"></td><td class="nm">DMD</td><td>43.02</td><td class="bad">78.91</td><td class="bad">58.12</td></tr>
      </tbody>
    </table>
    <p class="muted" style="margin-top: .5rem; font-size: .68rem">논문 요약: 프레임 화질은 비슷하거나 조금 좋음 · 카메라 제어는 step 수가 줄어 다소 하락 (Tanks and Temples에서 두드러짐)</p>
  </div>
</div>

<div class="src">출처: 논문 §4.5 (Distillation), §5.2, 부록 A.3, Table 1</div>

<style>
.tb { display: grid; grid-template-columns: 9.5rem 1fr 4.2rem; align-items: center; gap: .5rem; margin-bottom: .45rem; }
.tr { height: 12px; background: #232a35; border-radius: 6px; overflow: hidden; }
.bb { height: 100%; border-radius: 6px; }
.tb b { text-align: right; }
table.dm { width: 100%; border-collapse: collapse; }
table.dm th { font-size: .64rem; color: var(--lx-muted); font-weight: 400; text-align: right; padding: .2rem .35rem; line-height: 1.25; }
table.dm td { padding: .3rem .35rem; text-align: right; border-top: 1px solid var(--lx-line); }
table.dm td.ds { text-align: left; color: var(--lx-muted); font-size: .66rem; white-space: nowrap; }
table.dm td.nm { text-align: left; }
table.dm tr.d td.ds { border-top: none; }
table.dm tr.d td { color: var(--lx-accent); }
table.dm tr.d td.bad { color: var(--lx-bad); }
</style>

<!--
(부록, 질문 나오면)
빠른 버전입니다. 원래 모델은 노이즈 제거를 35 step 하고 CFG 때문에 매 step 두 번씩 계산해서, 80프레임 한 번 만드는 데 약 194초가 걸립니다. DMD로 증류해서 4 step, CFG도 한 번으로 합쳐 약 15초로 줄였습니다. 약 13배 빠릅니다.
품질은 DL3DV에서는 오히려 조금 좋고, Tanks and Temples에서는 카메라 제어와 스타일 일관성이 떨어집니다.

(참고) DMD: Distribution Matching Distillation. 35 → 4 denoising step, CFG도 증류. 194초는 깊이 추정 · 검색 · 생성 포함, GB200 GPU 1장 (§4.5, 부록 A.3).
(참고) Self-Augmentation은 증류 단계에서도 그대로 적용 (§4.5).
[Q&A 대비] 왜 본문에서 뺐나? DMD는 드리프트 해결이 아니라 추론 속도를 위한 별도 기술이라서.

[용어]
- distillation (증류): 큰 모델(선생)의 결과를 빠른 모델(학생)이 따라 하도록 학습
- DMD (Distribution Matching Distillation): 선생 모델의 출력 분포를 맞추는 방식의 증류. 적은 step으로 비슷한 결과
- CFG (classifier-free guidance): 조건 있는 예측과 없는 예측을 둘 다 계산해서 차이를 키우는 기법. 품질은 오르지만 계산 2배
-->
