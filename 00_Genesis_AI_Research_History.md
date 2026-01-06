# Genesis AI Research History

Genesis 물리 시뮬레이터를 기반으로  
로봇 제어, 강화학습 구조 분석, 자동차 시뮬레이션 및 데이터 기반 제어까지  
단계적으로 확장해 온 개인 연구 기록

---

## Project Progress

### 주요 마일스톤
- **9월**: 드론·로봇 예제 시뮬레이션 분석 (URDF, 물리 엔진, 제어 구조 이해)
- **10월**: 강화학습(PPO) 구조 분석 및 메모리·GPU 사용량 정량화
- **11월**: Blender–Genesis 연동을 통한 자동차 데이터 수집 및 물리 안정화
- **12월**: 데이터 통합 및 NN 기반 차량 제어 구조 개선 (진행 중)

---

## 2025.09 — Genesis & Robot Simulation Fundamentals

- **Genesis 시뮬레이터 설치 및 예제 실행 기록**  
  → [Genesis 샘플 실행 및 문제 해결 정리](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0910_genesis%20%EC%83%98%ED%94%8C%20%EC%8B%A4%ED%96%89%20%EB%B3%B4%EA%B3%A0%EC%84%9C.md)

- **드론 위치·고도 추종 안정성 분석 (그래프 기반)**  
  → [드론 ckpt 동작 그래프 분석](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0916_ckpt%20%EA%B7%B8%EB%9E%98%ED%94%84%20%EC%84%A4%EB%AA%85.md)

- **Go2 로봇 PPO 학습 코드 흐름 및 신경망 구조 분석**  
  → [PPO 학습 코드 및 보상 구조 정리](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0916_train%EC%BD%94%EB%93%9C%20%EB%B6%84%EC%84%9D%20%EB%B0%8F%20%ED%95%99%EC%8A%B5%20%EA%B5%AC%EC%A1%B0%20%ED%8C%8C%EC%95%85.md)

- **Go2 백플립 동작 생성 파이프라인 정리 (입력→출력→PD 제어)**  
  → [Backflip 동작 생성 흐름 분석](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0922_backflip%EB%B3%B4%EA%B3%A0%EC%84%9C.md)

- **외부 시뮬레이터 조사: CARLA 자율주행 환경 분석**  
  → [CARLA 환경 및 센서 구성 조사](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0918_%EC%99%B8%EB%B6%80%20%EC%9E%90%EB%8F%99%EC%B0%A8%20%EB%AC%BC%EB%A6%AC%20%EC%97%94%EC%A7%84%20%EC%A1%B0%EC%82%AC.md)

- **Genesis 물리 엔진 기반 자동차 시뮬레이션 초기 실험**  
  → [자동차 시뮬레이션 기초 실험 기록](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0922_car_simulate%EB%B3%B4%EA%B3%A0%EC%84%9C.md)

- **Go2 백플립 환경의 좌표계·URDF·센서 구조 분석**  
  → [Backflip URDF 및 좌표계 대응 분석](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0925_backflip_URDF.md)

- **보행 학습에서 step / rollout / iteration 데이터 흐름 정리**  
  → [Walking 학습 데이터 구조 설명](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0930_walking_train.md)

---

## 2025.10 — Reinforcement Learning Scaling & Performance

- **Rollout 및 Mini-batch 기준 GPU 메모리 사용량 계산**  
  → [Backflip 학습 데이터 크기 및 메모리 분석](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1014_backflip_data_size_report.md)

- **다중 ckpt 로봇 동시 관찰 및 GPU 이슈 해결 시도**  
  → [다중 로봇 실행 및 성능 이슈 정리](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1016_walk_report.md)

---

## 2025.11 — Vehicle Simulation & Data Collection

- **Blender 지형 기반 차량 주행 및 CSV 데이터 수집**  
  → [Blender 차량 데이터 수집 파이프라인](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1103_blender_car_data.md)

- **URDF 무게중심·관성·충돌 박스 조정으로 주행 안정화**  
  → [Genesis 차량 물리 파라미터 튜닝 기록](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1118_Running%20a%20car%20in%20the%20Genesis%20environment.md)

- **직진 주행 데이터 기반 MLP 차량 제어 실험 (Steer 제외)**  
  → [Straight Driving MLP 학습 실험](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1121_Genesis_Straight_train_MLP.md)

- **조향 포함 주행 데이터 학습 및 회전 동작 재현**  
  → [Steer 포함 차량 학습 실험](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1124_train_car_including_steer.md)

---

## 2025.12 — Neural Network–Based Vehicle Control (Ongoing)

- **바퀴별 데이터 → Genesis 제어 인터페이스 통합 및 학습 구조 개선**  
  → [NN 기반 Steering & Throttle 제어 구조 개선](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1217_Neural%20Network%E2%80%93Based%20Steering%20and%20Throttle%20Control%20for%20a%20Vehicle%20in%20Genesis.md)
- **24가지 data 기반으로 MLP 학습 진행 후 Genesis에서 시뮬레이션**  
  -> [MLP구조 및 조향,토크,브레이크 제어 파이프라인 정리](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1226_MLP_Architecture_and_Training.md)  
  -> [전체적인 학습 시스템 파이프라인 및 학습결과 정리](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1226_System_Workflow.md)
---
## 2026.01 - Revisiting Control Data Extraction Pipelines for Blender-to-Genesis Vehicle Transfer

- **Blender data 추출 방식 재점검 및 MLP 학습 파이프라인**
   
-> [Blender raw data를 이용한 Genesis 시뮬레이션](https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2026_0106_Control%20Signal%20Extraction%20from%20Blender%20for%20Reliable%20Genesis%20Vehicle%20Simulation.md)
