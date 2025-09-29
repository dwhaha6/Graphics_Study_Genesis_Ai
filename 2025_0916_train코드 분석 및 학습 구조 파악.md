# 코드 이해 전 필요한 사전 지식
## PPO 알고리즘
### PPO 알고리즘이란?
- 상황을 주면 -> 로봇(에이전트)가 행동을 수행
- 그 행동이 잘했으면 보상(+), 못했으면 보상(-)를 부여
- 이 경험을 쌓아서 "앞으로 더 잘 행동하려면 정책(policy)을 어떻게 고쳐야 할까?"를 학습하는 방법
- 강화학습에서 주로 쓰이는 훈련법임
## AI 수학에서 배웠던 그래디언트 디센트와 무슨 관련이 있는가?
- PPO엔 뉴런망이 들어감
- 즉 똑같이 그래디언트(기울기)를 계산해서 가중치(파라미터)를 업데이트 함
- 이때, 러닝 레이트(learning rate)는 배웠다시피 "정책 신경망의 파라미터(가중치)를 얼마나 크게 고칠지"를 정하는 기준이 됨
    - 너무 크면 발산하며 학습이 망가짐
    - 너무 작으면 수렴하기까지 너무 오랜 시간이 걸림
## 알고리즘 관련 주요 용어 정리
### 정책(POLICY)이란?
- "상황이 주어졌을 때 어떤 행동을 할지 정하는 규칙(확률)"을 의미
    - 즉 로봇의 두뇌 역할을 함
- 예를들어 초기 상태의 로봇의 정책은 랜덤임(아무것도 학습이 되지 않았기 때문) 그러나 주어진 환경에 따라 적절한 보상을 받아가며 정책(신경망)이 업데이트가 되고 결과적으로 로봇은 환경이 원하던 행동을 할 확률이 높아지게 됨 
- 신경망 그 자체를 의미한다고 봐도 무방
### 클립 파라미터(clip_param)
- 정책이 업데이트 됨에 따라 로봇은 특정 행동을 출력하게 됨
- 이때 그 행동의 분포가 너무 크게 달라지지 않게 조절해주는 파라미터
- 0.2면 +- 20% 이상 바뀌지 않도록 조절
### gamma
- 현재의 보상뿐 아니라 앞으로의 보상을 얼마나 중요하게 생각하는지를 정하는 수
- gamma=1.0  ->  1초뒤의 보상도 현재 보상과 동일하게 간주
- gamma=0.5 -> 1초뒤의 보상은 현재 보상의 절반의 가치로 간주
### lam = 0.95
- 얼마나 오래 경험을 기억할까
- 이 행동이 얼마나 좋은가를 계산할 때 쓰이는 메모리 길이 조절기
- 0.95면 적당히 과거까지 끌고 오자
### entropy_coef
- 정책이 한쪽 행동에만 치우치면 새로운 전략은 배우지 못 함
- 랜덤성에 조금 점수를 줌으로써 로봇에게 탐험을 강제하는 역할
- 0.01 이면 약간의 랜덤성을 유지해 새로운 길도 가보도록 함
### learning_rate
- 학습의 속도를 결정하는 파라미터
- 신경망의 가중치를 결정함
### max_grade_norm
- 한 번에 고칠 수 있는 최대치 제한
- 가중치의 변화량이 갑자기 엄청 커질 떄 이를 잘라주는 안전장치
- 이게 없으면 업데이트가 폭주해 학습이 망가질 수 있음
### num_learning_epochs
- 한번 모은 데이터를 가지고 신경망을 업데이트 할 때 **몇 번 돌려서 학습할지**
- 너무 크면 과적합이, 너무 작으면 학습 부족이 될 수 있음
### num_mini_batches
- 위에서 말한 학습 데이터를 몇 덩어리로 쪼개서 학습할지
- 4면 데이터를 4개로 나눠서 조금씩 학습하게 되고 메모리 효율과 학습 안정성이 올라감



```python
import argparse
import os
import pickle
import shutil
from importlib import metadata
# try except 구문으로 버전 충돌 방지, rsl-rl 버전이 아닌 2.2.4버전으로 다운로드하도록 유도
try:
    try:
        if metadata.version("rsl-rl"):
            raise ImportError
    except metadata.PackageNotFoundError:
        if metadata.version("rsl-rl-lib") != "2.2.4":
            raise ImportError
except (metadata.PackageNotFoundError, ImportError) as e:
    raise ImportError("Please uninstall 'rsl_rl' and install 'rsl-rl-lib==2.2.4'.") from e


from rsl_rl.runners import OnPolicyRunner
# Genesis 엔진
import genesis as gs
# 보행환경
from go2_env import Go2Env


def get_train_cfg(exp_name, max_iterations):

    # 학습에 필요한 모든 설정을 하나의 딕셔너리로 묵어주는 함수
    
    train_cfg_dict = {
        # PPO 학습 관련 설정
        "algorithm": {
            "class_name": "PPO",
            "clip_param": 0.2,
            "desired_kl": 0.01,
            "entropy_coef": 0.01,
            "gamma": 0.99,
            "lam": 0.95,
            "learning_rate": 0.001,
            "max_grad_norm": 1.0,
            "num_learning_epochs": 5,
            "num_mini_batches": 4,
            "schedule": "adaptive",
            "use_clipped_value_loss": True,
            "value_loss_coef": 1.0,
        },
        
        "init_member_classes": {},
        "policy": {
            # 정책 네트워크 구조
            # Actor-Critic MLP 구조
            "activation": "elu",
            "actor_hidden_dims": [512, 256, 128],
            "critic_hidden_dims": [512, 256, 128],
            "init_noise_std": 1.0,
            "class_name": "ActorCritic",
        },
        
        "runner": {
            # 러닝 반복, 체크 포인트/로그 주기, 재시작 여부 등
            "checkpoint": -1,
            "experiment_name": exp_name,
            "load_run": -1,
            "log_interval": 1,
            "max_iterations": max_iterations,
            "record_interval": -1,  # 영상 기록 활성화 여부
            "resume": False, # 재개 여부
            "resume_path": None,
            "run_name": "",
        },
        # 공통적으로 적용되는 파라미터
        "runner_class_name": "OnPolicyRunner",
        "num_steps_per_env": 24, # 각 env에서 수집할 스텝 수
        "save_interval": 100, # 체크포인트 저장 간격
        "empirical_normalization": None,
        "seed": 1,
    }

    return train_cfg_dict


def get_cfgs():
    env_cfg = {  # 로봇의 기본 자세, 관절 초기값, 종료 조건 등 물리환경 파라미터
        "num_actions": 12,
        # 초기 관절 각도(라디안)
        "default_joint_angles": {  # [rad]
            "FL_hip_joint": 0.0,
            "FR_hip_joint": 0.0,
            "RL_hip_joint": 0.0,
            "RR_hip_joint": 0.0,
            "FL_thigh_joint": 0.8,
            "FR_thigh_joint": 0.8,
            "RL_thigh_joint": 1.0,
            "RR_thigh_joint": 1.0,
            "FL_calf_joint": -1.5,
            "FR_calf_joint": -1.5,
            "RL_calf_joint": -1.5,
            "RR_calf_joint": -1.5,
        },
        # 관절 명칭(행동,관측 정렬을 위해 중요)
        "joint_names": [
            "FR_hip_joint",
            "FR_thigh_joint",
            "FR_calf_joint",
            "FL_hip_joint",
            "FL_thigh_joint",
            "FL_calf_joint",
            "RR_hip_joint",
            "RR_thigh_joint",
            "RR_calf_joint",
            "RL_hip_joint",
            "RL_thigh_joint",
            "RL_calf_joint",
        ],
        # PD
        "kp": 20.0,
        "kd": 0.5,
        # 종료 조건
        "termination_if_roll_greater_than": 10,  # degree
        "termination_if_pitch_greater_than": 10,
        # 초기 몸통 자세
        "base_init_pos": [0.0, 0.0, 0.42],
        "base_init_quat": [1.0, 0.0, 0.0, 0.0],
        "episode_length_s": 20.0,
        "resampling_time_s": 4.0,
        "action_scale": 0.25,
        "simulate_action_latency": True,
        "clip_actions": 100.0,
    }
    obs_cfg = { # 관측값 개수(45개), 각 관측 신호 스케일
        "num_obs": 45,
        "obs_scales": {
            "lin_vel": 2.0,
            "ang_vel": 0.25,
            "dof_pos": 1.0,
            "dof_vel": 0.05,
        },
    }
    reward_cfg = { # 보상 함수 가중치 -> 잘 걷도록 유도
        "tracking_sigma": 0.25,
        # 목표 바디 높이, 발 높이
        "base_height_target": 0.3,
        "feet_height_target": 0.075,
        # 보상/페널티 스케일(가중치)
        "reward_scales": {
            "tracking_lin_vel": 1.0,
            "tracking_ang_vel": 0.2,
            "lin_vel_z": -1.0,
            "base_height": -50.0,
            "action_rate": -0.005,
            "similar_to_default": -0.1,
        },
    }
    command_cfg = { # 로봇에게 내릴 수 있는 명령 (x방향 속도는 0.5로 고정)
        "num_commands": 3,
        "lin_vel_x_range": [0.5, 0.5],
        "lin_vel_y_range": [0, 0],
        "ang_vel_range": [0, 0],
    }

    return env_cfg, obs_cfg, reward_cfg, command_cfg


def main():
    # 실행 시 인자 받기: 실험 이름, 환경 개수, 최대 반복 학습 횟수 등
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exp_name", type=str, default="go2-walking")
    parser.add_argument("-B", "--num_envs", type=int, default=4096)
    parser.add_argument("--max_iterations", type=int, default=101)
    args = parser.parse_args()

    # genesis 물리 엔진 초기화
    gs.init(logging_level="warning")

    # 실험 로그 저장용 폴더 생성
    log_dir = f"logs/{args.exp_name}"

    # 환경 설정 + 학습 설정 불러오기
    env_cfg, obs_cfg, reward_cfg, command_cfg = get_cfgs()
    train_cfg = get_train_cfg(args.exp_name, args.max_iterations)

    # 이미 같은 실험명이 있으면 이전 폴더 삭제
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    os.makedirs(log_dir, exist_ok=True)
    # 설정 값들을 pickle로 저장 -> 나중에 재현 가능
    pickle.dump(
        [env_cfg, obs_cfg, reward_cfg, command_cfg, train_cfg],
        open(f"{log_dir}/cfgs.pkl", "wb"),
    )
    '''
    Go2Env: 4발 로봇 시뮬레이터 생성
    OnPolicyRunner:PPO 학습기를 불러와서 환경 + 설정과 연결
    runner.learn():실제 학습 시작
    '''
    env = Go2Env(
        num_envs=args.num_envs, env_cfg=env_cfg, obs_cfg=obs_cfg, reward_cfg=reward_cfg, command_cfg=command_cfg
    )

    runner = OnPolicyRunner(env, train_cfg, log_dir, device=gs.device)

    runner.learn(num_learning_iterations=args.max_iterations, init_at_random_ep_len=True)


if __name__ == "__main__":
    main()

"""
# training
python examples/locomotion/go2_train.py
"""
```

![](/이미지/backflip%20basemodel.png)
- 명령어를 실행해 무슨 모델에 어떤 체크포인트가 붙는지 확인한 결과

### 파라미터 수(대략)
- Actor = 189,324개
- Critic = 187,905개
- 합계 = 377,229개
### 규격 요약
- 베이스(백그라운드) 모델 = Actor–Critic MLP
    - Actor: 45 → 512 → 256 → 128 → 12
    - Critic: 45 → 512 → 256 → 128 → 1
#### 신경망의 층 구성
- Actor: 45 → 512 → 256 → 128 → 12 (ELU)

- Critic: 45 → 512 → 256 → 128 → 1 (ELU)

- 알고리즘 = PPO(훈련법이지 모델 이름 X)

- 체크포인트(.pt)는 이 Actor/Critic에 로드되어 동작함.

### 결론
- rsl-rl-lib 라이브러리가 policy.class_name="ActorCritic" 설정을 읽어 Actor-Critic MLP를 생성하는 구조
- 즉 YOLO처럼 외부에서 가져오는 사전학습 모델이 아니라, PPO로 학습하는 정책 네트워크
- env.py의 보상 함수 + 커맨드(목표 속도·각속도·기준 높이·기본자세)가 기준을 정의
- env.py의 보상/커맨드 설계가 곧 학습의 기준이 되는 reference라고 할 수 있음

### 결론(drone)
- 결과가 다르다면 drone의 사례를 따로 작성하려 했으나 드론 모델 역시 Genesis 시뮬레이터 + rsl-rl-lib의 PPO가 학습을 진행
- 보상은 전부 hover_env.py의 설계에서 오며, 외부 데이터/ 라벨은 없음
- ActorCritic을 읽어 MLP를 생성하는 것도 동일
