# System State Sheet — Sim2Sim Control Pipeline

---

## Stage 1: Sweep Test (a, k Matching)

말씀하신 바와 같이 **a, k matching** 단계입니다.

```
f(T, S ; v) → (a, k)
```

동일한 T, S를 입력해도 v가 다르면 a, k가 달라지기 때문에, **v를 mapping을 결정짓는 system state로 사용**하였습니다.

v 외에도 a, k를 결정짓는 다른 state가 분명 존재합니다. 다만 아래 두 가지 이유로 Stage 1에서는 v만 간단하게 state로 정의하였습니다.

1. a, k를 정확히 맞춰도 dynamic model에서는 경로가 조금 달라질 수 있음
2. Stage 1의 목적은 a, k를 대략적으로만 맞춰두고 경로를 얼추 따라가게 만드는 것 (Stage 2를 위한 기초 발판)

---

## Stage 2: PD Feedback Control (Trajectory Matching)

Stage 1에서 대략적으로만 따라가게 만든 상태에서, 추가적인 system state를 정의하여 궤적을 보정합니다.

### Loss로 사용한 State

| State | 기호 | 설명 | 적용 제어 |
|-------|------|------|----------|
| 종방향 속도 | v | 차량 전방 방향 속도 (m/s) | throttle 보정 (P 제어) |
| 요각 | yaw | 차량 heading 각도 (rad) | steer 보정 (PD 제어) |
| 횡방향 위치 오차 | ct | 목표 경로로부터의 수직 이탈 거리 (m) | steer 보정 (PD 제어) |

**제어 수식:**

```
throttle = ff(v, a_target)  −  kp_v · (v_gen − v_target)

steer    = ff(v, k_target)  −  kp_yaw · e_yaw  −  kd_yaw · ė_yaw
                             −  kp_ct  · e_ct   −  kd_ct  · ė_ct
```

---

### Loss로 사용하지 않은 State

| State | 기호 | 설명 |
|-------|------|------|
| 횡방향 속도 | v_lat | 차량 측면 방향 속도 (m/s) |

**v_lat을 loss로 정의하지 않은 이유:**

1. 서로 다른 물리 엔진 환경에서 제어 입력(throttle, steer)으로 v_lat을 직접 조종하는 것이 불가능
2. v_lat의 영향(경로 이탈)은 위에서 정의한 loss(yaw, ct)로 간접적으로 잡아낼 수 있음

---

## 요약

| Stage | 목적 | System State | Loss 사용 여부 |
|-------|------|-------------|---------------|
| Stage 1 | a, k matching (coarse) | v | — |
| Stage 2 | trajectory matching (fine) | v, yaw, ct | v, yaw, ct ✓ |
| Stage 2 | trajectory matching (fine) | v_lat | — (간접 보정) |
