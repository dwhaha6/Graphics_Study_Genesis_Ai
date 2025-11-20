## 1. Blender에서 직진하는 차량에 대한 Data 뽑아내기
https://github.com/user-attachments/assets/656b3974-f634-4cd3-a30a-9de3d9257279
- Data를 뽑아낼 Blender 차량 (직진)

```python
ROT_B2G = Matrix.Rotation(math.radians(90.0), 3, 'Z')  # Blender→Genesis 회전

def vec_B_to_G(v_b: Vector) -> Vector:
    """Blender 벡터 → Genesis 좌표계로 회전"""
    return ROT_B2G @ v_b


def mat3_B_to_G(R_b: Matrix) -> Matrix:
    """Blender 3x3 회전행렬 → Genesis 회전행렬"""
    return ROT_B2G @ R_b


def quat_B_to_G(q_b: Quaternion) -> Quaternion:
    """Blender 쿼터니언 → Genesis 쿼터니언"""
    R_b = q_b.to_matrix()
    R_g = mat3_B_to_G(R_b)
    return R_g.to_quaternion().normalized()
```
- 블렌더는 -Y축 전진, Genesis는 +X축 전진이므로 Z축에 대해 90도 회전
```text
( x )     ( 0 -1  0 )(x)
( y )  =  ( 1  0  0 )(y)
( z )     ( 0  0  1 )(z)

x_G = -y_B
y_G =  x_B
z_G =  z_B
```
- 코드 맨 첫줄에 나왔던 행렬의 형태

#### vec_B_to_G()
- 위치벡터, 속도벡터, 각속도벡터 등을 Genesis 좌표 기준으로 회전시키는 함수

#### mat3_B_to_G()
- Blender의 회전 행렬을 Genesis의 회전행렬도 바꾸는 함수

#### quat_B_to_G()
- 이전에 배웠던 것처럼 쿼터니언을 사용해야 변환(보간, 좌표계 변환)이 쉽고 안정적임
- 따라서 함수 내부 구현은 다음과 같이 이루어짐
    1. Blender quaternion → 3×3 회전행렬로 변환
    2. 그 회전행렬에 ROT_B2G 곱해서 좌표계 변환
    3. 다시 회전행렬 → quaternion

#### 선속도는 현재 위치 - 이전 위치의 차이를 이용해 구함
    vel = (curr_loc - prev_loc) / dt
#### 각속도 구하기
    prev_rot = Quaternion(prev_rot)
    curr_rot = obj.matrix_world.to_quaternion()
- q1,q2(현재의 쿼터니언, 이전의 쿼터니언 가져오기)
```
delta = prev_rot.conjugated() @ curr_rot
```
- 두 쿼터니언의 차이 구하기 ->Δq (상대회전)
```
angle = delta.angle
axis = delta.axis
ang_vel = axis * (angle / dt)
```
- 각도와 축을 뽑은 후 차이 각을 dt로 나눈 값에 축 방향을 곱해서 최종 각속도 벡터 얻기
```math
\Delta q = q^{-1}_{\text{prev}} \otimes q_{\text{curr}}
```
- 쿼터니언의 차이를 구하는 식(뺄셈이 아니라 곱셈)

## 뽑아낸 데이터로 MLP 만들고 Pytorch로 학습시키기
### MLP 구조
![](./이미지/MLP.png)
#### 1. Linear(3,64)
- weight: 3 × 64 = 192
- bias: 64
- 합: 192 + 64 = 256
#### 2. Linear(64, 64)
- weight: 64 × 64 = 4096
- bias: 64
- 합: 4096 + 64 = 4160
#### 3. 3층: Linear(64, 2)
- weight: 64 × 2 = 128
- bias: 2
- 합: 128 + 2 = 130
#### 4. 총 파라미터 수
- 총합 = 256 + 4160 + 130 = 4,546개
### Input (state) – NN이 보는 정보
```python
s_t = [g_lin_vx, g_lin_vy, g_lin_vz]
```
- x,y,z축에 대한 선속도(3차원 vector)

### Output(action) - NN이 내보내는 컨트롤
```python
a_t = [steer_cmd, throttle_cmd]
(조향각, 정규화된 스로틀)
```
- steer_cmd → 앞바퀴 조향 DOF position target
- 뒷바퀴 토크 = throttle_cmd * max_wheel_torque
    - max_torque값은 코드 실행시 고정값
    - throttle_cmd 값은 아래의 공식에 따라 -1~1 사이의 값으로 세팅
```python
throttle_cmd = normalize(mean(spin_RL, spin_RR) / ω_max)  # [-1, 1]
```
- spin: 각속도(rad/s) -> 바퀴가 얼마나 빨리 도는가
-  mean(spin_RL, spin_RR): 좌우 뒷바퀴의 평균 회전 속도
- w_max: 최대 회전속도
- rear_spin / ω_max: 현재 회전 속도가 최대 회전 속도의 몇배인가
- normalize: 값이 너무 커지지 않게 -1~1사이의 값으로 매핑
```
throttle_cmd = -1 → 강한 역방향 (브레이크 또는 리버스)

throttle_cmd = 0 → 스로틀 0

throttle_cmd = +1 → 최대 스로틀
```
## 학습 완료된 차량 주행
https://github.com/user-attachments/assets/93038e86-8a81-4a5d-8d9b-27c4f0e0436f
- 정답 데이터에 따라 무난하게 주행하는 모습
### 초반에 조향이 틀어졌다가 서서히 직진 조향으로 바뀌는 이유?
- 학습에 사용된 CSV 데이터는 대부분 차량이 이미 움직이고 있는 구간에서 추출
- 따라서 모델은 정지 상태(velocity = 0, spin = 0)에 해당하는 입력을 학습하지 못 한 것으로 보임

- Genesis 실행 시 첫 프레임의 차량 상태는:
```math
s_0 = (v_x, v_y, v_z) = (0, 0, 0)
```
- 이는 학습 데이터 분포에서 벗어난 Out-of-Distribution(OOD) 상태
    - 따라서 초기 1초 남짓한 시간 동안 조향/가속 제어가 불안정했던 것으로 보임
- 현재는 간단한 모델이기에 주행에 별 문제는 없었으나 이후 더 복잡한 MLP를 구축할 땐 위 내용을 고려할 필요가 있음
