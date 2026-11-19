---
layout: default
---

<div class="kicker">PART 5 · 3D RECONSTRUCTION</div>

# 완성된 영상 → 3DGS · 메쉬

<p class="lead">긴 영상을 <span class="em">Feed-forward 3D 모델 DAv3</span>에 넣어 Forward Pass 1회로 3DGS 예측 · 그 Depth로 Mesh까지 추출</p>

<div class="grid mt-1" style="grid-template-columns: 1.62fr 1fr; gap: 1.1rem; align-items: start">
  <div>
    <div class="pipe5">
      <div><LImg src="lyra/fig/indoor_frames.jpg" class="r5" /><div class="cap5">생성된 긴 영상</div></div>
      <div class="arr5">→</div>
      <div class="dav3"><b>DAv3</b><span class="em">Fine-tuned</span><span class="ff">Feed-forward</span><span class="mu5">장면별 최적화 없이 Forward Pass 1회로 3DGS 예측</span></div>
      <div class="arr5">→</div>
      <div><LImg src="lyra/fig/indoor_3dgs.jpg" class="r5" /><div class="cap5">3DGS</div></div>
    </div>
    <div class="cap5" style="margin: .55rem 0 .25rem">Mesh 추출 <span class="mu5" style="font-weight: 400">· 2D 단면으로 그린 예시 (실제는 3D 격자 → 삼각형 Mesh)</span></div>
    <MeshSteps />
  </div>
  <div class="flex flex-col gap-2">
    <div class="panel chg"><div class="big">1/4</div><div><b>Gaussian 개수</b><div class="mu5">입력 해상도는 그대로 · <b class="em">Gaussian DPT Head의 출력 해상도</b>를 k×k (k=2)로 낮춤</div></div></div>
    <div class="panel chg"><div class="big">3,000</div><div><b>생성 영상으로 추가 학습</b><div class="mu5">Lyra 2.0이 만든 <b class="em">1분 길이 생성 영상 3,000개</b>로 Fine-tuning → 생성 영상의 오류에 강해짐</div></div></div>
    <div v-click class="panel" style="padding: .45rem .6rem">
      <div style="font-size: .7rem; margin-bottom: .1rem"><b>LPIPS-P ↓</b> <span class="mu5">영상이 3D로 일관되게 복원되는 정도 (DL3DV)</span></div>
      <LpipsP />
      <div class="mu5" style="margin-top: .2rem">Fine-tuning 효과: FID 74.39 → 65.94 · LPIPS-G 0.603 → 0.579</div>
    </div>
  </div>
</div>

<div class="peq">

<span class="pl">논문 표기</span> DAv3 = feed-forward · Gaussian DPT Head를 $k{\times}k$ downsample · 생성 영상 3,000개로 fine-tune · Mesh: depth → SDF → marching cubes <span class="mu">(§4.4, 부록 A.4)</span>

$$
\underbrace{H\times W}_{\text{입력 해상도 그대로}}
\ \xrightarrow{\ \text{Gaussian DPT Head}\ }\
\underbrace{\tfrac{H}{k}\times\tfrac{W}{k}}_{\text{출력 해상도}\ (k=2)}
\ \Rightarrow\
\underbrace{\tfrac{1}{k^2}=\tfrac{1}{4}}_{\text{Gaussian 개수}}
\qquad
\text{LPIPS-P}=\text{LPIPS}\big(\underbrace{\text{3DGS 렌더링}}_{\text{새 시점}},\ \underbrace{\text{생성 영상 프레임}}_{\text{정답 대신}}\big)
$$

</div>

<div class="src">출처: 논문 §4.4 (3D Reconstruction), 부록 A.4, §5.3, Table 2 · 그림: 논문 Figure 1 일부</div>

<style>
.pipe5 { display: grid; grid-template-columns: auto auto 1fr auto auto; align-items: center; gap: .35rem; }
.r5 { height: 108px; width: auto; border-radius: 6px; display: block; }
.cap5 { font-size: .68rem; font-weight: 700; margin-top: .15rem; }
.arr5 { text-align: center; font-size: 1.1rem; color: var(--lx-muted); margin-top: -1rem; }
.dav3 { display: flex; flex-direction: column; align-items: center; text-align: center; gap: .1rem; border: 1px solid var(--lx-line); border-radius: 8px; padding: .45rem .4rem; margin-top: -1rem; font-size: .66rem; }
.dav3 b { font-size: .9rem; }
.dav3 .ff { font-size: .6rem; font-weight: 700; color: #0d1117; background: #cbd5e1; border-radius: 4px; padding: 0 .35rem; }
.mu5 { font-size: .6rem; color: var(--lx-muted); line-height: 1.4; }
.chg { display: grid; grid-template-columns: 3.6rem 1fr; align-items: center; gap: .5rem; padding: .45rem .6rem; font-size: .72rem; }
.chg .big { font-size: 1.35rem; font-weight: 800; color: var(--lx-accent); text-align: center; }
</style>

<!--
(약 1분)
마지막 단계, 완성된 영상을 3D로 바꾸는 부분입니다. 여기는 새 아이디어보다는 기존 모델을 잘 고쳐 쓴 부분이라 짧게 보겠습니다.
DAv3는 Feed-forward 방식의 3D 모델입니다. 기존 3DGS처럼 장면마다 오래 최적화하지 않고, 영상을 넣으면 Forward Pass 한 번으로 픽셀별 3DGS 속성을 예측합니다. Lyra 2.0은 이걸 두 가지 바꿔서 씁니다.
첫째, Gaussian 개수를 4분의 1로 줄였습니다. 입력 해상도는 그대로 두고, Gaussian을 내보내는 DPT Head의 출력 해상도만 가로세로 2배씩 낮춘 겁니다.
둘째, Lyra 2.0으로 만든 1분 길이 영상 3,000개로 추가 학습했습니다. 생성 영상에는 작은 기하 오류가 섞여 있어서, 그런 영상에서도 3D가 잘 나오도록 적응시킨 겁니다.
아래는 Mesh 추출입니다. 3DGS에서 시점마다 Depth를 뽑고, Depth의 기울기로 Normal을 구해 방향 있는 점을 만들고, 이걸로 격자마다 표면까지의 거리(SDF)를 계산한 뒤, 0인 곳을 이어 Mesh를 만듭니다. Mesh가 있으면 시뮬레이터 같은 곳에서 바로 쓸 수 있습니다.
(클릭) LPIPS-P는 3DGS로 렌더링한 이미지를 생성 영상 프레임과 비교한 값입니다. 영상이 3D로 일관될수록 3DGS가 영상을 잘 재현하니까 낮게 나옵니다. Lyra 2.0이 가장 낮고, 추가 학습한 버전이 더 낮습니다.

(참고) DAv3 = feed-forward 3D 모델: 장면마다 최적화하는 기존 3DGS와 달리, 한 번의 추론으로 픽셀별 3DGS 속성을 예측. (§4.4)
(참고) Gaussian 줄이기: DAv3의 Gaussian DPT head가 k×k(k=2)로 줄인 feature map을 내도록 수정 → 고해상도 입력은 그대로 쓰면서 Gaussian 수 k² = 4배 감소. (§4.4, 부록 A.4)
(참고) 추가 학습 데이터: DL3DV의 이미지와 카메라 경로로 1분짜리 영상 3,000개를 Lyra 2.0으로 생성 → DAv3를 10,000 iteration fine-tune (lr 5e-5, batch 8). Lyra 1.0과 비슷한 전략. (부록 A.4)
(참고, 시간 부족하면 생략) 메쉬 세부 구현: OpenVDB 기반 계층형 sparse grid. 생성 카메라 근처는 촘촘한 칸, 먼 배경은 성긴 칸. 각 시점에서 Gaussian의 median depth를 깊이 지도로 렌더링 → 깊이 기울기로 normal 계산 → 방향 있는 point cloud → SDF → marching cubes → 단계별로 이어 붙이고 단순화(decimate). (§4.4, 부록 A.4)
(참고) 3D 평가 지표: LPIPS-G = 3DGS 렌더링 vs 실제 정답 프레임 (전체 품질), LPIPS-P = 3DGS 렌더링 vs 생성 영상 프레임 (영상이 3D로 얼마나 일관된지). Ours Full LPIPS-P 0.381 (DL3DV)로 가장 낮음 → 영상 자체가 3D로 일관됨. 모든 방법을 같은 DAv3로 복원해서 비교. Tanks and Temples: Ours Full 0.372, Ours + DAv3 0.409, SPMem 0.412. (§5.3, Table 2)
(참고) 왼쪽 아래 Mesh 그림은 2D 단면 예시를 실제로 계산해서 그린 것 (sphere tracing으로 Depth → point-to-plane SDF → marching squares). 논문 그림 아님.

[용어]
- feed-forward 복원: 최적화 반복 없이 신경망에 한 번 넣어서 바로 3D를 얻는 방식. 수 분 대신 수 초
- Gaussian (가우시안): 3DGS의 기본 단위. 위치·크기·색·투명도를 가진 작은 3D 덩어리
- DPT head: 이미지 특징에서 픽셀마다 값을 예측하는 출력 부분. DAv3에서는 픽셀마다 가우시안을 예측
- fine-tune: 이미 학습된 모델을 새 데이터로 조금 더 학습시키는 것
- FID: 생성 이미지들과 실제 이미지들의 분포 차이. 낮을수록 실제와 비슷
- LPIPS-G: 3DGS에서 새 시점으로 렌더링한 이미지와 실제 정답 프레임의 차이 (사람 눈 기준 유사도). 낮을수록 좋음
- SDF (signed distance function): 공간의 각 점이 표면에서 얼마나 떨어져 있는지 (안쪽은 음수) 적은 값
- OpenVDB: 빈 공간은 저장하지 않는 계층형 3D 격자 자료구조. 넓은 장면도 메모리를 적게 씀
- marching cubes: 격자의 SDF 값에서 표면(0이 되는 곳)을 찾아 삼각형 메쉬로 만드는 고전 알고리즘
-->

---

<div class="kicker">RESULTS</div>

# 결과: 화질과 카메라 제어를 둘 다 잡음

<p class="lead">기존 방법들은 화질과 카메라 제어 사이의 상충 관계가 존재 → Lyra 2.0은 <span class="em">두 성능을 균형 있게 확보</span> (긴 영상 생성, 논문 Table 1)</p>

<div class="grid gap-5" style="grid-template-columns: 1.35fr 1fr; align-items: start">
  <ResultScatter />
  <div class="flex flex-col gap-2" style="font-size: .76rem; line-height: 1.55">
    <div class="panel" style="padding: .5rem .75rem"><b>GEN3C</b> · 그림(RGB) warping으로 카메라는 정확 → 하지만 화질이 낮음 <span class="muted">(Part 3의 "그림을 옮기면" 문제)</span></div>
    <div class="panel" style="padding: .5rem .75rem"><b>CaM · SPMem</b> · 과거 프레임을 기억해 화질은 좋음 → 카메라 정보를 암묵적으로만 써서 경로를 잘 못 따름</div>
    <div class="panel" style="padding: .5rem .75rem"><b>VMem</b> · 길게 가면 일관성 유지 실패</div>
    <div class="panel" style="padding: .5rem .75rem; border-color: var(--lx-accent)"><b class="em">Lyra 2.0</b> · 3D Geometry를 주로 정보 참조에 활용 + 그림은 영상 모델이 생성 → 두 성능을 균형 있게 확보</div>
  </div>
</div>

<div class="peq">

<span class="pl">논문 표기</span> Subjective Quality ↑, Camera Controllability ↑ (WorldScore 지표) · DL3DV-Evaluation (학습 분포 안), Tanks and Temples (학습에 없던 데이터) <span class="mu">(§5, Table 1)</span>

</div>

<div class="src">출처: 논문 Table 1, §5 (Long Video Generation) · 값을 다시 그림</div>

<!--
(약 1분)
결과입니다. 가로축은 한 장면의 화질, 세로축은 카메라 경로를 얼마나 정확히 따르는지입니다. 오른쪽 위로 갈수록 좋습니다.
GEN3C는 그림을 warping해서 넣는 방식이라 카메라는 가장 정확하지만 화질이 낮습니다. Part 3에서 본 "그림을 옮기면 결함까지 따라 그린다"는 문제입니다.
CaM, SPMem은 과거 프레임을 기억해서 화질은 좋은데, 카메라 정보를 암묵적으로만 써서 경로를 잘 못 따라갑니다.
Lyra 2.0은 3D Geometry를 주로 정보 참조에 활용하고 그림은 영상 모델에 맡겨서, 두 성능을 균형 있게 확보합니다. (논문 표현: "3D geometry serves as an information routing signal", §5.2) (데이터셋 전환) 학습에 안 쓴 Tanks and Temples에서도 같은 경향입니다.

(참고) 비교 대상: Yume-1.5, GEN3C, Context as Memory(CaM), VMem, SPMem, HY-WorldPlay(동시기 연구). Yume-1.5와 HY-WorldPlay는 카메라 경로 조건이 명시적이지 않아 카메라 제어 점수 없음("--"), HY-WorldPlay는 드리프트가 심함. (§5)
(참고) 지표: Subjective Quality = 사람 지각 기준 화질, Camera Controllability = 카메라 포즈 정확도 (WorldScore 지표). (§5)
(참고) 다른 지표 (DL3DV, Ours): SSIM 0.388, LPIPS 0.498, FID 43.43 모두 1등. 스타일 일관성 87.46 (2등, 1등은 Ours DMD 88.57). 카메라 제어와 재투영 오차는 GEN3C가 1등 (69.54, 0.068) vs Ours (64.67, 0.076). (Table 1)
(참고) 정성 비교: 약 800번째 프레임에서 비교했을 때 기존 방법은 화질 저하, 형태 왜곡, 드리프트가 심함 (논문 정성 비교 그림).
(참고) 빠른 버전 DMD: 35 → 4 step, CFG 증류 → 80프레임 1회 약 194초 → 15초 (GB200 1장, 약 13배). Tanks and Temples에서 카메라 제어 63.87 → 58.12로 다소 하락, 화질은 비슷. (§4.5, 부록 A.3)
[Q&A 대비] 데이터셋? DL3DV (실제 장면 영상 약 1만 개, 학습에 사용, 평가는 DL3DV-Evaluation), Tanks and Temples (학습에 안 쓴 외부 데이터, 일반화 평가). (§5)

[용어]
- DL3DV: 실제 장면 영상 1만 개 데이터셋. Lyra 2.0의 학습 데이터. DL3DV-Evaluation은 그 평가용 분할 (학습 분포 안)
- Tanks and Temples: 학습에 없던 실제 장면 (일반화 평가)
- 비교 대상 (논문 §5 설명 기준)
  - GEN3C: depth로 warping한 그림을 조건으로 줌 → 카메라 정확, 화질 낮음 (NVIDIA의 이전 연구)
  - CaM (Context as Memory) · SPMem: 과거 프레임을 기억으로 사용, 카메라 조건은 암묵적. SPMem은 하나의 전역 point cloud로 누적. 둘 다 공개 코드가 없어 저자들이 Wan 2.1 14B로 재구현
  - VMem: 3D 표면 조각으로 과거 프레임을 검색. 길게 가면 일관성 붕괴
  - Yume-1.5: FramePack 기반, 공간 기억 없음 · HY-WorldPlay: 키보드 입력으로 조작 → 둘 다 명시적인 카메라 경로 조건을 지원하지 않아 카메라 점수 없음
-->

---

<div class="kicker">LIMITATIONS & DISCUSSION</div>

# Lyra 2.0의 한계 및 추가 검증 필요성

<div class="grid gap-5 mt-3" style="grid-template-columns: 1.05fr 1fr; align-items: start">
  <div class="flex flex-col gap-3">
    <div class="panel lim">
      <div class="limh">저자가 명시한 한계 <span class="muted">(논문 §6 Discussion)</span></div>
      <div class="li"><b>Static Scene에 한정된 생성</b><span>Dynamic Scene은 명시적으로 모델링하지 않음 · 저자도 향후 과제로 언급</span></div>
      <div class="li"><b>Photometric Inconsistency로 인한 3DGS 결함</b><span>학습 데이터(DL3DV)의 시점 간 노출 차이를 생성 영상이 재현 → Feed-forward 3DGS 복원에 결함</span></div>
    </div>
    <div class="panel lim">
      <div class="limh">발표자 관점에서의 한계</div>
      <div class="li"><i class="no">①</i><b>장시간 Autoregressive Generation에서 품질 저하가 완전히 해소되었는지 불명확</b><span>Style Consistency는 첫 · 마지막 프레임만 비교 · 정성 비교는 약 800번째 프레임 (Figure 3)</span></div>
      <div class="li"><i class="no">②</i><b>급격한 시점 변화 및 기존 관측 영역을 벗어나는 경로에 대한 강건성 검증 부족</b><span>GUI · In-the-Wild 결과는 정성적으로만 제시 (Figure 7, 8)</span></div>
      <div class="li"><i class="no">③</i><b>갑작스러운 노이즈, 품질 붕괴 등 실패 사례에 대한 정량적 분석 부족</b><span>논문에 실패 사례 분석 없음 (Discussion의 한계는 위 2가지)</span></div>
    </div>
  </div>
  <div class="flex flex-col gap-3">
    <div>
      <LVideo src="lyra/videos/lim_night.mp4" poster="lyra/videos/lim_night.jpg" class="limv" />
      <div class="limc"><i class="no">①</i> 진행할수록 화면이 어두워지고 흐려짐</div>
    </div>
    <div>
      <LVideo src="lyra/videos/lim_castle.mp4" poster="lyra/videos/lim_castle.jpg" class="limv" />
      <div class="limc"><i class="no">②</i> 탑 주변을 돌다 벽면으로 급격히 다가가는 경로</div>
    </div>
  </div>
</div>

<div class="src">논문 §3, §4.3, §5.2, §6을 기반으로 한 비판적 분석 · 영상: 발표자가 직접 생성한 예시</div>

<style>
.lim { padding: .6rem .85rem; }
.limh { font-size: .82rem; font-weight: 800; margin-bottom: .4rem; }
.limh .muted { font-weight: 400; font-size: .66rem; }
.li { position: relative; padding-left: .9rem; margin-bottom: .45rem; font-size: .72rem; line-height: 1.4; }
.li:last-child { margin-bottom: 0; }
.li::before { content: ''; position: absolute; left: 0; top: .48rem; width: 5px; height: 5px; border-radius: 50%; background: var(--lx-accent); }
.li span { display: block; font-size: .6rem; color: var(--lx-muted); margin-top: .05rem; }
.no { font-style: normal; color: var(--lx-accent); font-weight: 800; margin-right: .25rem; }
.limv { width: 100%; aspect-ratio: 896 / 384; border-radius: 6px; display: block; background: #000; }
.limc { font-size: .7rem; font-weight: 700; margin-top: .2rem; }
</style>

<!--
(약 1분)
마지막으로 한계입니다. 왼쪽은 저자들이 논문에서 직접 밝힌 한계입니다.
첫째, 정적인 장면만 다룹니다. 움직이는 사람이나 물체 같은 동적 장면은 명시적으로 모델링하지 않고, 저자들도 향후 과제로 남겼습니다.
둘째, 학습 데이터인 DL3DV에 시점마다 노출이 달라지는 영상이 섞여 있어서, 모델이 그 밝기 변화까지 따라 만듭니다. 이런 Photometric Inconsistency가 3DGS 복원에서 결함으로 나타납니다.
오른쪽은 제 관점에서 본 한계입니다. 우선 드리프트가 정말 끝까지 해결됐는지는 불명확합니다. Style Consistency는 첫 프레임과 마지막 프레임만 비교하고, 정성 비교도 800번째 프레임 정도까지만 보여 줍니다.
또 급격하게 시점을 바꾸거나 한 번도 본 적 없는 영역으로 가는 경로에 대한 정량 검증이 없고, 실패 사례 분석도 없습니다.
(영상 ①) 직접 생성한 예시입니다. 진행할수록 화면이 점점 어두워지고 흐려집니다. 장시간 생성에서 품질 저하가 남아 있는 사례입니다.
(영상 ②) 탑 주변을 크게 돌다가 벽면으로 급격히 다가가는 경로입니다. 급격한 시점 변화에 대한 사례입니다.

(참고) 논문 원문 요지 (§6 Discussion): ① 정적 환경에 집중, 동적 장면은 명시적으로 모델링하지 않음 → 향후 과제. ② 영상 모델이 학습 데이터 특성을 물려받음. DL3DV의 시점 간 노출 차이를 재현할 수 있고, 이 photometric inconsistency가 feed-forward 3DGS 복원에 결함을 만듦.
(참고) 저자가 제시한 해결 방향: 네트워크 안에서 photometric stability를 다루거나 (PPISP), 게임 엔진 같은 photometric 일관성이 있는 합성 데이터셋 사용.
(참고) 오른쪽 세 항목은 발표자 의견. 근거: Style Consistency 정의 = 첫 · 마지막 프레임 사이 드리프트 (§5.2), 정성 비교 그림 = 약 800번째 프레임 (Figure 3), GUI · In-the-Wild는 그림만 (Figure 7, 8), 실패 사례 절 없음.
[Q&A 대비] 그럼 몇 프레임까지 되나? 논문에 최대 길이 정량 결과는 없음. Figure 3이 약 800번째 프레임, 3DGS 추가 학습 데이터는 1분 길이 영상 (부록 A.4).

[용어]
- Static Scene / Dynamic Scene: 움직이는 물체가 없는 장면 / 사람·차 등 움직이는 물체가 있는 장면
- Photometric Inconsistency: 같은 곳인데 시점마다 밝기·노출·색이 달라지는 현상
- 노출 (exposure): 카메라가 빛을 받아들이는 양. 시점마다 다르면 같은 벽도 밝기가 달라 보임
- Autoregressive Generation: 앞에서 만든 결과를 다음 입력으로 써서 이어 붙여 만드는 방식
-->

---

<div class="kicker">SUMMARY</div>

# 정리: Lyra 2.0이 한 일

<div class="sumg mt-3">
  <div class="hd">문제</div><div class="hd">해결</div><div class="hd">핵심 한 줄</div>
  <div><b>공간 망각</b></div>
  <div>3D로 찾기 → warping으로 주소 대응표 → attention Q·K에 힌트</div>
  <div class="em">3D는 길 안내만, 그림은 영상 모델이</div>
  <div><b>시간적 드리프트</b></div>
  <div>Self-Augmentation (+ FramePack)</div>
  <div class="em">연습 때부터 틀린 과거를 보여 줌</div>
  <div><b>영상 → 3D</b></div>
  <div>생성 영상으로 다시 학습한 DAv3 → 3DGS · 메쉬</div>
  <div class="em">생성 영상의 오류에 강하게</div>
</div>

<div v-click class="panel mt-5" style="font-size: .8rem; line-height: 1.6">
  <div class="bad" style="margin-bottom: .2rem">한계 (논문)</div>
  <div>• 움직이는 물체가 없는 <b>정적인 장면</b>만 다룸</div>
  <div>• 학습 데이터(DL3DV)의 시점별 <b>밝기·노출 차이</b>까지 따라 만들어서 3DGS에 얼룩이 생길 수 있음</div>
</div>

<div class="src">출처: 논문 §6 (Discussion)</div>

<style>
.sumg { display: grid; grid-template-columns: 9rem 1.6fr 1.2fr; gap: .55rem 1rem; font-size: .88rem; align-items: center; }
.sumg .hd { font-size: .7rem; color: var(--lx-muted); border-bottom: 1px solid var(--lx-line); padding-bottom: .2rem; }
</style>

<!--
(약 40초)
정리하겠습니다. 공간 망각은 3D로 과거 프레임을 찾고, warping으로 주소 대응표를 만들어, attention에 힌트로 넣어서 풀었습니다. 핵심은 3D는 길 안내에만 쓰고 그림은 영상 모델이 그린다는 것입니다.
시간적 드리프트는 학습 때부터 모델 자신의 틀린 과거를 보여 주는 Self-Augmentation으로 풀었습니다.
그리고 이렇게 만든 긴 영상을 생성 영상에 맞게 다시 학습한 DAv3로 3DGS와 메쉬로 바꿉니다.
(클릭) 한계도 있습니다. 움직이는 물체가 없는 정적인 장면만 다루고, 학습 데이터의 시점별 밝기 차이까지 따라 만들어서 3D에 얼룩이 생길 수 있습니다.

(참고) 논문이 제안한 해결 방향: 네트워크 안에서 밝기 안정화, 또는 게임 엔진 같은 밝기가 일정한 합성 데이터 사용. (§6)
(참고) 활용: 인터랙티브 탐색, VR, 시뮬레이션 (논문에 NVIDIA Isaac Sim 데모 언급). (§6)
-->
