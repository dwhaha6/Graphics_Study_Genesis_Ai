# 📘 Genesis AI Research History
> **Blender to Genesis: High-Fidelity Sim2Sim Pipeline for Autonomous Vehicle Control**

[![Tech Stack](https://img.shields.io/badge/Genesis_AI-Physics_Simulation-blue)](#)
[![Tech Stack](https://img.shields.io/badge/Reinforcement_Learning-PPO_/_MPC-green)](#)
[![Tech Stack](https://img.shields.io/badge/Framework-PyTorch_/_Blender-orange)](#)

**Genesis AI 기반 물리 시뮬레이션 및 제어 최적화** 연구 기록입니다. 데이터 파이프라인 구축과 Sim2Sim 오차 극복 과정에 집중했습니다.

---

## 🚀 Core Competencies (핵심 역량)
* **Physics Simulation:** Genesis AI 기반의 로봇(Go2) 및 차량 물리 엔진 최적화
* **Sim2Sim Transfer:** Blender의 제어 신호를 물리 시뮬레이션 환경(Genesis)으로 전이하는 파이프라인 구축
* **Control Optimization:** PPO, MPC, Sweep + Feedback 제어를 통한 주행 안정성 확보 (평균 거리 오차 0.05m 달성)
* **Problem Solving:** 시행착오 분석을 통한 Ground Truth 생성 로직 재설계 경험

---

## 🗓 Project Roadmap
| Phase | Focus | Key Achievement |
|:---|:---|:---|
| **Phase 1~2** | **Fundamentals** | Genesis 환경 구축 및 로봇(Go2) PPO 학습 구조 분석 |
| **Phase 3~4** | **Exploration** | Blender-Genesis 연동 및 MLP 기반 직접 제어 시도 |
| **Phase 5~6** | **Optimization** | **[Current]** GT 생성 파이프라인 혁신 및 지도학습 성공 |

---

## 🏆 Highlight: Sim2Sim Result
> **[시연 결과 보고서 바로가기 🚗](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0228_varius_data_learning.md)**
> *10가지 복합 움직임에 대해 평균 거리 오차 0.05m의 Ground Truth 달성 및 검증 완료*

---

## 🔍 Research Timeline & Reports

### Phase 6: Ground Truth Generation (2026.02 ~ Present)
*가장 기술적 완성도가 높은 단계로, 시행착오를 통해 독자적인 제어 방식을 구축했습니다.*

| Date | Topic | Deliverables | Key Point |
|:---|:---|:---:|:---|
| 03.17 | **Ground Truth 시행착오 분석** | [📑 Report](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0317_Trial%20and%20Error%20about%20Ground%20Truth.pdf) | **Best Practice** |
| 02.28 | 10가지 움직임 통합 학습 결과 | [📑 Report](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0228_varius_data_learning.md) | 오차 0.05m 달성 |
| 02.18 | Sweep + Feedback 제어 전환 | [📑 Report](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0218_sweep_feedback_approach.md) | MPC 한계 극복 |

<details>
<summary><b>이전 단계(Phase 1~5) 기록 보기 (클릭)</b></summary>

#### Phase 5: Pipeline Revision (2026.01)
* [중간점검 전체 리포트 (PDF)](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0116_%EA%B0%95%EB%8F%99%EC%9A%B1_report.pdf)
* [PPO 기반 보상 함수 최적화](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0118_Optimization%20of%20PPO-based%20Autonomous%20Driving%20Control%20via%20Reward%20Function%20Engineering.md)

#### Phase 1~4: Early Exploration (2025.09 ~ 2025.12)
* [Genesis 환경 구축 가이드](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0910_genesis%20%EC%83%98%ED%94%8C%20%EC%8B%A4%ED%96%89%20%EB%B3%B4%EA%B3%A0%EC%84%9C.md)
* [Blender 데이터 수집 및 물리 파라미터 튜닝](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1118_Running%20a%20car%20in%20the%20Genesis%20environment.md)
</details>

---

## 💡 Engineering Insight: "Turning Point"
**"기존의 직접 Sim2Sim 접근법을 왜 폐기했는가?"**
1개 MLP로 직접 제어 시 발생하는 고속 구간의 발산 문제와 오버피팅을 해결하기 위해, **'Ground Truth 생성 후 지도학습'**이라는 더 견고한 아키텍처로 선회했습니다. 이 과정에서의 실패 기록은 저의 가장 큰 자산입니다.
> [Trial & Error 상세 분석 보고서](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0317_Trial%20and%20Error%20about%20Ground%20Truth.pdf)
