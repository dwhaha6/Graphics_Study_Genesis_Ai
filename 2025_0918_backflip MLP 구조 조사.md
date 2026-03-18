# 모션 캡처 기반 학습
- 실제 사람/로봇의 백플립 동작을 캡처한 애니메이션 데이터를 레퍼런스로 삼는 방식
- 보상 함수에 "현재 관절 상태 vs 레퍼런스 포즈" 를 넣어서 레퍼런스를 따라 하도록 학습
- DeepMind, Berkeley 등에서 쓰는 모션 클리핑 데이터셋이 대표적
- 백플립의 경우 원본 애니메이션 파일이 프로젝트 안에 없음
# 강화학습 기반 자기 생성
## 보상
```python
# 정의된 보상을 계산하는 함수들
# 목표한 선속도(x,y)와 실제 선속도의 차이를 줄일수록 보상
def _reward_tracking_lin_vel(self):
    # (목표 속도 명령 - 실제 몸통 선속도)를 계산후 제곱한 값을 lin_vel_error에 대입
        lin_vel_error = torch.sum(torch.square(self.commands[:, :2] - self.base_lin_vel[:, :2]), dim=1)
        # 오차가 작을 수록 1로 오차가 클수록 0에 가까워짐, 즉 오차가 작을 수록 보상이 커짐
        return torch.exp(-lin_vel_error / self.reward_cfg["tracking_sigma"])
# 목표 각속도(회전속도)와 실제 각속도의 차이를 줄이면 보상
    def _reward_tracking_ang_vel(self):
        # (목표 각속도 - 실제 각속도)의 의 제곱을 ang_vel_error에 대입
        ang_vel_error = torch.square(self.commands[:, 2] - self.base_ang_vel[:, 2])
        # 해당 값이 작을 수록 보상 큼
        return torch.exp(-ang_vel_error / self.reward_cfg["tracking_sigma"])
# 몸통이 위/아래로 튀는 속도(z축 선속도)를 최소화 시키기
    def _reward_lin_vel_z(self):
        # z축 속도의 제곱을 계산 후 그 값이 크면 차후 음수 가중치를 곱해 패널티 부여
        return torch.square(self.base_lin_vel[:, 2])
# 연속된 스텝에서 action이 크게 변하지 않도록 하는 함수
    def _reward_action_rate(self):
        # (현재 액션 - 지난 액션)의 제곱을 계산 이것도 마찬가지로 차후 음수 가중치로 부여
        return torch.sum(torch.square(self.last_actions - self.actions), dim=1)
# 기본 자세(default pose)에서 너무 벗어나지 않도록 하는 함수
    def _reward_similar_to_default(self):
        # (현재 관절각 - 기본 관절각)의 절댓값을 합산, 마찬가지로 클수록 패널티
        return torch.sum(torch.abs(self.dof_pos - self.default_dof_pos), dim=1)
# 몸통의 높이가 목표 높이에서 벗어나지 않게 하는 함수
    def _reward_base_height(self):
        # (현재 base z좌표 - 목표 높이)의 제곱 계산 후 클수록 패널티
        return torch.square(self.base_pos[:, 2] - self.reward_cfg["base_height_target"])
```

```python
# 각 보상 함수에서 리턴된 값에 정해진 가중치를 곱해 합산하여 최종 보상이 결정되는 구조(크면 좋지 않은 값들에는 음수 가중치가 부여됐음을 알 수 있음)
total_reward = (
    +1.0 * _reward_tracking_lin_vel() +
    +0.2 * _reward_tracking_ang_vel() +
    -1.0 * _reward_lin_vel_z() +
    -0.005 * _reward_action_rate() +
    -0.1 * _reward_similar_to_default() +
    -50.0 * _reward_base_height()
)
```
- 시뮬레이터는 매 타임스탭(step())에서 환경 상태를 갱신하고, 위에서 말한 각 보상함수들을 호출, 그 결과 합산된 total_reward 값이 나옴
- 이 total_reward 값은 단순 점수가 아니라 강화학습 알고리즘의 입력 신호로 쓰임
## 강화학습의 전반적인 루프
1. PPO(Proximal Policy Optimization) 네트워크가 현재 상태(obs)를 입력받아 현재 로봇의 action을 출력
2. 그 action을 시뮬레이터에 적용 -> 로봇이 움직임
3. 시뮬레이터는 새로운 상태(new_obs)와 함께 total_reward를 리턴
4. 알고리즘은 (obs,action,reward,next_obs) 튜플을 기록하고, 나중에 이 trajectory들을 모아 정책 파라미터를 업데이트 함
## 그래서 이 reward가 정확히 어떻게 신경망에 적용되는가
1. πθ​(a∣s)
    - s: 현재 상태 (예: 속도, 자세, 관절각)
    - a: 행동 (예: 모터 토크 값)
    - θ: 신경망의 가중치
- 즉 이 상태에서 행동A는 30%, 행동 B는 70% 이런식으로 분포를 뽑애냄
2. At​=Rt​+γV(st+1​)−V(st​)
    - At는 행동을 통해 들어온 보상을 누적하거나 보정해서 "이 행동이 얼마나 좋은가"를 계산한 것
    - ex) 앞으로 잘 걸으면 +1, 쓰러지면 -1
    - Rt: 즉시 보상(total_reward)
    - V(s): 현재 상태에서의 기대 보상
    - 𝛾: 미래 보상을 얼마나 고려할지
- 결론: At가 0보다 크면 좋은 행동, A가 작거나 음수면 나쁜행동이 됨
3. L(θ)=−Et​[logπθ​(at​∣st​)⋅At​]
- logπθ​(at​∣st​): 실제로 선택한 행동의 확률 로그 값
- A: 그 행동이 얼마나 좋은지(위에서 구한거)
- 즉 해당 행동이 얼마나 좋은지를 고려해 정책을 업데이트 하는 것
4. 작동 메커니즘
- L은 손실을 의미 즉 이를 최소화 시키는 것이 목표
    - At > 0이면, L을 줄이기 위해 log 값이 커짐 즉 그 행동의 확률이 올라감
    - At < 0이면, L을 줄이기 위해 반대로 log 값이 작아짐 즉 그 행동의 확률이 줄어듦
5. PPO에서는 위 정책에서 안정성을 더한 버전
PPO의 목적함수는 $L^{\mathrm{PPO}}(\theta)=\mathbb{E}_t[\min(r_t(\theta)A_t,\;\mathrm{clip}(r_t(\theta),1-\epsilon,1+\epsilon)A_t)]$ 


- 행동 확률이 너무 급격히 바뀌지 않도록 클리핑을 넣음

## 그래서 정답(기준)이 되는 값들은 어디에 정의가 됐는가?
- train.py 초기에 정의되어 있음
### 목표 속도(commands)
``` python
command_cfg = {
    "num_commands": 3,
    "lin_vel_x_range": [0.5, 0.5],   # 목표: x축 속도 0.5 m/s
    "lin_vel_y_range": [0, 0],       # 목표: y축 속도 0
    "ang_vel_range": [0, 0],         # 목표: yaw 각속도 0
}

```
- 정답: 앞으로 0.5m/s 직진, 옆, 회전은 0
### 목표 높이
```python
reward_cfg = {
    "base_height_target": 0.3,   # 목표 몸통 높이 (m)
}

```
- 정답: 몸통 높이 0.3m 유지
### 목표 관절 위치
```python
"default_joint_angles": {
    "FL_thigh_joint": 0.8,
    "FR_thigh_joint": 0.8,
    "RL_thigh_joint": 1.0,
    "RR_thigh_joint": 1.0,
    "FL_calf_joint": -1.5,
    "FR_calf_joint": -1.5,
    "RL_calf_joint": -1.5,
    "RR_calf_joint": -1.5,
    ...
}
```
- 정답: 관절들이 위 값 근처에 위치하도록 유지
### + 액션 변화 줄이기(정답이 동적으로 변함)
```python
torch.sum(torch.square(self.last_actions - self.actions), dim=1)
```
- 정답 값: 이전 행동과 크게 다르지 않은 부드러운 움직임

# 백플립 Go2 로봇의 움직임 원리(자세 제어)
- single.pt 내부 구조
    - 60(관측값)만큼의 입력을 넣어 7단계를 거쳐 최종 12개의 출력을 뽑아냄
    - 이 12개의 값 = 12개 관절에 줄 액션 명령
    - 이 12개의 각 값들이 그대로 env.step(actions)에 들어가서 다리 관절이 움직임
- 즉 애니메이션 데이터(궤적)이 직접적으로 들어가 있는게 아니라, 뉴럴넷 파라미터가 들어 있어서 "현재 상태 -> 다음 액션"을 계산하는 원리
## 관측값
- BackflipEnv.get_observations() 부분
``` python
self.obs_buf = torch.cat(
    [
        self.base_ang_vel * self.obs_scales["ang_vel"],   # 3
        self.projected_gravity,                           # 3
        (self.dof_pos - self.default_dof_pos) * self.obs_scales["dof_pos"], # 12
        self.dof_vel * self.obs_scales["dof_vel"],        # 12
        self.actions,                                     # 12
        self.last_actions,                                # 12
        torch.sin(phase),                                 # 1
        torch.cos(phase),                                 # 1
        torch.sin(phase / 2),                             # 1
        torch.cos(phase / 2),                             # 1
        torch.sin(phase / 4),                             # 1
        torch.cos(phase / 4),                             # 1
    ],
    axis=-1,
)
```
- 로봇 에이전트가 매 순간 자신의 상태를 숫자들로 묶어(벡터) 신경망에 넣기위해 여러 정보를 옆으로 이어붙이는 코드
1. 기본 동역학 상태
    - 몸통의 각속도, 중력 벡터가 로봇 좌표계에서 어떻게 보이는지
2. 관절 상태
    - 관절 위치 편차
    - 관절 속도
3. 액션 히스토리
    - 현재 액션
    - 직전 액션
4. 위상 인코딩
    - 시간 진행에 따라 주기적인 신호 제공(리듬감, 플립 타이밍 학습 가능)
- 즉 60개의 관측값은 로봇의 물리 상태(자세,속도,관절), 직전 액션 히스토리, 그리고 현재 동작이 몇 % 진행됐는지 나타내는 위상 정보
# 결론
- 이 샘플의 경우 관절 12개를 제어하는 것이 핵심, 드론의 경우 모터회전수에 따른 힘(추력), 위치/속도/자세를 제어하기 위한 물리식 풀기 등 더 복잡한 메커니즘이 있는 것으로 파악됨

# backflip 모델의 MLP 구조
1. Linear
2. ELU
3. Linear
4. ELU
5. Linear
6. ELU
7. Linear(출력층)
- 즉 4개의 Linear 층과 ELU 활성화 함수를 가진 깊이 7층짜리 MLP
## 파라미터 개수
- single.pt(1번 백플립) : 197,004개
- double.pt(2번 백플립) : 197,004개
## Linear 와 ELU
- Linear
    - y=Wx+b
    - 입력 벡터 x를 가중치 W,편향 b로 선형변환시켜 주는 층
- ELU
     - ELU(x)=x (x>=0)
     - ELU(x)=a(exp(x)-1)(x<0)
        - 보통 a = 1
        - 평균을 0 근처로 끌어주어 학습 안정성에 도움을 주는 비선형 변환층

## 층별 상세(입출력, 파라미터 계산)
1. Linear #1: in=60 → out=512
    - weight shape: (512, 60), bias: (512)
    - params=512 x 60 + 512 =31,232
2. ELU : 파라미터 0
3. Linear #2: in 512 -> out=256
    - weight: (256, 512), bias: (256)
    - params = 256 x 512 + 256 = 131,328
4. ELU #2 파라미터 0
5. Linear #3: in=256 → out=128
    - weight: (128,256), bias:(256)
    - params=128 x 256 + 128 = 32896
6. ELU #3: 파라미터 0
7. Linear #4 (출력층): in=128 → out=12
    = weight:(12,128), bias:(12)
    - params = 12 x 128 + 12 = 1548
### 총 파라미터 = 31232 + 131328 + 32896 + 1548 = 197004개
    - single.pt , double.pt 둘 다 파라미터 개수 동일



