---
layout: default
---

<StepBar :steps="['① 찾기', '② Warping', '③ 대응표', '④ Attention']" :cur="0" />

<div class="kicker">PART 3 · ANTI-FORGETTING</div>

# ① 기억에서 찾기: 지금 볼 곳을 예전에 본 프레임

<p class="lead">프레임마다 <span class="em">원본 Depth + 카메라 파라미터 + 검색용 Point Cloud</span> 저장 → 새 시점에 투영해서 과거 프레임 최대 5장 선택</p>

<div class="grid gap-5" style="grid-template-columns: 1.25fr 1fr; align-items: start">
  <RetrievalDemo />
  <div class="flex flex-col gap-3" style="font-size: .8rem; line-height: 1.55">
    <div class="panel" style="padding: .6rem .8rem">
      <div class="em" style="margin-bottom: .25rem">저장: 프레임별 기억</div>
      <div>• 만든 프레임마다 원본 Depth + 카메라 파라미터 + 검색용 Point Cloud 저장</div>
      <div>• 하나의 3D로 <b>합치지 않음</b> → 프레임별 Depth 추정 오차로 인한 3D 정합 불일치 방지</div>
    </div>
    <div class="panel" style="padding: .6rem .8rem">
      <div class="em" style="margin-bottom: .25rem">찾기: 3D로 투영</div>
      <div>• 각 프레임의 점들을 새 화면에 투영 → 가려지지 않고 보이는 점 개수 = Visibility Score</div>
      <div>• 아직 안 채워진 곳을 가장 많이 채우는 프레임부터 (Greedy)</div>
    </div>
  </div>
</div>

<div class="peq">

<span class="pl">논문 표기</span> 프레임 $i$마다 저장, 목표 시점 $(\mathbf{T}^*,\mathbf{K}^*)$에 투영해서 Visibility Score 계산 · 보이는 점: $z - z_{\min}(u,v) < \delta$ <span class="mu">(§4.2)</span>

$$
\mathcal{C}:\ \big(\underbrace{D_i}_{\text{원본 Depth}},\ \underbrace{(\mathbf{T}_i,\mathbf{K}_i)}_{\text{카메라 파라미터}},\ \underbrace{\mathbf{P}_i\in\mathbb{R}^{(H/d)\times(W/d)\times 3}}_{\text{검색용 Point Cloud }(d\,=\,8)}\big)
\qquad
\underbrace{\phi(i)}_{\text{Visibility Score}}
\ \xrightarrow{\ \text{greedy}\ }\
\underbrace{N_s=5}_{\text{최대 장수}}
$$

</div>

<div class="src">출처: 논문 §4.2 (Spatial Memory, Geometry-aware Retrieval), 부록 A.2</div>
<div class="concept">왼쪽: 개념 시뮬레이션 (위에서 본 2D)</div>

<!--
(약 1분 20초)
이제 Part 3, 공간 망각을 막는 Anti-forgetting입니다. 앞 장의 "찾아온 과거 프레임"과 "주소 대응표"를 만드는 과정이고, 네 단계로 보겠습니다. 찾고, 옮기고, 대응표를 만들고, attention에 넣는 순서입니다. (오른쪽 위 단계 표시)
먼저 기억입니다. 영상 모델은 최근 몇십 프레임만 보기 때문에, 오래전에 본 곳을 잊어버립니다. 그래서 Lyra 2.0은 만든 프레임마다 원본 Depth, 카메라 파라미터, 검색용 Point Cloud를 따로 저장해 둡니다. 중요한 건 하나의 3D로 합치지 않는다는 점입니다. Depth는 생성된 프레임에서 추정하므로 프레임마다 오차가 있고, 합치면 그 오차 때문에 3D 정합이 어긋난 하나의 망가진 3D가 됩니다.
(왼쪽 데모) 위에서 본 방입니다. A부터 F는 예전에 찍은 프레임, 흰 삼각형이 지금 만들 새 시점입니다. 아래 칸은 새 화면을 24칸으로 나눈 것입니다.
각 프레임의 점들을 새 화면에 투영해서, 가려지지 않고 보이는 점이 많을수록 Visibility Score가 높습니다. (Score순 ↔ Greedy 전환) Score순으로 뽑으면 A, B처럼 비슷한 곳을 본 프레임이 중복되지만, Lyra는 아직 안 채워진 칸을 가장 많이 채우는 프레임부터 고릅니다. 이렇게 최대 5장을 찾습니다.
빈칸은 예전에 본 적 없는 곳이라 모델이 새로 그립니다.
그런데 찾아오기만 하면 끝이 아닙니다. 찾아온 프레임의 어느 픽셀이 새 화면의 어디인지를 알려 줘야 하는데, 그게 다음 단계인 warping입니다.

(참고) 저장 내용: 프레임마다 원본 해상도 깊이 + 카메라(포즈, 내부 파라미터), 그리고 검색용으로 8배 줄인 point cloud (832×480 → 104×60). 깊이는 Depth Anything V3로 추정. (§4.2, A.2)
(참고) 가려짐 처리 z − z_min(u, v) < δ: 새 화면 픽셀 (u, v)마다 모든 프레임 점 중 가장 가까운 깊이 z_min을 구하고, 점의 깊이 z가 그보다 δ = 0.1(정규화 깊이) 이상 뒤에 있으면 안 보이는 것으로 침. (§4.2, A.2) 이 식은 논문 문장("difference between its depth and the minimum depth is less than δ")을 식으로 옮긴 것
(참고) 학습 때는 Greedy가 아니라 점수에 비례해 무작위로 뽑음 → 검색 결과가 조금 달라도 버티게. (§4.2)
(참고) 왜 5장: 부록 실험(학습 영상 뒷부분 기준)에서 커버율이 1장 28.9% → 5장 42.6% → 10장 45.0%로, 5장 이후 거의 안 늘어서 효율과 균형. 몇 개 영상으로 쟀는지는 논문에 없음. (부록 A.1)
(참고) 검색 시간: 1회 1초 미만. (부록 A.3)
(참고) 공개 코드는 8프레임마다 1장꼴로 기억에 저장 (spatial_memory_stride=8), 검색 장수 옵션 기본값은 1.
[Q&A 대비] 왜 하나의 3D로 합치지 않나? 논문 실험(Tanks and Temples): 하나의 point cloud로 합쳐 그 렌더링을 조건으로 쓰게 바꾸면 카메라 제어 63.87 → 49.86, 스타일 일관성 85.07 → 82.42. 기존 GEN3C, Lyra 1.0 계열이 이 방식. (§1, Ablation "w/ Global Point Cloud")
[Q&A 대비] 다시 돌아오면 저장한 화면을 그대로 보여 주나? 아니요. 매번 이 찾기 → 생성 과정을 거쳐 새로 생성. 찾아온 과거 프레임을 강하게 참고해서 같은 장면이 나오는 것.

[용어]
- 3D cache: 만든 프레임마다 깊이 지도·카메라·점들을 따로 저장해 둔 기억 장소
- 깊이 지도 (depth map) D_i: 픽셀마다 카메라에서 얼마나 먼지 적은 이미지
- Depth Anything 3 (DAv3): 사진(들)에서 깊이와 카메라를 추정하는 공개 모델. Lyra 2.0은 생성된 프레임의 깊이를 이걸로 추정
- 카메라 외부 파라미터 T_i (extrinsic): 카메라가 어디에 있고 어느 방향을 보는지
- 카메라 내부 파라미터 K_i (intrinsic): 렌즈 특성 (초점 거리, 화면 중심). 같은 위치라도 줌이 다르면 다르게 찍힘
- 다운샘플 (d = 8): 가로세로 8칸마다 1점만 남겨서 가볍게 만듦. 검색용이라 대충이어도 충분
- 투영 (projection): 3D 점이 특정 카메라 화면의 어느 픽셀에 찍히는지 계산하는 것
- 가려짐 (occlusion): 앞의 물체에 가려서 안 보이는 것. 같은 픽셀에 여러 점이 오면 가장 가까운 것만 보임
- δ (델타): 가려짐 판정 허용 오차. 가장 가까운 깊이와 차이가 δ보다 작으면 보인다고 침
- greedy (탐욕적 선택): 매 단계 지금 가장 좋은 것 하나를 고르는 방식. 여기서는 "아직 안 채운 곳을 가장 많이 채우는 프레임"을 하나씩 추가
-->

---

<StepBar :steps="['① 찾기', '② Warping', '③ 대응표', '④ Attention']" :cur="1" />

<div class="kicker">PART 3 · ANTI-FORGETTING</div>

# ② Warping: 과거 픽셀이 새 화면 어디로 가는지 계산

<p class="lead">픽셀마다 <span class="em">깊이</span>를 알고, 두 카메라의 위치·회전을 알면 → 과거 화면의 픽셀이 새 화면 어디에 찍히는지 계산할 수 있음</p>

<WarpGeo />

<div class="peq">

<span class="pl">논문 표기</span> $\mathbf{T}_i=[\mathbf{R}_i\mid\mathbf{t}_i]$: world → camera · $\mathbf{K}_i$: 카메라 내부 파라미터 · $D_i$: 깊이 <span class="mu">(§3)</span> · $s$ = 과거 프레임 A, $*$ = 새 시점 B · 논문은 아래 과정을 $\texttt{FwdWarp}(\cdot)$ 하나로 씀 <span class="mu">(아래는 풀어 쓴 식)</span>

$$
\underbrace{p \xrightarrow{\ D_s(p)\,\mathbf{K}_s^{-1}\ } X^{s}_{\text{cam}} \xrightarrow{\ \mathbf{T}_s^{-1}\ } X_{\text{world}}}_{\text{① 픽셀 + 깊이 → 3D 점 (흰 선)}}\ \underbrace{\xrightarrow{\ \mathbf{T}^{*}\ } X^{*}_{\text{cam}} \xrightarrow{\ \mathbf{K}^{*}\ +\ \text{Perspective Division}\ } p^{*}}_{\text{② 새 카메라로 다시 찍기 (청록 점선)}}
$$

</div>

<div class="src">출처: 논문 §3 (depth-based warping), §4.2 (forward warping)</div>
<div class="concept">개념 시뮬레이션 · 위에서 본 2D, 화면은 한 줄로 단순화</div>

<!--
(약 1분 20초)
두 번째, warping입니다. Lyra 2.0의 대응 관계는 모두 이 계산에서 나옵니다.
(왼쪽 그림) 위에서 내려다본 장면입니다. 흰 카메라 A가 예전에 찍은 과거 프레임, 청록 카메라 B가 지금 만들 새 시점입니다. 오른쪽 위 띠는 A가 찍은 화면 한 줄입니다.
(A 화면 칸에 마우스) A 화면의 픽셀 하나를 고르면, 그 픽셀의 깊이를 알기 때문에 흰 선처럼 3D 공간의 점 하나로 되살릴 수 있습니다. 이게 ① 단계입니다.
그 3D 점을 B 카메라로 다시 찍으면, 청록 점선처럼 B 화면의 어느 칸에 오는지가 나옵니다. 이게 ② 단계입니다. 이걸 모든 픽셀에 하면 A 화면을 B 시점으로 옮긴 결과, 아래 띠가 나옵니다. 이게 warping입니다.
(슬라이더로 B 이동) 가까운 노란 기둥은 많이 움직이고 먼 건물은 조금 움직입니다. 그리고 기둥 뒤처럼 A에서 가려져 있던 곳은 옮겨 올 픽셀이 없어서 검은 빈칸이 됩니다.
정리하면, warping은 "과거 픽셀 → 새 화면 위치"라는 대응 관계를 계산하는 도구입니다. 그럼 무엇을 옮길까요? 다음 장입니다.

(참고) 수식으로: 3D 점 X = D(p)·K_A⁻¹·p (픽셀 p를 깊이 D만큼 뻗기, 카메라 A 좌표) → 월드 좌표로 변환 → 카메라 B로 투영 p' = K_B·[R|t]_B·X. 여러 점이 같은 칸에 오면 가장 가까운 것만 남김 (z-buffer). 이렇게 앞으로 밀어 보내는 방식을 forward warping이라 함.
(참고) 깊이는 생성된 프레임에서 Depth Anything V3로 추정한 값. 그래서 조금 틀릴 수 있음 → 뒤에서 이걸 모델이 보정.
(참고) 이 warping은 기존 카메라 제어에도 쓰임: 직전 프레임의 그림(RGB)을 새 카메라 위치로 warping해서 "이렇게 보일 것" 힌트로 줌 (GEN3C 등, 논문 §3). 여기에 카메라 광선 정보(Plücker)도 함께 넣어서 카메라 경로를 따르게 함. Lyra 2.0도 이 기본 장치는 그대로 씀.

[용어]
- warping (와핑): 한 시점에서 찍은 이미지를 다른 시점에서 본 모습으로 옮기는 것
- forward warping: 원본 픽셀을 하나씩 새 화면 위치로 보내는 방식. 아무도 안 오는 곳은 구멍으로 남음
- world 좌표 / camera 좌표: 장면 전체 공통 좌표계 / 특정 카메라 기준 좌표계. T_i가 world → camera 변환
- 역투영 (unprojection): 픽셀 + 깊이 → 3D 점. 투영의 반대
- z-buffer: 같은 픽셀에 여러 점이 오면 가장 가까운 것만 남기는 규칙
- 구멍 (hole / disocclusion): 원래 시점에서 가려져 있다가 새 시점에서 드러난 곳. 과거 정보가 없으니 새로 그려야 함
-->

---

<StepBar :steps="['① 찾기', '② Warping', '③ 대응표', '④ Attention']" :cur="2" />

<div class="kicker">PART 3 · ANTI-FORGETTING</div>

# ③ 그림 대신 '주소'를 옮겨서 대응표 만들기

<p class="lead">찾아온 과거 프레임마다 <span class="em">픽셀 주소</span>를 warping → 새 화면 픽셀마다 "과거 프레임 j의 어느 픽셀인지" 대응표 (canonical coordinate)</p>

<div class="grid gap-4" style="grid-template-columns: 2.1fr 1fr; align-items: start">
  <CoordWarp />
  <div class="flex flex-col gap-3" style="font-size: .76rem; line-height: 1.55">
    <div class="panel" style="padding: .55rem .75rem">
      <div class="bad" style="margin-bottom: .2rem">그림(RGB)을 옮기면</div>
      <div>구멍 · 늘어짐 · 경계 번짐이 생김 → 모델이 <b>결함까지 재생성</b>할 수 있음</div>
    </div>
    <div class="panel" style="padding: .55rem .75rem; border-color: var(--lx-accent)">
      <div class="em" style="margin-bottom: .2rem">주소를 옮기면</div>
      <div>"어디끼리 같은 곳인지"만 전달, 외형 정보 없음 → 그림은 원본 과거 프레임을 보고 <b>모델이 그림</b></div>
    </div>
    <div class="muted" style="font-size: .7rem">픽셀마다 4채널: <b>u, v</b> (픽셀 위치) · <b>Slot ID j</b> · <b>Depth</b></div>
  </div>
</div>

<div class="peq">

<span class="pl">논문 표기</span> canonical coordinate warping <span class="mu">(§4.2)</span> · $u, v \in[-1,1]$ 픽셀 위치 · $j$ = 검색된 Spatial Slot 번호 · 대응 없는 곳은 비움

$$
\underbrace{\mathbf{C}_j=\big(u,\ v,\ 2\tfrac{j}{N_s}-1\big)}_{\text{왼쪽: 과거 프레임 } j \text{ 의 주소}}
\ \xrightarrow{\ \texttt{FwdWarp}(\mathbf{C}_j,\,D_{s_j},\,\mathbf{T}_{s_j},\,\mathbf{T}^*,\,\mathbf{K}_{s_j},\,\mathbf{K}^*)\ }\
\underbrace{[\,\hat{\mathbf{C}}_j\,;\ \hat{D}_j\,]}_{\text{오른쪽: 새 화면 대응표 + 옮긴 깊이 (4채널)}}
$$

</div>

<div class="src">출처: 논문 §4.2 (Canonical Coordinate Warping)</div>
<div class="concept">개념 시뮬레이션 · 단순한 장면, 카메라 옆 이동만</div>

<!--
(약 1분 20초)
세 번째, 무엇을 옮길지입니다. 앞에서 본 warping으로 과거 프레임을 새 시점에 옮길 수 있는데, 그림 자체를 옮길 수도 있고 다른 걸 옮길 수도 있습니다.
(그림을 옮기면) 그림을 옮기면 가까운 기둥과 벤치 뒤에 구멍이 생기고 경계가 깨집니다. 논문에 따르면 이걸 조건으로 주면 모델이 이 결함까지 따라 그립니다. 생성 능력을 쓰는 대신 옮긴 그림에 기대 버리는 겁니다.
(주소를 옮기면) 그래서 Lyra 2.0은 색 대신 주소를 옮깁니다. 과거 프레임의 픽셀마다 "나는 (u, v) 위치의 픽셀"이라는 좌표를 붙이고, 그 좌표를 warping합니다. 색은 좌표를 눈에 보이게 칠한 것일 뿐입니다.
(오른쪽에 마우스) 그러면 새 화면 픽셀마다 "여기는 과거 프레임 j의 저 픽셀과 같은 곳"이라는 대응표가 생깁니다. 실제로는 픽셀마다 u, v, 몇 번째 프레임인지 j, 그리고 옮겨진 깊이까지 숫자 4개가 들어갑니다. 검은 곳은 대응이 없는, 처음 보는 곳입니다.
찾아온 5장 각각에 대해 이 대응표를 만듭니다. 이제 이 대응표를 모델에 어떻게 넣는지가 마지막 단계입니다.

(참고) 논문 정의: C_j = (u, v, 2·j/N_s − 1), 값 범위 [−1, 1]. u, v = 정규화된 픽셀 위치, j = 찾아온 프레임 번호(0~4), N_s = 5. 이 좌표 지도를 원본 해상도 깊이로 forward-warp → Ĉ_j. 옮겨진 깊이 D̂_j를 4번째 채널로 추가 → 프레임마다 4채널 지도 [Ĉ_j; D̂_j]. (§4.2)
(참고) "canonical"인 이유: 각 과거 프레임 자기 픽셀 격자를 기준으로 고정된 좌표라서, 그림 내용과 무관하게 항상 같은 값.
(참고) 5장보다 적게 찾으면 빈 슬롯을 채워(padding) 진짜 대응과 빈칸을 모델이 구분하게 함. (§4.2)
(참고) 논문 표현: RGB warping은 disocclusion 구멍, 늘어짐(stretching), 깊이 경계 번짐(bleeding)이 생기고, 모델이 이걸 "목발(crutch)"처럼 써서 생성 능력을 우회함. 좌표는 같은 대응 정보를 외형 정보 없이 전달. (§4.2)
(참고) 직전 프레임의 RGB warping(카메라 제어용 기본 장치)은 그대로 유지. 찾아온 과거 프레임에만 주소를 씀. (부록 A.1)
[Q&A 대비] 실제 3D 좌표(XYZ)를 넣는 건가? 아니요. 과거 프레임 이미지상의 픽셀 위치(u, v)와 프레임 번호. 3D 계산은 warping에서만 쓰임.

[용어]
- canonical coordinate (정규 좌표): 픽셀의 "원래 주소"를 −1~1로 정규화한 값. 여기서는 (u, v, Spatial Slot 번호 j)
- 채널 (channel): 픽셀 하나가 가진 숫자 칸 수. RGB = 3채널, 여기 주소 = u, v, j, 깊이 4채널
- padding: 찾은 프레임이 5장보다 적을 때 빈 칸을 정해진 값으로 채우는 것
- crutch (목발): 모델이 warping된 그림을 그대로 베끼는 데 의존해 버리는 문제를 논문이 부른 표현
-->

---

<StepBar :steps="['① 찾기', '② Warping', '③ 대응표', '④ Attention']" :cur="3" />

<div class="kicker">PART 3 · ANTI-FORGETTING</div>

# ④ 대응표를 attention에 넣기: 어디를 참고할지 알려 줌

<p class="lead">새 화면의 Query가 과거 프레임의 Key·Value를 참조하는 상황을 예시로 표현 · 주소 힌트를 <span class="em">Q · K</span>에 더함</p>

<div class="grid gap-4" style="grid-template-columns: 2.1fr 1fr; align-items: start">
  <AttnDemo />
  <div class="flex flex-col gap-3" style="font-size: .76rem; line-height: 1.55">
    <div style="line-height: 1.6">
      <div>• 주소 정보를 활용해 대응되는 Token에 높은 Attention을 부여하도록 학습 (비중 = softmax)</div>
      <div>• V는 그대로 → 색 · 모양은 <b>원본 과거 프레임</b>에서 가져옴</div>
      <div>• 학습된 Attention이 부정확한 대응 정보의 영향을 완화할 수 있음</div>
    </div>
  </div>
</div>

<div class="peq">

<span class="pl">논문 표기</span> 주소를 $\mathbf{p}$로 인코딩 (positional encoding → pixel shuffle + linear) 해서 모든 블록에 더함 <span class="mu">(부록 A.1, Figure 2)</span>

$$
\mathbf{q}=W_Q(\mathbf{x}+\underbrace{\mathbf{p}}_{\text{새 화면: }\hat{\mathbf{C}}_j}),\qquad
\mathbf{k}=W_K(\mathbf{x}+\underbrace{\mathbf{p}}_{\text{과거 프레임: }\mathbf{C}_j}),\qquad
\underbrace{\mathbf{v}=W_V\,\mathbf{x}}_{\text{그대로 (색·모양)}}
$$

</div>

<div class="src">출처: 논문 §4.2, Figure 2, 부록 A.1 (Canonical Coordinate Injection)</div>
<div class="concept">개념 시뮬레이션 · 토큰 단위로 단순화</div>

<style>
.fx { font-family: ui-monospace, monospace; font-size: .74rem; }
.fx b { color: var(--lx-accent); }
</style>

<!--
(약 1분 30초)
마지막 단계, 이 대응표를 모델에 넣는 방법입니다. 영상 모델은 transformer라서, 이미지를 작은 조각(토큰)으로 나눠 attention으로 서로 정보를 주고받습니다. 새로 만들 화면의 토큰이 Query, 찾아온 과거 프레임의 토큰이 Key와 Value입니다. Query와 Key가 비슷할수록 그 Value를 많이 가져옵니다.
(주소 힌트 없이) 대응 정보가 없으면, 새 화면 토큰은 과거 프레임의 어디를 봐야 할지 스스로 알아내야 합니다. 시점이 크게 바뀌면 이게 어려워서 여러 곳을 흐리게 섞거나 엉뚱한 자리를 봅니다. (오른쪽에 마우스 → 왼쪽 넓게 퍼진 하이라이트)
(주소 힌트 넣기) Lyra 2.0은 과거 프레임 토큰에는 원래 주소를, 새 화면 토큰에는 앞에서 옮겨 온 주소를 Query와 Key에 더합니다. 그러면 주소가 같은 토큰끼리 q·k가 커져서, 새 화면 토큰이 과거 프레임의 정확히 맞는 자리를 봅니다. (마우스 → 한 칸에 집중)
그리고 Value는 건드리지 않기 때문에, 실제 색과 모양은 원본 과거 프레임에서 그대로 가져옵니다. 즉 3D는 "어디를 볼지" 길 안내만 하고, 그림은 모델이 원본을 보고 그립니다. 빗금 친 곳처럼 대응이 없는 곳은 모델이 새로 그립니다.
정리하면 Anti-forgetting은 3D로 찾고, warping으로 대응을 구하고, 그 대응을 attention 힌트로 넣어서, 다시 돌아왔을 때 같은 장면을 그리게 합니다.

(참고) 실제 넣는 방법: 4채널 지도 [Ĉ_j; D̂_j] → latent 해상도로 pixel shuffle → 채널별 sinusoidal positional encoding → pixel shuffle + linear(학습되는 MLP) → 모든 transformer 블록의 self-attention Q·K에 더함, V는 그대로. 카메라 광선 정보(Plücker)도 같은 방식으로 Q·K에 더함. 새로 추가한 모듈은 0으로 초기화해서 처음엔 원래 Wan 2.1과 똑같이 동작. (부록 A.1, A.2)
(참고) 논문 표현: 이 설계는 대응 신호가 "어떤 생성 토큰이 어떤 spatial slot(과거 프레임)을 볼지"를 정하게 하고, V는 사전학습 모델 그대로 유지. (부록 A.1)
(참고) "과거 프레임 토큰에 원래 주소 C_j를 붙임"은 Figure 2의 "Attach 3D coords C_j" 표시 근거. 본문 문장에는 옮긴 주소를 넣는다고만 나옴.
(참고) 데모는 개념: 실제로는 정확히 한 칸만 보는 게 아니라, 학습된 attention이 힌트를 참고해 비중을 정함. 힌트 없는 경우도 실제 모델은 카메라 정보로 어느 정도 추측함.
(참고) 찾아온 과거 프레임은 VAE로 각각 따로 인코딩해서 토큰으로 넣고(spatial slots), 최근 영상 토큰, 새로 만들 토큰과 함께 하나의 self-attention에서 같이 처리. (§4.2)
[Q&A 대비] 깊이 계산으로 직접 합치면 안 되나? 논문 실험: attention 학습 대신 깊이 기반으로 직접 합치면 카메라 제어 63.87 → 57.29 (Ablation "w/ Explicit Corr. Fusion"). 깊이가 틀릴 수 있어서 학습된 방식이 더 잘 버팀.
[Q&A 대비] 왜 V는 안 건드리나? 힌트가 "누가 누구를 볼지"만 바꾸고, 내용 표현은 사전학습된 모델 그대로 두기 위해 (부록 A.1).

[용어]
- softmax: 점수들을 합이 1인 비율로 바꾸는 함수. attention에서 "어느 토큰을 얼마나 볼지" 비중
- positional encoding (sinusoidal): 숫자 하나를 여러 주파수의 sin·cos 값으로 펼쳐서 신경망이 미세한 차이를 구분하기 쉽게 만드는 방법
- pixel shuffle: 가로세로 이웃 픽셀 묶음을 채널 방향으로 접어서 해상도를 줄이는 연산. 여기서는 주소 지도를 latent 크기에 맞추는 데 사용
- linear layer: 가장 단순한 신경망 층 (곱하고 더하기)
- zero-init: 새로 붙인 층을 0으로 시작. 처음에는 원래 Wan 모델과 똑같이 동작하다가 학습하며 점점 힌트를 쓰게 됨
- transformer 블록: transformer를 이루는 반복 단위. Lyra 2.0은 모든 블록의 Q·K에 주소 힌트를 더함
-->
