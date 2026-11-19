---
layout: default
---

<StepBar :steps="['원인 · 아이디어', '만드는 법', '효과']" :cur="0" />

<div class="kicker">PART 4 · ANTI-DRIFTING</div>

# 드리프트의 원인: 연습 때와 실전이 다르다

<p class="lead">원인은 <span class="em">observation bias</span>: 학습 때는 깨끗한 과거, 실제로 쓸 때는 자신이 생성한 불완전한 과거 → 해결: <span class="em">Self-Augmentation</span></p>

<SelfAugDemo src="lyra/fig/street_clean.jpg" />

<div v-click class="panel mt-4" style="font-size: .76rem; padding: .5rem .8rem"><span class="muted">함께 쓰는 기존 기법</span> <b>FramePack</b> · 오래된 과거는 압축해서 더 길게 보고, 첫 사진을 항상 기준점으로 함께 넣음 → 드리프트 <b>완화</b>. 하지만 <b class="em">학습-실전 차이 자체는 그대로</b> → 그래서 Self-Augmentation</div>

<div class="peq">

<span class="pl">논문 표기</span> "observation bias": 학습 때는 ground-truth history, 추론 때는 모델 자신의 imperfect outputs를 조건으로 받음 <span class="mu">(§4.3)</span> · FramePack: $\texttt{f1k1}$ (anchor = 첫 사진 $I_0$) + temporal slots $\texttt{f16k4 f2k2 f1k1}$ <span class="mu">(§3)</span>

</div>

<div class="src">출처: 논문 §4.3, §3 (FramePack) · 사진: 논문 Figure 1의 입력 사진</div>
<div class="concept">개념 시뮬레이션 · 실제 모델 결과 아님</div>

<!--
(약 1분 10초)
Part 4, 시간적 드리프트입니다. Part 1에서 길게 만들수록 색이 변하고 흐려지는 걸 봤는데, 왜 그럴까요?
(학습할 때) 영상 모델은 학습할 때 "과거 장면"으로 항상 깨끗한 정답 영상을 받습니다.
(실제로 쓸 때) 그런데 실제로 길게 만들 때는 과거 장면이 모델 자신이 방금 만든, 조금씩 틀린 결과입니다. 연습 때 본 적 없는 상황이라 오류를 고치지 못하고 다음 구간으로 넘기고, 이게 쌓이면서 드리프트가 됩니다. 이 학습과 실전의 차이를 observation bias라고 부릅니다.
(Self-Augmentation 학습) 그래서 Lyra 2.0은 학습할 때부터 과거 장면을 일부러 "조금 틀린 결과"로 바꿔서 줍니다. 대신 정답은 항상 깨끗한 다음 구간입니다. 그러면 모델이 틀린 과거를 받아도 바로잡아 이어 가는 법을 배웁니다.
(클릭) 참고로 FramePack이라는 기존 기법도 함께 씁니다. 오래된 과거는 압축해서 더 길게 보고, 첫 사진을 항상 기준점으로 넣어서 드리프트를 줄입니다. 다만 학습과 실전의 차이 자체는 못 없애기 때문에 Self-Augmentation이 핵심입니다.

(참고) 논문 표현: 구간마다 생기는 오류 = 색 변화(color shift), 흐려짐(blurring), 형태 왜곡(distortion). 고쳐지지 않고 autoregressive step마다 누적. observation bias라는 용어는 FramePack 논문(Zhang & Agrawala 2025)에서 인용. (§4.3)
(참고) FramePack 구성: f1k1 (첫 사진, 항상 원본) + [f4k2 f1k1] (Part 3에서 찾아온 5장) + [f16k4 f2k2 f1k1] (직전 영상 19 latent ≈ 76프레임, 오래될수록 크게 압축) + g20 (새로 만들 20 latent = 80프레임). fNkM = latent N개를 공간 배율 M으로 압축. (§3, §4.2)
(참고) FramePack 효과(논문 실험): 직전 영상 칸(temporal slots)을 빼면 스타일 일관성 85.07 → 80.61, 재투영 오차 0.069 → 0.079 (Tanks and Temples).

[용어]
- ground truth (GT, 정답): 실제로 촬영된 영상. 학습 때 정답으로 씀
- 학습 (training) / 추론 (inference): 모델을 가르치는 단계 / 다 배운 모델로 실제 영상을 만드는 단계
- observation bias: 학습 때는 정답 과거, 추론 때는 자신이 생성한 불완전한 과거를 받는 차이
- FramePack · anchor: 오래된 프레임일수록 더 줄여 넣는 기존 기법 · 항상 넣는 첫 사진
-->

---

<StepBar :steps="['원인 · 아이디어', '만드는 법', '효과']" :cur="1" />

<div class="kicker">PART 4 · ANTI-DRIFTING</div>

# Self-Augmentation: '조금 틀린 과거'를 싸게 만드는 법

<p class="lead">학습 중 과거 장면을 일부러 흐트러뜨린 뒤 <span class="em">One-Step Denoising (DiT Forward Pass 1회)</span> 결과로 바꿔서 줌 · 목표는 그대로 정답</p>

<SelfAugMech src="lyra/fig/street_clean.jpg" />

<div class="grid grid-cols-2 gap-3 mt-3" style="font-size: .78rem; line-height: 1.5">
  <div v-click class="panel" style="padding: .55rem .8rem"><b>무엇을 배우나</b> · 틀린 과거를 받아도 <b>깨끗한 정답</b>을 내도록 학습 → 실제로 쓸 때 다음 구간으로 오류가 누적되는 현상을 완화</div>
  <div v-click class="panel" style="padding: .55rem .8rem"><b>왜 싼가</b> · 실전처럼 35단계를 전부 돌려 과거를 만들지 않고 <b>모델을 한 번만 더</b> 돌림 · 추론 때 추가 비용 없음</div>
</div>

<div class="peq">

<span class="pl">논문 표기</span> ① 정답 과거 $\mathbf{z}_0^{\text{hist}}$를 확률 $p_{\text{aug}}{=}0.7$로 아래처럼 교체 · ④ 목표 $\mathbf{z}_0^{\text{cur}}=\mathcal{E}(\mathbf{x}^{\text{cur}}\mid\mathbf{x}^{\text{hist}})$는 항상 깨끗한 쪽 <span class="mu">(§4.3)</span>

$$
\underbrace{\mathbf{z}_t^{\text{hist}}=(1-t)\,\mathbf{z}_0^{\text{hist}}+t\,\boldsymbol{\epsilon}}_{\text{② 노이즈 섞기},\ t\,\sim\,\mathcal{U}(0,\,0.5)}
\quad\Longrightarrow\quad
\underbrace{\tilde{\mathbf{z}}_0^{\text{hist}}=\mathbf{z}_t^{\text{hist}}-t\cdot v_\theta(\mathbf{z}_t^{\text{hist}},t,\mathbf{c})}_{\text{③ One-Step Denoising → 조금 틀린 과거 (조건으로 사용)}}
\quad {\small \Big(=\ \mathbf{z}_0^{\text{hist}}-t\cdot\underbrace{\mathbf{e}_v}_{\text{Velocity 예측 오차}}\Big)}
$$

</div>

<div class="src">출처: 논문 §4.3 (Self-Augmentation Training), 부록 A.2</div>
<div class="concept">개념 시뮬레이션 · 실제로는 이미지가 아니라 latent에서 일어남</div>

<!--
(약 1분 20초)
그럼 "모델 자신이 만든 조금 틀린 과거"를 학습 중에 어떻게 만들까요? 실제처럼 영상을 끝까지 생성하면 너무 비쌉니다. 그래서 아주 싼 방법을 씁니다.
(왼쪽부터) 학습 데이터의 정답 과거 장면에 노이즈를 섞고, 모델이 그걸 한 번에 복원하게 합니다. 한 번에 복원하면 완벽하지 않아서 조금 흐리고 색이 틀어진, 모델 자신의 오류가 섞인 과거가 나옵니다. 이걸 원래 과거 대신 조건으로 넣습니다.
(오른쪽) 그런데 학습 목표, 즉 정답 다음 구간은 항상 깨끗한 정답 그대로입니다. 그래서 모델은 "과거가 조금 틀려도 깨끗하게 이어 가는 법"을 배웁니다.
(슬라이더) 노이즈를 많이 섞을수록 복원 결과가 더 많이 틀립니다. (뽑기 버튼) 학습 샘플마다 70% 확률로 이렇게 바꾸고, 노이즈 양도 매번 무작위입니다.
(클릭) 결과적으로 실제로 쓸 때 다음 구간으로 오류가 누적되는 현상이 완화됩니다. (클릭) 비용도 작습니다. 실전처럼 35단계를 다 돌려서 과거를 만드는 대신 모델을 한 번만 더 돌리면 되고, 추론 때는 아무것도 추가되지 않습니다.

(참고) 노이즈 섞는 식은 영상 모델의 학습 방식(flow matching)과 같은 식: 정답 z_0와 노이즈 ε를 t 비율로 직선 보간, 모델은 그 방향(속도 v)을 예측하도록 학습됨. 그래서 v를 한 번 빼면 바로 정답 추정치가 나옴.
(참고) 수식: z_t = (1 − t)·z_0 + t·ε, t ~ U(0, 0.5) · 한 번에 복원: z̃_0 = z_t − t·v_θ(z_t, t, c) → z̃_0를 과거(history) 조건으로 사용. 확률 p_aug = 0.7. (§4.3, 부록 A.2)
(참고) 오른쪽 작은 식 z̃_0 = z_0 − t·e_v는 논문에 없는 유도식: 모델 예측을 v_θ = (ε − z_0) + e_v로 두고 위 두 식에 넣으면 나옴. e_v = velocity 예측 오차 → 섞는 노이즈 t가 클수록, 예측 오차가 클수록 z̃_0가 정답에서 멀어짐
(참고) t = 0이면 z̃_0 = z_0, 즉 정답과 똑같음 → 데모에서도 슬라이더 0이면 변화 없음.
(참고) 목표 latent는 "깨끗한 과거"로 만든 VAE cache로 인코딩. VAE가 causal이라 현재 구간 인코딩이 과거에 의존하기 때문. 목표가 오염되지 않게 하는 장치 (§4.3).
(참고) 비교 대상 Self-Forcing: 학습 때 모델 자신의 예측을 조건으로 쓰는 기존 방법. causal 구조용이라, 양방향(bi-directional) 영상 모델인 Wan에 그대로 쓰면 과거 구간마다 전체 attention + 35단계 denoising이 필요해 너무 비쌈 (§4.3).
(참고) 빠른 버전(DMD) 증류할 때도 Self-Augmentation은 그대로 유지 (§4.5).
[Q&A 대비] 왜 노이즈만 섞지 않고 한 번 복원까지 하나? 논문은 "approximate reconstruction"을 조건으로 쓴다고만 설명. 해석: 단순 노이즈가 아니라 모델 자신이 만드는 종류의 오류(흐림, 색 틀어짐)를 싸게 흉내 내기 위함.
[Q&A 대비] t 상한이 0.5인 이유? 논문에 설명 없음.

[용어]
- data augmentation: 학습 데이터를 일부러 변형해서 모델을 더 튼튼하게 만드는 기법. self-augmentation = 모델 자신의 출력으로 변형
- U(0, 0.5): 0~0.5 사이에서 무작위로 고르는 균등 분포
- forward pass: 모델에 입력을 한 번 넣어 출력을 얻는 계산 1회
- 한 번에 복원 (one-step denoise): z̃₀ = z_t − t·v. 예측한 속도로 한 번에 정답 쪽으로 점프. 35단계를 다 돌리지 않아 싸지만 조금 틀림
- Self-Forcing: 학습 중에 모델이 실제로 과거를 다 생성해서 그걸 조건으로 쓰는 기존 기법. 과거 토큰만 보는 causal 모델용이라, 앞뒤를 다 보는 bidirectional 모델(Wan)에는 너무 비쌈
- causal / bidirectional: 앞 토큰만 볼 수 있는 구조 / 앞뒤 토큰을 모두 볼 수 있는 구조
-->

---

<StepBar :steps="['원인 · 아이디어', '만드는 법', '효과']" :cur="2" />

<div class="kicker">PART 4 · ANTI-DRIFTING</div>

# Self-Augmentation은 장기적 일관성과 카메라 제어를 개선한다

<p class="lead">Self-Aug를 빼면 한 장의 화질(Subjective Quality)은 오히려 높지만, 길게 보면 <span class="em">일관성과 카메라 제어</span>가 떨어짐</p>

<div class="grid gap-6 mt-3" style="grid-template-columns: 1fr 1fr; align-items: start">
  <div>
    <div class="hg">
      <figure><LImg src="lyra/fig/abl_horse_ours.jpg" /><figcaption class="em">Lyra 2.0</figcaption></figure>
      <figure><LImg src="lyra/fig/abl_horse_gt.jpg" /><figcaption>정답 (GT)</figcaption></figure>
      <figure><LImg src="lyra/fig/abl_horse_fp.jpg" /><figcaption>FramePack 없이</figcaption></figure>
      <figure><LImg src="lyra/fig/abl_horse_sa.jpg" /><figcaption>Self-Aug 없이</figcaption></figure>
    </div>
    <div class="muted" style="font-size: .64rem; margin-top: .3rem">같은 입력 이미지에서 시작한 생성 결과 · 정답 = 실제 촬영 장면 (Figure 6 일부)</div>
  </div>
  <AblationBars />
</div>

<div class="muted" style="font-size: .64rem; margin-top: .6rem">논문 Table 3에는 SSIM · LPIPS · FID · Reprojection Error도 있음 (여기서는 3개 지표만 발췌) · FramePack 없이 = temporal slots를 뺀 버전 · 실험명: w/o FramePack, w/o Self-Augmentation</div>

<div class="src">출처: 논문 §5.4 (Ablation Study), Table 3, Figure 6 · Tanks and Temples</div>

<style>
.hg { display: grid; grid-template-columns: 1fr 1fr; gap: .45rem .5rem; }
.hg figure { margin: 0; }
.hg img { width: 100%; aspect-ratio: 212 / 123; object-fit: cover; border-radius: 6px; display: block; }
.hg figcaption { font-size: .7rem; font-weight: 700; margin-top: .15rem; }
</style>

<!--
(약 50초)
실제 효과입니다. 왼쪽은 논문 Figure 6의 일부로, 같은 입력 이미지에서 시작한 생성 결과입니다. 오른쪽 위가 실제로 촬영된 정답입니다.
FramePack이나 Self-Augmentation을 빼면 색감이나 물체가 정답과 달라지고, Lyra 2.0이 정답에 가장 가깝습니다.
(그래프) 숫자로 보면 Style Consistency와 Camera Controllability는 Lyra 2.0이 가장 높습니다. Self-Aug를 빼면 각각 7.09, 9.95 떨어집니다.
반면 Subjective Quality, 즉 한 장 단위 화질은 Self-Aug 없이가 오히려 가장 높습니다. 한 장이 보기 좋은 것과 길게 일관된 것은 다른 문제라는 걸 보여 줍니다.
(주의) Table 3의 다른 지표까지 보면 모든 지표에서 이긴 건 아님: Reprojection Error는 Self-Aug 없이가 0.066으로 가장 낮고, LPIPS는 FramePack 없이가 가장 좋음. "모든 지표에서 우수"라고 말하지 말 것.

(참고) 지표: 스타일 일관성 (Style Consistency, WorldScore) = 첫 프레임과 마지막 프레임 사이의 시각적 드리프트 측정. 카메라 제어 (Camera Controllability) = 카메라 포즈 정확도. 한 장면 화질 (Subjective Quality) = 사람 지각 기준 프레임 품질. (§5)
(참고) 표 전체 (Tanks and Temples, Ours / w/o FramePack / w/o Self-Aug): SSIM 0.384 / 0.362 / 0.363 · LPIPS 0.552 / 0.549 / 0.568 · FID 51.33 / 50.98 / 55.15 · 재투영 오차 0.069 / 0.079 / 0.066.
(참고) 논문 해석: Self-Aug 없이 학습하면 불완전한 조건을 본 적이 없어서 추론 때 자기 출력에 취약 → 구간마다 오류 누적 (Ablation).
(참고) 그림은 논문 Figure 6 (qualitative ablation)에서 말 동상 행의 4개 열만 잘라 씀 (Global Point Cloud, Explicit Corr. Fusion, Input 열 제외). 몇 번째 프레임인지는 그림 설명에 없음.

[용어]
- ablation (절제 실험): 구성 요소를 하나씩 빼서 그게 얼마나 중요한지 확인하는 실험
- WorldScore: 장면 생성 모델 평가용 공개 지표 모음. 아래 세 점수가 여기서 나옴
- Style Consistency: 첫 프레임과 마지막 프레임 사이 색감·스타일이 얼마나 유지되는지 (드리프트 측정)
- Camera Controllability: 생성 영상의 카메라 움직임이 지정한 경로와 얼마나 맞는지
- Subjective Quality: 사람이 보기에 얼마나 그럴듯한지를 예측한 점수
- Reprojection error: 생성 영상의 3D 일관성. 낮을수록 좋음 (SLAM 도구 ViPE로 깊이를 추정해 계산)
- Tanks and Temples: 실제 장면을 촬영한 3D 복원 벤치마크 데이터셋. 학습에 안 쓴 데이터라 일반화 평가용
-->
