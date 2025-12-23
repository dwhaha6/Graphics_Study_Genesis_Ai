# Genesis ai Research_History
# 2025_09
## 1. Genesis 시뮬레이터를 직접 설치하고 실행해 보면서 과정과 문제 해결 방법을 정리한 기록
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0910_genesis%20%EC%83%98%ED%94%8C%20%EC%8B%A4%ED%96%89%20%EB%B3%B4%EA%B3%A0%EC%84%9C.md
## 2. 드론이 명령한 높이·위치를 잘 따라가는지와 흔들림·충돌 없이 안정적으로 움직이는지를 그래프로 정리한 분석
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0916_ckpt%20%EA%B7%B8%EB%9E%98%ED%94%84%20%EC%84%A4%EB%AA%85.md
## 3. Go2 로봇이 PPO로 학습되는 전체 코드 흐름과 신경망 구조, 보상이 어떻게 행동을 만들지 정리한 설명
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0916_train%EC%BD%94%EB%93%9C%20%EB%B6%84%EC%84%9D%20%EB%B0%8F%20%ED%95%99%EC%8A%B5%20%EA%B5%AC%EC%A1%B0%20%ED%8C%8C%EC%95%85.md
## 4. Go2 백플립 로봇이 코드에서 어떤 순서로 움직임이 만들어지는지(입력 60 → 출력 12 → PD제어) 한 번에 정리한 문서
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0922_backflip%EB%B3%B4%EA%B3%A0%EC%84%9C.md
## 5. CARLA 시뮬레이터로 자율주행 환경과 센서를 어떻게 구성하고 실행하는지 정리한 노트 (외부 자동차 시뮬레이션 조사)
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0918_%EC%99%B8%EB%B6%80%20%EC%9E%90%EB%8F%99%EC%B0%A8%20%EB%AC%BC%EB%A6%AC%20%EC%97%94%EC%A7%84%20%EC%A1%B0%EC%82%AC.md
## 6. Genesis 물리 엔진으로 자동차 시뮬레이션을 처음으로 만들어보고, 왜 그렇게 움직이는지 하나씩 확인한 기록
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0922_car_simulate%EB%B3%B4%EA%B3%A0%EC%84%9C.md
## 7. Go2 백플립 환경에서 쓰이는 좌표계, URDF 구조, 관절·센서 설정이 실제 로봇과 어떻게 대응되는지 정리한 분석
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0925_backflip_URDF.md
## 8. Go2 로봇 보행 학습에서 step, rollout, iteration 같은 데이터 흐름을 이해하기 쉽게 정리한 문서
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_0930_walking_train.md
## 9. 한 Rollout과 Mini-batch 기준으로 강화학습 데이터가 얼마나 쌓이고 GPU 메모리를 얼마나 쓰는지 계산해본 정리
# 2025_10
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/edit/main/2025_1014_backflip_data_size_report.md
## 10. 하나의 환경에서 서로 다른 ckpt의 로봇들 담아 관찰하기 + GPU 이슈관련 해결방안 탐색
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1016_walk_report.md
# 2025_11
## 11. Blender 지형 위에서 자동차를 주행시키고 위치·자세·센서 데이터를 CSV로 뽑아내는 과정을 정리한 문서
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1103_blender_car_data.md
## 12. Genesis에서 자동차가 제대로 굴러가도록 URDF의 무게중심, 관성, 충돌 박스를 조정하며 주행 문제를 해결한 과정 정리
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1118_Running%20a%20car%20in%20the%20Genesis%20environment.md
## 13. Blender에서 수집한 직진 주행 데이터를 좌표계 변환 후 MLP로 학습해 Genesis 차량을 제어한 실험 기록(조향X, 직진만)
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1121_Genesis_Straight_train_MLP.md
## 14. 직진뿐 아니라 조향까지 포함한 주행 데이터를 학습해 Genesis 차량이 Blender의 회전 동작을 따라가도록 만든 실험 기록
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1124_train_car_including_steer.md
## 15. Blender에서 추출한 바퀴별 데이터를 Genesis의 steer·throttle 제어 방식에 맞게 통합하고 학습 구조를 개선한 기록(14에 대한 실험에한 피드백) 
# 2025_12
https://github.com/dwhaha6/Graphics_Study_Genesis_Ai/blob/main/2025_1217_Neural%20Network%E2%80%93Based%20Steering%20and%20Throttle%20Control%20for%20a%20Vehicle%20in%20Genesis.md
