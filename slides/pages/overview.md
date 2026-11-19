---
layout: default
---

<div class="kicker">본문 시작 · 영상 모델의 입력</div>

# 영상 모델(DiT)의 입력: 4개 그룹

<p class="lead">Part 2의 <b>Generate</b> 단계에서 DiT에 들어가는 입력 · 각 입력을 만드는 방법이 Part 3 · 4</p>

<ContextLayout />

<div class="src">출처: 논문 §3 (Preliminaries · FramePack), §4.2 (context layout), 부록 A.1 · 논문 표기를 그림으로 다시 그림</div>

<!--
- DiT는 토큰이 많을수록 계산이 급격히 무거워집니다. attention은 모든 토큰 쌍을 보기 때문입니다.
  - 그래서 정해진 토큰 예산 안에서 더 긴 과거를 보려고 줄입니다.
5장 중 어느 것을 원본으로 두는지, 왜 이 비율인지는 논문에 나오지 않습니다.
[Q&A 대비] spatial 5장 중 어느 것이 원본 해상도(f1k1)인가?
- 논문: "4 frames at subsampling factor 2 and 1 frame at full resolution"까지만 씀. 어느 것인지, 왜 4:1인지는 논문에 없음
- 공식 코드 (nv-tlabs/lyra, Lyra-2 lyra2_model.py): 추론 때 greedy가 고른 순서를 뒤집어서 [5번째, 4번째, 3번째, 2번째, 1번째 선택] 순으로 슬롯에 넣음 → 앞 4칸이 f4k2, 마지막 칸이 f1k1 → 첫 번째로 고른 이미지(새 시점을 가장 많이 덮는 이미지)가 원본 해상도
- 5장보다 적게 찾으면 앞쪽(축소 칸)부터 첫 프레임으로 채움 (padding). 학습 때는 점수 비례 무작위 추출이라 순서가 확률적
- 비율의 이유는 논문·코드 어디에도 설명 없음. FramePack의 동기(정해진 토큰 예산 안에서 더 많은 프레임)를 spatial에도 적용했다고만 씀
[Q&A 대비] 각 그룹에 붙는 조건 (부록 A.1 + 공식 코드)
- spatial 이미지: 자기 좌표맵 C_j (warping 안 한 원래 주소)
- 생성 구간: warping된 좌표맵 [Ĉ_j; D̂_j] (5장 각각) + 직전 프레임을 warping한 RGB (VAE 인코딩 후 채널로 이어 붙임)
- temporal 프레임: 좌표맵 없음 (0으로 채움)
- Plücker ray: 모든 프레임 (temporal, spatial, 생성)

[용어]
- DiT (Diffusion Transformer): 노이즈 제거(diffusion)를 transformer 구조로 하는 모델. 이미지·영상을 작은 조각(토큰)으로 나눠 한꺼번에 처리
- Transformer: 입력 조각들이 서로를 참고(attention)하며 정보를 섞는 신경망 구조. ChatGPT 같은 언어 모델도 같은 구조
- Wan 2.1 14B: Alibaba가 공개한 오픈소스 영상 생성 DiT. 14B = 파라미터 140억 개
- VAE: 영상을 작은 요약본(latent)으로 압축하고 다시 복원하는 신경망. 여기서는 가로세로 8배, 시간 4배 압축
- latent: VAE로 압축된 영상. 모델은 실제 픽셀이 아니라 이 latent 위에서 작업. latent 1개 ≈ 영상 4프레임
- 토큰 (token): latent를 잘게 나눈 조각 하나. transformer가 처리하는 기본 단위. 토큰이 많을수록 계산이 무거움
- self-attention: 모든 토큰이 다른 모든 토큰을 보고, 관련 있는 것끼리 정보를 주고받는 연산
- Q · K · V (query · key · value): attention의 세 역할. Q = 내가 찾는 것, K = 각 토큰의 꼬리표, V = 실제로 가져올 내용. Q와 K가 잘 맞을수록 그 V를 많이 가져옴
- slot (슬롯): 모델 입력에서 특정 용도로 예약된 칸. spatial slot = 찾아온 과거 프레임 칸, temporal slot = 최근 영상 칸
- anchor (앵커): 기준점. 항상 같이 넣는 첫 사진 I₀
- FramePack: 오래된 프레임일수록 더 크게 줄여서(토큰을 적게) 넣는 기존 기법. 같은 토큰 예산으로 더 긴 과거를 볼 수 있음
- fnkm: 프레임(latent) n개를 가로세로 m배 줄여서 넣는다는 표기. g20 = 새로 만들(generate) latent 20개
- flow matching: 노이즈와 정답 사이를 직선으로 잇고, 그 방향(속도)을 맞히도록 학습하는 생성 모델 학습법
- velocity (속도) v: 노이즈 쪽에서 정답 쪽으로 가려면 어느 방향으로 얼마나 움직여야 하는지. 모델이 이걸 예측해서 조금씩 노이즈를 걷어 냄
- z₀ / ε / z_t / t: 정답 latent / 순수 노이즈 / 둘을 섞은 것 / 섞은 비율 (0 = 정답, 1 = 노이즈)
- c (condition): 모델에 주는 조건 전체 (과거 프레임, 카메라, 텍스트 등)
- Plücker ray: 픽셀마다 "카메라에서 그 픽셀로 나가는 광선"을 숫자 6개로 표현한 것. 카메라 위치·방향을 픽셀 단위로 알려 주는 방법
- 832×480: 생성 영상 해상도 (가로×세로 픽셀)
-->
