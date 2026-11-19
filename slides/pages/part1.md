---
layout: default
---

<div class="kicker">RESULT</div>

# 사진 한 장 → 걸어 다닐 수 있는 3D World

<div class="flex justify-center mt-2">
  <div style="width: 68%">
    <LVideo src="https://nv-tlabs.github.io/Project-Lyra/assets/teaser.mp4" poster="lyra/videos/teaser.jpg" :start="0" :end="14.3" class="w-full rounded-lg" style="background: #000; display: block" />
    <div class="muted" style="font-size: .72rem; margin-top: .4rem">대각선 왼쪽 위: 3D로 복원해서 렌더링한 화면 · 오른쪽 아래: 생성된 영상 → 둘이 거의 같음</div>
  </div>
</div>

<div class="src">영상: Lyra 2.0 공식 프로젝트 페이지 (teaser 앞부분 두 장면)</div>

<!--
(약 30초)
먼저 결과부터 보겠습니다. 둘 다 사진 한 장에서 출발해 만든 장면입니다. 앞은 실제 같은 거리, 뒤는 상상 속 사막 사원입니다.
대각선 한쪽은 생성된 영상, 다른 쪽은 그 영상으로 만든 3D를 렌더링한 화면인데, 둘이 거의 같다는 게 포인트입니다.
-->

---

<div class="kicker">TASK</div>

# 무엇을 하는 논문인가?

<p class="lead">입력은 <span class="y">사진 1장</span>과 <span class="y">카메라가 지나갈 길</span>, 출력은 그 안을 돌아다닐 수 있는 <span class="em">3D world</span></p>

<div class="steps">
  <LImg src="lyra/fig/indoor_input.jpg" class="st-img" style="border: 2px solid #fbbf24" />
  <div v-click="1" class="arr">→</div>
  <LImg v-click="1" src="lyra/fig/indoor_frames.jpg" class="st-img" />
  <div v-click="2" class="arr">→</div>
  <LImg v-click="2" src="lyra/fig/indoor_pc.jpg" class="st-img" style="background: #e9efe9" />
  <div v-click="3" class="sep"></div>
  <LImg v-click="3" src="lyra/fig/indoor_3dgs.jpg" class="st-img" />
  <div class="cap" style="grid-column: 1"><b>① 입력 사진 1장</b><span>+ 카메라 경로</span></div>
  <div v-click="1" class="cap" style="grid-column: 3"><b>② 경로를 따라 걷는 영상 생성</b><span>사진에 없던 부분은 모델이 새로 그림</span></div>
  <div v-click="2" class="cap" style="grid-column: 5"><b>③ Point cloud</b><span>중간 결과<br>화살표 = 카메라 경로</span></div>
  <div v-click="3" class="cap" style="grid-column: 7"><b>④ 3DGS · 메쉬</b><span>최종 결과<br>1·2·3 = 경로 위 위치</span></div>
</div>

<style>
.steps { display: grid; grid-template-columns: auto 24px auto 24px auto 17px minmax(122px, auto); justify-content: center; align-items: center; row-gap: .45rem; margin: .5rem -2rem 0; }
.steps .st-img { height: 142px; border-radius: 6px; justify-self: center; }
.steps .arr { color: var(--lx-muted); font-size: 1.25rem; text-align: center; }
.steps .sep { grid-column: 6; grid-row: 1 / span 2; align-self: stretch; justify-self: center; width: 1px; background: var(--lx-line); }
.steps .cap { grid-row: 2; align-self: start; display: flex; flex-direction: column; gap: .15rem; text-align: center; line-height: 1.35; }
.steps .cap b { font-size: .88rem; }
.steps .cap span { font-size: .74rem; color: var(--lx-muted); }
.gloss { margin-top: 1.5rem; display: grid; grid-template-columns: 1fr 1fr; gap: .45rem 1.6rem; }
.gloss .term::before { content: "•"; color: var(--lx-accent); font-weight: 700; margin-right: .45rem; }
</style>

<div class="panel gloss">
  <div class="term"><b>카메라 경로</b>: 가상의 카메라가 어디서 어디를 보며 움직일지 정한 길</div>
  <div class="term"><b>Point cloud</b>: 프레임마다 깊이를 추정해, 픽셀을 3D 공간에 색깔 점으로 찍은 것</div>
  <div class="term"><b>3DGS</b>: 흐릿한 색 덩어리를 아주 많이 모아 장면을 표현. 실시간 렌더링 가능</div>
  <div class="term"><b>메쉬 (Mesh)</b>: 삼각형 면으로 만든 표면. 게임 엔진·시뮬레이터용</div>
</div>

<div v-click="4" class="panel mt-3" style="font-size: .9rem">
  핵심 발상 <b class="em">Generative Reconstruction</b>: 여러 각도에서 직접 찍는 대신, <b>영상 생성 모델이 만든 영상을 촬영본처럼</b> 써서 3D를 만듦
</div>

<div class="src">출처: 논문 Abstract, §1, §4.1 · 그림: 논문 Figure 1 일부</div>

<!--
(약 1분 30초)
(용어 먼저) 아래 용어 네 개를 먼저 짚고 시작: 카메라 경로, point cloud, 3DGS, 메쉬.
한 줄로 말하면: 사진 한 장과 카메라 경로를 주면, 그 경로를 걷는 영상을 만들고, 그 영상으로 3D를 만든다.
(클릭) 사진에 없던 공간은 모델이 새로 그려 넣습니다.
(클릭) 영상의 프레임마다 깊이를 추정해서, 각 픽셀을 3D 공간에 색깔 점으로 찍으면 point cloud가 됩니다. 지금까지 만든 공간과 카메라가 지나간 길을 한눈에 볼 수 있어서, 사용자는 이걸 보고 다음 경로를 정합니다. 중간 결과입니다.
(클릭) 최종 결과는 3DGS와 메쉬입니다. 이건 point cloud에서 만드는 게 아니라 생성된 영상에서 따로 만듭니다. 그림은 경로 위 1, 2, 3 위치에서 3DGS를 본 화면입니다.
(클릭) 원래 3D를 만들려면 현장에서 여러 각도로 직접 찍어야 하는데, 그 촬영을 영상 생성 모델이 대신하는 겁니다. 이걸 Generative Reconstruction이라고 부르고, 전작 Lyra 1.0이 이 방식입니다.
요즘 영상 모델은 바로 옆 프레임끼리는 3D적으로 잘 맞아서 가능한 방법입니다. 문제는 "멀리 떨어진 프레임끼리"입니다.

[용어]
- 카메라 경로 (trajectory): 카메라가 어디서 어느 방향을 보며 움직일지 정한 경로. 사용자가 직접 그림
- point cloud: 3D 공간에 찍힌 점들의 모음. 픽셀마다 깊이를 알면 그 픽셀을 3D 점으로 올릴 수 있음
- 3DGS (3D Gaussian Splatting): 장면을 수많은 작은 반투명 3D 덩어리(가우시안)로 표현하는 방식. 아무 시점에서나 빠르게 그려 볼 수 있음
- 메쉬 (mesh): 삼각형 면을 이어 붙인 3D 표면. 게임 엔진·물리 시뮬레이션에 바로 쓸 수 있는 형태
- Generative Reconstruction: 사진에 없는 부분은 생성 모델로 지어내서 채운 뒤 3D로 만드는 방식
-->

---

<div class="kicker">CHALLENGE</div>

# 기존 영상 모델의 문제점<br><br>



<div class="panel mb-3">
  <div style="font-size: .85rem; margin-bottom: .5rem">영상 모델은 한 번에 정해진 길이만 만들 수 있음 → 긴 영상은 <span class="em">앞 구간을 보고 다음 구간을 이어 붙이는 방식</span> (autoregressive)</div>
  <ChunkChain />
</div>

<div class="grid grid-cols-2 gap-4">
  <div v-click class="panel" style="border-color: #f8717188">
    <div class="bad">① Spatial Forgetting (공간 망각)</div>
    <div style="font-size: .8rem; margin-top: .2rem">오래전에 본 곳이 참고 범위 밖으로 밀려남 → 다시 가면 새로 지어냄</div>
  </div>
  <div v-click class="panel" style="border-color: #f8717188">
    <div class="bad">② Temporal Drifting (시간적 드리프트)</div>
    <div style="font-size: .8rem; margin-top: .2rem">구간마다 생기는 작은 오류가 쌓여 색·형태가 점점 틀어짐</div>
  </div>
</div>

<div class="src">출처: 논문 Abstract, §1, §2, §3, §5.3</div>
<div class="concept">개념 그림 · 참고 범위 길이는 예시</div>

<!--
(약 1분)
전작 Lyra 1.0은 짧은 영상을 만들어 3D로 바꿨기 때문에 만들 수 있는 장면 크기에 한계가 있었습니다. 넓은 공간을 만들려면 영상이 길어져야 합니다.
그런데 지금의 영상 모델은 긴 영상을 한 번에 못 만들어서, 짧은 구간을 만들고 그걸 보고 다음 구간을 이어 붙입니다. (버튼 몇 번 눌러 보여주기)
모델이 한 번에 볼 수 있는 과거의 길이(context window)는 정해져 있어서, 오래된 구간은 범위 밖으로 밀려나 참고하지 못합니다. 범위 길이 2구간은 설명용 예시입니다.
여기서 두 가지 문제가 생깁니다. (클릭) 공간 망각, (클릭) 시간적 드리프트. 이건 Lyra 1.0만의 문제가 아니라 긴 영상을 만드는 기존 영상 모델 전반의 문제입니다.

[용어]
- 영상 생성 모델 (video diffusion model): 노이즈에서 시작해서 조금씩 노이즈를 걷어 내며 영상을 만드는 AI 모델
- 자기회귀 (autoregressive): 한 구간을 만들고, 그걸 보고 다음 구간을 만드는 식으로 이어 붙이는 방식
- context window: 모델이 한 번에 볼 수 있는 입력 길이의 한계. 이걸 넘는 과거는 직접 볼 수 없음
-->

---

<div class="kicker">PROBLEM ①</div>

# Spatial Forgetting: 왔던 곳을 잊어버림

<ForgettingDemo class="mt-3" />

<div class="src">출처: 논문 Abstract, §1</div>
<div class="concept">개념 시뮬레이션 · 실제 모델 결과 아님</div>

<!--
(약 1분 30초)
거실에서 시작해 복도, 침실로 갔다가 다시 거실로 돌아오는 상황입니다. (▶ 눌러 가며 진행)
모델은 직전 장면들만 참고할 수 있어서, 침실까지 갔다 오면 처음 본 거실은 기억 범위 밖입니다.
그래서 거실로 돌아오면 거실을 처음부터 새로 지어내고, 소파나 창문이 달라집니다. 3D로 만들면 같은 방이 두 가지 모습이 되는 셈이라 치명적입니다.
-->

---

<div class="kicker">PROBLEM ②</div>

# Temporal Drifting: 작은 오류가 쌓여 틀어짐

<p class="lead">복사본을 다시 복사하면 점점 흐려지는 것과 비슷 · 새로운 곳으로 갈수록 처음 장면과 겹치는 부분이 줄어 <b>기준 삼을 것도 사라져</b> 더 심해짐</p>

<DriftDemo src="lyra/fig/street_clean.jpg" />

<div class="src">출처: 논문 Abstract, §1 · 사진: 논문 Figure 1의 입력 사진</div>
<div class="concept">개념 시뮬레이션 · 실제 모델 결과 아님</div>

<!--
(약 1분)
두 번째 문제입니다. 앞 구간 결과를 보고 다음 구간을 만드니까, 앞 구간의 작은 오류가 다음 구간으로 넘어가고 계속 쌓입니다.
(슬라이더) 원본 -> 생성 사진(약간의 오차 존재) -> 그 다음 생성 사진(이전에 있던 오차에 오차가 추가로 누적) 이게 반복되며 오차가 점점 쌓이는 문제
(원인, Q&A 대비) 학습 때는 과거 프레임으로 항상 깨끗한 실제 영상을 받는데, 실제로 만들 때는 자기가 만든 불완전한 프레임을 이어받음 → 흐려지거나 틀어진 과거를 고치는 법을 배운 적이 없어 오류를 그대로 넘기고, 거기에 또 오류가 더해짐 (§4.3, observation bias). 새로운 곳으로 갈수록 처음 사진과 겹치는 부분이 줄어 붙잡아 줄 기준도 없음 (§1).
(넘어가며) 정리하면 공간 망각과 시간적 드리프트, 이 두 문제입니다. 이제 Lyra 2.0이 어떤 구조로 이걸 푸는지 전체 흐름부터 보겠습니다.

[용어]
- drift (드리프트): 작은 오류가 구간마다 쌓여서 색감·구조가 점점 원래 장면에서 멀어지는 현상
- observation bias: 학습 때 본 입력(깨끗한 정답)과 실제로 쓸 때 받는 입력(자기가 만든 결과)이 달라서 생기는 차이. 다른 논문에서는 exposure bias라고도 부름
-->
