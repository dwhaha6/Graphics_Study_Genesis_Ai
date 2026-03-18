# 📘Genesis AI Research History

> Genesis 물리 시뮬레이터를 기반으로
> 로봇 제어, 강화학습 구조 분석, 자동차 시뮬레이션 및 데이터 기반 제어까지
> 단계적으로 확장해 온 개인 연구 기록입니다.
> 주요 report md들은 Highlight에 그 내용을 요약해두었습니다.

**[Sim2Sim 결과 바로보기🚗](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0228_varius_data_learning.md)**

---

## 🗓 Project Timeline

| Phase | Period | Focus |
|:------|:-------|:------|
| **Phase 1** | 2025.09 | Genesis & Robot Simulation Fundamentals |
| **Phase 2** | 2025.10 | Reinforcement Learning Scaling & Performance |
| **Phase 3** | 2025.11 | Vehicle Simulation & Data Collection |
| **Phase 4** | 2025.12 | Neural Network-Based Vehicle Control |
| **Phase 5** | 2026.01 | Revisiting Control Data Extraction Pipelines |
| **Phase 6** | 2026.02 ~ 03 | Ground Truth Generation & Supervised Learning |

---

## Phase 1 · 2025.09 — Genesis & Robot Simulation Fundamentals

| Date | Topic | Link | Highlight✨ |
|:-----|:------|:-----|:----------|
| 09.10 | Genesis 시뮬레이터 설치 및 예제 실행 | [Genesis 환경 구축 가이드](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0910_genesis%20%EC%83%98%ED%94%8C%20%EC%8B%A4%ED%96%89%20%EB%B3%B4%EA%B3%A0%EC%84%9C.md) | Genesis AI 설치 Guide Line이 잘 정리되어 있음 |
| 09.16 | Go2 로봇 PPO 학습 코드 흐름 및 신경망 구조 분석 | [PPO 학습 코드 분석](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0916_train%EC%BD%94%EB%93%9C%20%EB%B6%84%EC%84%9D%20%EB%B0%8F%20%ED%95%99%EC%8A%B5%20%EA%B5%AC%EC%A1%B0%20%ED%8C%8C%EC%95%85.md) | |
| 09.18 | 외부 시뮬레이터 조사: CARLA 자율주행 환경 분석 | [CARLA 환경 조사](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0918_%EC%99%B8%EB%B6%80%20%EC%9E%90%EB%8F%99%EC%B0%A8%20%EB%AC%BC%EB%A6%AC%20%EC%97%94%EC%A7%84%20%EC%A1%B0%EC%82%AC.md) | |
| 09.22 | Go2 백플립 동작 생성 파이프라인 정리 | [Backflip 동작 흐름 분석](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0922_backflip%EB%B3%B4%EA%B3%A0%EC%84%9C.md) | |
| 09.22 | Genesis 물리 엔진 기반 간단한 toy car sample 만들어보기 | [자동차 시뮬레이션 기초 실험](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0922_car_simulate%EB%B3%B4%EA%B3%A0%EC%84%9C.md) | |
| 09.25 | Go2 백플립 환경의 좌표계·URDF·센서 구조 분석 | [URDF 및 좌표계 분석](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0925_backflip_URDF.md) | Genesis 예제 중 하나인 Backflip의 환경(좌표계, 중력 방향 등)과 Go2 Robot URDF를 상세히 분석 |
| 09.30 | 보행 학습에서 step/rollout/iteration 등 용어 정리 | [강화학습 용어정리](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0930_walking_train.md) | 처음 접하면 난해하게 느껴지는 RL 용어들을 이해하기 쉽게 정리 |

---

## Phase 2 · 2025.10 — Reinforcement Learning Scaling & Performance

| Date | Topic | Link | Highlight✨ |
|:-----|:------|:-----|:----------|
| 10.14 | Rollout 및 Mini-batch 기준 GPU 메모리 사용량 계산 | [메모리 분석 보고서](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1014_backflip_data_size_report.md) | |
| 10.16 | 다중 ckpt 로봇 동시 관찰 및 GPU 이슈 해결 | [다중 로봇 성능 이슈](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1016_walk_report.md) | |

---

## Phase 3 · 2025.11 — Vehicle Simulation & Data Collection

| Date | Topic | Link | Highlight✨ |
|:-----|:------|:-----|:----------|
| 11.03 | Blender 지형 기반 차량 주행 및 CSV 데이터 수집 | [Blender 데이터 수집](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1103_blender_car_data.md) | Blender에서 차량을 주행해보며 최초로 Data를 추출 |
| 11.18 | URDF 무게중심·관성·충돌 박스 조정으로 주행 안정화 | [물리 파라미터 튜닝](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1118_Running%20a%20car%20in%20the%20Genesis%20environment.md) | |
| 11.21 | 직진 주행 데이터 기반 MLP 차량 제어 실험 | [Straight Driving MLP](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1121_Genesis_Straight_train_MLP.md) | 매우 간단한 움직임에 대해 MLP를 정의해 Blender→Genesis를 최초로 시도 |
| 11.24 | 조향 포함 주행 데이터 학습 및 회전 동작 재현 | [Steer 포함 학습 실험](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1124_train_car_including_steer.md) | |

---

> **Note** · Phase 3 ~ Phase 4 (11.24 ~ 12.17)
>
> 이 시기의 연구는 Blender 차량의 **속도 모사를 무시**하고 **경로 추종에 대해서만** 진행하였으며,
> 파이프라인이 아직 확립되지 않은 탐색 단계였습니다.

---

## Phase 4 · 2025.12 — Neural Network-Based Vehicle Control *(탐색 단계)*

> 1개의 MLP만으로 Blender→Genesis 직접 제어를 시도하던 시기입니다.

| Date | Topic | Link | Highlight✨ |
|:-----|:------|:-----|:----------|
| 12.17 | 바퀴별 데이터 → Genesis 제어 인터페이스 통합 | [NN Steering & Throttle 제어](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1217_Neural%20Network%E2%80%93Based%20Steering%20and%20Throttle%20Control%20for%20a%20Vehicle%20in%20Genesis.md) | |
| 12.26 | 24가지 data 기반 MLP 학습 및 시뮬레이션 | [MLP 구조 및 제어 파이프라인](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1226_MLP_Architecture_and_Training.md) | |
| 12.26 | 전체 학습 시스템 파이프라인 및 결과 정리 | [System Workflow 정리](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1226_System_Workflow.md) | |

---

> **Turning Point** · 2026.01.19 교수님 미팅
>
> 기존의 "1개 MLP로 직접 Sim2Sim" 접근을 폐기하고,  
> **Ground Truth 생성 → 지도학습** 파이프라인으로 전면 변경.  
> 목표: Blender의 raw 제어만으로도 Genesis에서 동일 움직임을 재현하는 MLP 구축.

---

## Phase 5 · 2026.01 — Revisiting Control Data Extraction Pipelines *(전환기)*

> 1개 움직임에 대한 overfitting을 시작으로, 파이프라인 재설계를 모색하던 시기입니다.

| Date | Topic | Link | Highlight✨ |
|:-----|:------|:-----|:----------|
| 01.06 | Blender data 추출 방식 재점검 및 MLP 학습 파이프라인 | [Blender→Genesis 시뮬레이션](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0106_Control%20Signal%20Extraction%20from%20Blender%20for%20Reliable%20Genesis%20Vehicle%20Simulation.md) | |
| 01.16 | 현재까지 진행한 프로젝트 전체 파이프라인 | [중간점검 report (PDF)](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0116_%EA%B0%95%EB%8F%99%EC%9A%B1_report.pdf) | |
| 01.18 | 보상 함수 개선 및 재학습 | [보상 함수 최적화](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0118_Optimization%20of%20PPO-based%20Autonomous%20Driving%20Control%20via%20Reward%20Function%20Engineering.md) | |

---

> **Trial & Error** · 2026.01.18 ~ 02.18
>
> Ground Truth를 얻기 위해 강화학습, MPC기반 등의 최적화를 시도하였으나, loss term 간 coupling 충돌,  
> 고속 구간 발산 등의 문제로 실패. 이 과정은 아래 PDF에 요약되어 있습니다.
>
> [Ground Truth 시행착오 🔍 (PDF)](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0317_Trial%20and%20Error%20about%20Ground%20Truth.pdf)

---

## Phase 6 · 2026.02 ~ 03 — Ground Truth Generation & Supervised Learning

| Date | Topic | Link | Highlight✨ |
|:-----|:------|:-----|:----------|
| 02.08 | MPC를 활용한 Ground Truth 시도 1 *(실패)* | [Sim2Sim Control 최적화](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0208_Sim2Sim%20Control%20Optimization%20Report.md) | |
| 02.15 | MPC를 활용한 Ground Truth 시도 2 *(실패)* | [MPC 최적화 & Divergence](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0215_MPC%20Optimization%20Progress%20and%20Divergence%20Handling%20Strategy.md) | |
| 02.18 | Sweep + Feedback 제어 방식 시도 | [Sweep Feedback 접근](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0218_sweep_feedback_approach.md) | MPC 폐기 후 Sweep Table + PD Feedback 방식으로 전환한 전환점 |
| 02.21 | Ground Truth → MLP 최초 지도학습 시도 | [Input Mapper 설계](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0221_supervised%20learning.md) | 현재 기준으로는 다소 부정확한 GT Data였으나, 지도학습을 최초로 시도 |
| 02.27 | 1개 움직임에 대한 파이프라인 완성 | [1개 움직임 학습 과정](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0227_pipeline%20update_residual%20RL.md) | |
| 02.28 | MLP 성능 검증 — 10가지 움직임 통합 학습 | [Sim2Sim 결과 정리](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0228_varius_data_learning.md) | 10가지 움직임에 대해 평균 거리 오차 0.05m의 GT 달성. GT뿐만 아니라 MLP Sim2Sim 출력 결과까지 모두 포함 |
