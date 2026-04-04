# 3D Sim2Sim — 경사 지형 주행 데이터 추출 & 학습

- 기존 2D Sim2Sim 파이프라인을 3D 경사 지형(pitch, roll)으로 확장
- Blender에서 경사/뱅크 지형 위 다양한 주행 데이터를 추출
- Genesis에서 terrain heightfield를 로드하여 Ground Truth 생성
- 10개 GT 데이터를 병합하여 MLP 지도학습 진행
- 아래 정량 지표의 단위는 pos(m), v(m/s)

---

## 3D Ground Truth 결과 (이미지 클릭시 영상 재생)

| 저속 오르막 | 저속 내리막 | 오르막→내리막 | 조향 오르막 | 조향 내리막 |
|:-----------:|:-----------:|:------------:|:-----------:|:-----------:|
| <a href="https://github.com/user-attachments/assets/de3eef87-8509-4543-bc1b-07b7845ed680"><img src="./이미지/gt1.png" width="160"></a><br>───────<br>PosErr μ=0.052m<br>max=1.108m<br>VErr μ=0.127<br>max=0.506 | <a href="https://github.com/user-attachments/assets/f9b521fe-acb2-4d11-bda0-0ffe5bc900f0"><img src="./이미지/gt2.png" width="160"></a><br>───────<br>PosErr μ=0.084m<br>max=0.578m<br>VErr μ=0.212<br>max=0.861 | <a href="https://github.com/user-attachments/assets/0ea1aa49-cbf5-4239-9657-8f35e0e33cc6"><img src="./이미지/gt3.png" width="160"></a><br>───────<br>PosErr μ=0.031m<br>max=0.537m<br>VErr μ=0.079<br>max=0.316 | <a href="https://github.com/user-attachments/assets/e3bf9098-ad17-4a66-a6fc-c9c3e6f3a4dd"><img src="./이미지/gt4.png" width="160"></a><br>───────<br>PosErr μ=0.065m<br>max=0.372m<br>VErr μ=0.179<br>max=0.627 | <a href="https://github.com/user-attachments/assets/fa38eb8b-7bd2-4f5b-9ffd-a65401cd97ed"><img src="./이미지/gt5.png" width="160"></a><br>───────<br>PosErr μ=0.073m<br>max=0.168m<br>VErr μ=0.155<br>max=0.573 |
| pitch -6.5~1.6°<br>직진 100% | pitch -1.3~6.5°<br>직진 100% | pitch -10.6~11.1°<br>직진 84% | pitch -5.5~2.8°<br>roll ±4.7°<br>커브 63% | pitch -0.6~6.0°<br>roll ±5.8°<br>커브 62% |

| S자+조향 | Roll 직진 | Roll 커브 | 급경사+커브 | 급경사 직진 |
|:---------:|:---------:|:---------:|:----------:|:----------:|
| <a href="https://github.com/user-attachments/assets/6c6eb5f1-6526-4f91-b6d4-e5613a47a20c"><img src="./이미지/gt6.png" width="160"></a><br>───────<br>PosErr μ=0.070m<br>max=1.184m<br>VErr μ=0.178<br>max=0.731 | <a href="https://github.com/user-attachments/assets/c76f47cc-9c19-4313-b908-9a75ead37ef8"><img src="./이미지/gt7.png" width="160"></a><br>───────<br>PosErr μ=0.034m<br>max=0.405m<br>VErr μ=0.141<br>max=0.549 | <a href="https://github.com/user-attachments/assets/5b59c7b6-b036-4b68-b20f-bc3f08a4ab0a"><img src="./이미지/gt8.png" width="160"></a><br>───────<br>PosErr μ=0.060m<br>max=0.764m<br>VErr μ=0.151<br>max=0.639 | <a href="https://github.com/user-attachments/assets/2a922970-ff2e-46b1-8f34-0e57c49afda8"><img src="./이미지/gt9.png" width="160"></a><br>───────<br>PosErr μ=0.073m<br>max=1.829m<br>VErr μ=0.184<br>max=0.708 | <a href="https://github.com/user-attachments/assets/c471d527-cd89-436d-ba44-650e7e2490da"><img src="./이미지/gt10.png" width="160"></a><br>───────<br>PosErr μ=0.050m<br>max=1.603m<br>VErr μ=0.131<br>max=0.510 |
| pitch -11.3~23.2°<br>roll ±4.9°<br>커브 72% | pitch -12.5~11.9°<br>roll -8.3~0°<br>직진 100% | pitch -12.6~17.2°<br>roll -11.5~4.3°<br>커브 63% | pitch -22.3~13.3°<br>roll -10.4~6.3°<br>커브 68% | pitch -22.3~16.1°<br>직진 100% |

---

## 데이터별 학습 기여 분석

| # | 움직임 | 핵심 기여 |
|---|--------|----------|
| 1 | 저속 오르막 | 오르막 throttle 보정 기초 |
| 2 | 저속 내리막 | 내리막 throttle 감속 보정 |
| 3 | 오르막→내리막 | pitch 전환 구간 (1+2의 연결) |
| 4 | 조향 오르막 | 오르막 + 커브 + roll 복합 |
| 5 | 조향 내리막 | 내리막 + 커브 + roll 복합 |
| 6 | S자+조향 | 최대 다양성 — 큰 pitch + roll + 커브 |
| 7 | Roll 직진 | 뱅크 지형에서 직진 시 roll 보정 |
| 8 | Roll 커브 | 가장 극한 — 큰 pitch + roll + 커브 |
| 9 | 급경사+커브 | 급경사(±22°)에서 조향 — 미커버 영역 보완 |
| 10 | 급경사 직진 | 최대 pitch(±22°) — 급경사 throttle 한계 |

---

## 전체 GT 오차 요약

| Category | Motion Count | Avg PosErr (m) | Avg VErr (m/s) |
|:---------|:------------:|:--------------:|:--------------:|
| 3D Ground Truth | 10 | 0.059 | 0.154 |

---

## MLP 지도학습 결과 (이미지 클릭시 영상 재생)

| 저속 오르막 | 저속 내리막 | 오르막→내리막 | 조향 오르막 | 조향 내리막 |
|:-----------:|:-----------:|:------------:|:-----------:|:-----------:|
| <a href="#"><img src="./이미지/mlp1.png" width="160"></a><br>───────<br>PosErr μ=<br>max=<br>VErr μ=<br>max= | <a href="#"><img src="./이미지/mlp2.png" width="160"></a><br>───────<br>PosErr μ=<br>max=<br>VErr μ=<br>max= | <a href="#"><img src="./이미지/mlp3.png" width="160"></a><br>───────<br>PosErr μ=<br>max=<br>VErr μ=<br>max= | <a href="#"><img src="./이미지/mlp4.png" width="160"></a><br>───────<br>PosErr μ=<br>max=<br>VErr μ=<br>max= | <a href="#"><img src="./이미지/mlp5.png" width="160"></a><br>───────<br>PosErr μ=<br>max=<br>VErr μ=<br>max= |

| S자+조향 | Roll 직진 | Roll 커브 | 급경사+커브 | 급경사 직진 |
|:---------:|:---------:|:---------:|:----------:|:----------:|
| <a href="#"><img src="./이미지/mlp6.png" width="160"></a><br>───────<br>PosErr μ=<br>max=<br>VErr μ=<br>max= | <a href="#"><img src="./이미지/mlp7.png" width="160"></a><br>───────<br>PosErr μ=<br>max=<br>VErr μ=<br>max= | <a href="#"><img src="./이미지/mlp8.png" width="160"></a><br>───────<br>PosErr μ=<br>max=<br>VErr μ=<br>max= | <a href="#"><img src="./이미지/mlp9.png" width="160"></a><br>───────<br>PosErr μ=<br>max=<br>VErr μ=<br>max= | <a href="#"><img src="./이미지/mlp10.png" width="160"></a><br>───────<br>PosErr μ=<br>max=<br>VErr μ=<br>max= |

---

## 학습시키지 않은 새로운 경사 움직임 실험 (이미지 클릭시 영상 재생)

> TODO: 미학습 경사 데이터 추가 후 작성

---

## 전체 평균 오차 요약

| Category | Motion Count | Avg PosErr (m) | Avg VErr (m/s) |
|:---------|:------------:|:--------------:|:--------------:|
| 3D Ground Truth | 10 | 0.059 | 0.154 |
| MLP (학습된 움직임) | 10 | — | — |
| MLP (비학습 새로운 움직임) | — | — | — |
