---
layout: default
---

<div class="kicker">PIPELINE</div>

# 전체 흐름: 찾고 → 그리고 → 기억하기 (반복)

<Fig2Reader video="https://nv-tlabs.github.io/Project-Lyra/assets/issac_sim/paper_6441_supplement_video_frames2560-3868.mp4" poster="lyra/videos/gui_warehouse.jpg" :vstart="5" :vend="22" />

<div class="src">그림: 논문 Figure 2 (원본) · 설명: §4.1, Figure 2 캡션, §5 Interactive GUI · 영상: Lyra 2.0 공식 프로젝트 페이지</div>

<!--
(약 1분) 큰 그림만. 자세한 원리는 뒤 파트에서.
Lyra 2.0이 돌아가는 흐름을 논문 그림으로 간단히 보겠습니다. 사진 한 장에서 시작해서, 사용자가 경로를 줄 때마다 영상을 한 구간씩 만들고, 이걸 반복합니다. (탭 눌러 가며)
사용자 입력: 지금까지 만든 point cloud를 보면서 다음 경로를 그립니다. 오른쪽이 실제 GUI 화면입니다.
Retrieve: 가려는 곳을 예전에 본 프레임을 기억에서 찾아옵니다.
Generate: 그 프레임과 최근 프레임을 참고해서 새 구간을 그립니다.
Update: 새로 그린 프레임을 기억에 넣고, 다시 사용자 입력으로 돌아갑니다.
3D 복원: 탐험이 끝나면 쌓인 영상으로 3DGS와 메쉬를 만듭니다.

(참고) 한 구간 = 80프레임. GB200 GPU 1장으로 약 194초, 4단계로 줄인 DMD 버전은 약 15초. 기억 검색은 1초 미만. (부록 A.3)
(참고) 기억은 프레임마다 깊이·카메라를 따로 저장하고 하나의 point cloud로 합치지 않음. 생성된 프레임의 깊이는 갈수록 부정확해서, 합치면 오차가 한 덩어리에 쌓이기 때문 (§4.2). 공개 코드는 8프레임마다 1장씩 저장.
(참고) Generate 때 넣는 것: 찾아온 프레임(최대 5장) + 그 픽셀이 새 화면 어디로 가는지 3D 대응 정보 + 최근 프레임(오래될수록 더 압축) + 카메라 정보. 영상 모델은 Wan 2.1 (14B). → 본문 첫 장(영상 모델의 입력)에서 이 재료들을 한 장으로 다시 보여 줌.

[Q&A 대비] 예전에 본 곳에 다시 가면 저장된 장면을 그대로 보여 주나?
- 아니오. 같은 루프로 다시 생성함. 그때 본 프레임을 Retrieve로 찾아와 참고 + 그 픽셀이 지금 화면 어디에 오는지(대응 지도) + 최근 프레임 + 카메라 정보 → 영상 모델이 새로 그림
- 3D 정보(깊이·카메라)는 "어떤 프레임을 참고할지, 어디끼리 대응하는지"만 알려 주고, 색·모양은 전부 영상 모델이 그림 (§4.2). 생성 프레임의 깊이가 부정확해서, 그림을 그대로 옮겨 붙이면 구멍·늘어짐이 생기고 모델이 그걸 따라 그리기 때문
- 그래서 처음 본 모습과 거의 같지만 픽셀까지 똑같은 복사는 아님. 다시 그린 프레임도 기억에 또 추가됨
- 그대로 보이는 건 두 군데: GUI의 point cloud 미리보기(경로 그리는 지도), 최종 3DGS·메쉬(고정된 3D를 렌더링만 함)

[용어]
- Retrieve / Generate / Update: 찾기 / 만들기 / 기억에 넣기. 논문은 이 반복을 retrieve–generate–update loop라고 부름
- GUI: 사용자가 마우스로 경로를 그리는 화면 프로그램
- GB200: NVIDIA의 데이터센터용 GPU (Grace Blackwell 계열)
- DMD (Distribution Matching Distillation): 큰 모델의 결과 분포를 따라 하도록 학생 모델을 학습시켜 단계 수를 줄이는 기법. 여기서는 35단계 → 4단계
- Wan 2.1 (14B): Alibaba가 공개한 오픈소스 영상 생성 모델. 14B = 파라미터 140억 개. Lyra 2.0은 이걸 가져와 추가 학습
-->

---

<div class="kicker">ROADMAP</div>

# 정리: 문제와 해결책

<p class="lead">앞에서 본 두 문제를 Lyra 2.0은 각각 아래 장치로 해결 · 자세한 원리는 뒤 파트에서</p>

<div class="rm">
  <div class="muted hd">문제</div><div></div><div class="muted hd">Lyra 2.0의 해결책</div><div class="muted hd">자세히</div>
  <div class="panel"><span class="bad">① 공간 망각</span> <span class="muted">Spatial Forgetting</span></div>
  <div class="ar">→</div>
  <div class="panel"><span class="em">Anti-forgetting</span></div>
  <div class="em pt">Part 3</div>
  <div class="panel"><span class="bad">② 시간적 드리프트</span> <span class="muted">Temporal Drifting</span></div>
  <div class="ar">→</div>
  <div class="panel"><span class="em">Anti-drifting</span></div>
  <div class="em pt">Part 4</div>
</div>

<p style="font-size: .95rem; margin-top: 2.2rem">그리고 마지막 단계: 완성된 영상 → <b>3DGS · 메쉬</b>로 바꾸기 (3D Reconstruction) <span class="em">Part 5</span></p>

<style>
.rm { display: grid; grid-template-columns: 1.3fr 2.5rem 1fr 4.5rem; gap: .8rem .6rem; align-items: center; margin-top: 1.4rem; font-size: 1.05rem; }
.rm .hd { font-size: .72rem; }
.rm .ar { text-align: center; color: var(--lx-muted); font-size: 1.4rem; }
.rm .pt { text-align: center; }
</style>

<div class="src">출처: 논문 Abstract, §1, §4.1</div>

<!--
(약 30초)
정리하면, 앞에서 본 공간 망각은 Anti-forgetting, 시간적 드리프트는 Anti-drifting이라는 장치로 해결합니다. 각각 Part 3, Part 4에서 자세히 봅니다.
그리고 마지막으로 완성된 영상을 3DGS·메쉬로 바꾸는 단계를 Part 5에서 봅니다.
-->
