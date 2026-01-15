import bpy                 # 블렌더 내부 파이썬 API (오브젝트/프레임/씬 제어)
import csv                 # CSV 파일 쓰기/읽기
import math                # 수학 함수 (sin, cos, pi 등)
import numpy as np         # 수치 계산 도구 (여기선 주로 arange 같은 용도 가능)
from dataclasses import dataclass  # 간단한 데이터 구조(클래스) 만들기
from mathutils import Vector, Quaternion, Matrix  # 블렌더에서 쓰는 벡터/쿼터니언/행렬

# =====================
# CONFIG (설정값들)
# =====================

# Blender 씬 안에서 "차체" 오브젝트 이름
CAR_OBJECT_NAME   = "Corvette.Vehicle Body.RB"

# 앞바퀴(좌/우) 오브젝트 이름
FRONT_LEFT_WHEEL  = "Corvette.Vehicle Body.0.FL1_Wheel.RB"
FRONT_RIGHT_WHEEL = "Corvette.Vehicle Body.0.FR0_Wheel.RB"

# 뒷바퀴(좌/우) 오브젝트 이름
REAR_LEFT_WHEEL   = "Corvette.Vehicle Body.1.BL1_Wheel.RB"
REAR_RIGHT_WHEEL  = "Corvette.Vehicle Body.1.BR0_Wheel.RB"

# RBC Pro(리그)에서 조향/목표속도 같은 "운전 입력값"을 저장해 둔 Armature 이름
ARMATURE_NAME = "Corvette Rig Armature"

# CSV 저장 경로 (Blender에서 나온 주행 데이터를 여기에 저장)
# 50Hz로 뽑고 싶어서, 25FPS라면 0.5프레임마다 샘플링할 것
OUTPUT_CSV_PATH = "C:/Users/dwhah/Desktop/car_12/data_uturn_50hz_direct.csv"

# "차체의 앞 방향"을 로컬 좌표계에서 어떻게 정의할지
# Blender에서 -Y가 앞 방향이라고 가정한 것
BLENDER_FORWARD_LOCAL = Vector((0.0, -1.0, 0.0))

# 바퀴가 구르는(스핀하는) 축이 로컬 좌표에서 어느 축인지
# 여기선 (0,0,-1) 즉 -Z 축을 스핀축으로 가정
# ⚠ 모델마다 다를 수 있어서 체크 포인트라고 써둠
WHEEL_SPIN_AXIS_LOCAL = Vector((0.0, 0.0, -1.0))

# 전진/후진 판별에서, 아주 느리게 움직일 때(노이즈) 잘못 판단하는걸 막는 임계값
V_LONG_EPS = 0.10

# 스로틀 정규화에 쓰는 최대 바퀴 회전속도(기준값)
# Genesis에서 25mph 제한에 맞추려고 31.2로 둔 것
THROTTLE_OMEGA_MAX = 31.2

# 조향 최대각도 (degree → rad로 변환)
MAX_STEER_DEG = 35.0
MAX_STEER_RAD = math.radians(MAX_STEER_DEG)

# dt(시간 간격)가 너무 작으면 나누기 폭주하니까 최소값 둠
MIN_DT = 0.001

# ---------------------
# Blender 좌표 → Genesis 좌표 변환
# ---------------------
# 여기서는 "Z축으로 90도 회전"하면 Blender→Genesis 변환이 된다고 가정
ROT_B2G = Matrix.Rotation(math.radians(90.0), 3, 'Z')

# 벡터(위치/속도) 변환 함수
def vec_B_to_G(v_b: Vector) -> Vector:
    return ROT_B2G @ v_b

# 3x3 회전행렬 변환 함수
def mat3_B_to_G(R_b: Matrix) -> Matrix:
    return ROT_B2G @ R_b

# 쿼터니언(회전) 변환 함수
def quat_B_to_G(q_b: Quaternion) -> Quaternion:
    # 쿼터니언 -> 회전행렬로 바꾸고
    R_g = mat3_B_to_G(q_b.to_matrix())
    # 다시 쿼터니언으로 변환해서 정규화
    return R_g.to_quaternion().normalized()

# =====================
# Cache (이전 값 저장용)
# =====================

def get_obj(name: str):
    # Blender 데이터에서 이름으로 오브젝트를 찾는다
    obj = bpy.data.objects.get(name)
    # 없으면 에러로 중단 (오브젝트 이름이 틀린 경우)
    if obj is None:
        raise RuntimeError(f'Object not found: "{name}"')
    return obj

def get_eval(obj, depsgraph):
    # evaluated_get: 애니메이션/물리 계산이 반영된 "평가된 상태" 오브젝트를 얻는다
    # (그냥 obj 쓰면 물리/드라이버 반영이 덜 될 수 있음)
    return obj.evaluated_get(depsgraph)

# PREV: 이전 프레임의 위치/회전을 저장 (속도/각속도 계산에 필요)
PREV = {}

# PREV_SPIN: 이전 프레임의 바퀴 스핀 각도를 저장 (스핀속도 계산에 필요)
PREV_SPIN = {}

def reset_caches():
    # 클립 시작할 때 캐시를 초기화 (이전 값이 섞이면 속도 계산 망가짐)
    PREV.clear()
    PREV_SPIN.clear()

def vel_angvel_from_eval(name: str, obj_eval, dt: float):
    # 현재 프레임의 위치(벡터) 가져오기
    loc = obj_eval.matrix_world.to_translation().copy()
    # 현재 프레임의 회전(쿼터니언) 가져오기
    quat = obj_eval.matrix_world.to_quaternion().normalized()

    # dt가 너무 작거나, 이전 값이 없으면(첫 프레임) 속도/각속도 0으로 처리
    if dt < MIN_DT or name not in PREV:
        PREV[name] = {"loc": loc.copy(), "quat": quat.copy()}
        return Vector((0.0, 0.0, 0.0)), Vector((0.0, 0.0, 0.0))

    # 이전 위치/회전 불러오기
    prev_loc = PREV[name]["loc"]
    prev_quat = PREV[name]["quat"]

    # dt 안전장치
    dt_safe = max(dt, MIN_DT)

    # 선속도 = (현재위치 - 이전위치) / dt
    vel = (loc - prev_loc) / dt_safe

    # 상대회전 dq = prev^-1 * curr
    dq = prev_quat.conjugated() @ quat
    dq.normalize()

    # dq의 회전각(angle)
    angle = dq.angle

    # 회전이 거의 없으면 각속도 0
    if angle < 1e-12:
        angvel = Vector((0.0, 0.0, 0.0))
    else:
        # 각속도 벡터 = 회전축(axis) * (회전각 / dt)
        angvel = Vector(dq.axis) * (angle / dt_safe)

    # 다음 프레임을 위해 현재값을 저장
    PREV[name]["loc"] = loc.copy()
    PREV[name]["quat"] = quat.copy()

    return vel, angvel

# =====================
# Controls (운전 입력값 읽기)
# =====================

def get_actual_rbc_controls():
    # "RBC 리그(Armature)에 들어있는 운전 입력값"을 읽어오려는 함수
    try:
        # Armature 오브젝트를 찾음
        armature = bpy.data.objects.get(ARMATURE_NAME)
        if not armature:
            return 0.0, 0.0, 0.0, 0.0, 0.0

        # RBC가 저장해둔 커스텀 프로퍼티 키가 있는지 확인
        if 'sna_rbc_rig_armature_props' not in armature.keys():
            return 0.0, 0.0, 0.0, 0.0, 0.0

        # 커스텀 프로퍼티 덩어리
        props = armature['sna_rbc_rig_armature_props']

        # 그 안에 rig_drivers(steering/target_speed)가 있는지 확인
        if 'rig_drivers' not in props.keys():
            return 0.0, 0.0, 0.0, 0.0, 0.0
        rig_drivers = props['rig_drivers']

        # 조향값 읽기 (어떤 파일은 normalize, 어떤 파일은 rad일 수 있음)
        steering_raw = float(rig_drivers.get('steering', 0.0))

        # 만약 값이 -1~1 근처(<=1.5)이면 "정규화 steer"라고 판단
        if abs(steering_raw) <= 1.5:
            steer_norm_actual = steering_raw              # [-1,1] 가정
            steering_actual = steering_raw * MAX_STEER_RAD # rad로 변환
        else:
            # 값이 큰 편이면 이미 rad라고 판단
            steering_actual = steering_raw
            steer_norm_actual = steering_raw / MAX_STEER_RAD

        # 목표속도(target_speed) 읽기
        target_speed = float(rig_drivers.get('target_speed', 0.0))

        # target_speed 단위가 섞일 수 있어서 크기로 추정
        # 30보다 크면 "다른 단위(예: km/h 비슷)"일 가능성 → 0.35로 m/s 근사 변환
        if abs(target_speed) > 30:
            target_speed_ms = target_speed * 0.35
            throttle_raw = target_speed
        else:
            # 작으면 이미 m/s로 가정
            target_speed_ms = target_speed
            throttle_raw = target_speed / 0.35

        # throttle_raw를 THROTTLE_OMEGA_MAX로 나눠 [-1,1]로 정규화
        throttle_norm_actual = max(-1.0, min(1.0, throttle_raw / THROTTLE_OMEGA_MAX))

        # 반환: (steer_rad, steer_norm, throttle_raw, throttle_norm, target_speed_ms)
        return steering_actual, steer_norm_actual, throttle_raw, throttle_norm_actual, target_speed_ms

    except Exception as e:
        # 실패하면 0으로 처리
        print(f"[ERROR] Failed to get RBC controls: {e}")
        return 0.0, 0.0, 0.0, 0.0, 0.0

# =====================
# Utils (보조 함수들)
# =====================

def signed_yaw_between(forward_a_world: Vector, forward_b_world: Vector) -> float:
    # 두 벡터의 "yaw(평면 회전)" 각도 차이를 구한다 (z축 회전만)
    a = Vector((forward_a_world.x, forward_a_world.y, 0.0))
    b = Vector((forward_b_world.x, forward_b_world.y, 0.0))

    # 길이가 0에 가까우면 계산 불가 → 0 반환
    if a.length < 1e-12 or b.length < 1e-12:
        return 0.0

    # 단위벡터로 만들기
    a.normalize()
    b.normalize()

    # 각도 계산용 dot (acos에 넣을 때 -1~1로 클램프)
    dot = max(-1.0, min(1.0, a.dot(b)))
    ang = math.acos(dot)

    # 외적의 z부호로 왼쪽/오른쪽(부호) 결정
    if a.cross(b).z < 0:
        ang = -ang

    return ang

def unwrap_angle(prev, curr):
    # 각도가 -pi~pi로 튀는 것을 방지하기 위해 "연속적인 각도"로 만든다
    if prev is None:
        return curr

    d = curr - prev

    # 차이가 +pi보다 크면 2pi 빼서 가까운 값으로 맞추기
    while d > math.pi:
        curr -= 2.0 * math.pi
        d = curr - prev

    # 차이가 -pi보다 작으면 2pi 더해서 가까운 값으로 맞추기
    while d < -math.pi:
        curr += 2.0 * math.pi
        d = curr - prev

    return curr

def twist_angle_about_axis_stable(q: Quaternion, axis_local: Vector) -> float:
    # q 회전 중에서 "특정 축(axis) 주변으로 도는 성분(twist)"만 뽑아 각도를 구하는 함수
    axis = axis_local.normalized()

    # 쿼터니언 벡터부분(x,y,z)
    v = Vector((q.x, q.y, q.z))

    # v를 axis 방향으로 투영(= twist 성분만)
    proj = axis * v.dot(axis)

    # 쿼터니언 스칼라(w)
    w = float(q.w)

    # 투영 길이
    p = float(proj.length)

    # twist 각도 계산
    ang = 2.0 * math.atan2(p, w)

    # [-pi, pi]로 정리
    if ang > math.pi:
        ang -= 2.0 * math.pi

    # 축 방향과 같은 쪽이면 +, 반대면 -
    sign = 1.0 if proj.dot(axis) >= 0.0 else -1.0

    return sign * abs(ang)

def wheel_spin_rate_clean(wheel_name: str, wheel_eval, car_eval, dt: float) -> float:
    # 바퀴의 스핀 속도(rad/s)를 "안정적으로" 계산하는 함수
    if dt < MIN_DT:
        return 0.0

    # 차체 회전
    q_car = car_eval.matrix_world.to_quaternion().normalized()
    # 바퀴 회전
    q_w   = wheel_eval.matrix_world.to_quaternion().normalized()

    # 차체 기준 바퀴 상대회전 q_rel
    q_rel = q_car.conjugated() @ q_w
    q_rel.normalize()

    # 바퀴 로컬 스핀축을 월드축으로 변환
    axis_world = (wheel_eval.matrix_world.to_3x3() @ WHEEL_SPIN_AXIS_LOCAL).normalized()

    # 월드축을 차체 로컬축으로 변환 (축을 차체 기준으로 맞춤)
    axis_car_local = (car_eval.matrix_world.to_3x3().inverted() @ axis_world).normalized()

    # 상대회전에서 스핀축 주변 twist 각도만 추출
    ang = twist_angle_about_axis_stable(q_rel, axis_car_local)

    # 이전 각도 가져오기
    prev = PREV_SPIN.get(wheel_name, None)

    # angle unwrap으로 튐 방지
    ang_u = unwrap_angle(prev, ang)

    # prev가 있으면 2pi 후보 중에서 가장 가까운 걸 고르기 (더 안정화)
    if prev is not None:
        cands = [ang_u, ang_u + 2*math.pi, ang_u - 2*math.pi]
        ang_u = min(cands, key=lambda a: abs(a - prev))

    # 스핀 속도 = (현재각 - 이전각) / dt
    dt_safe = max(dt, MIN_DT)
    spin = 0.0 if prev is None else (ang_u - prev) / dt_safe

    # 이번 각도를 저장
    PREV_SPIN[wheel_name] = float(ang_u)

    # 너무 큰 값은 이상치이므로 -200~200으로 제한
    return max(-200.0, min(200.0, float(spin)))

def clamp(x, lo, hi):
    # x를 [lo, hi] 범위로 제한하는 함수
    return lo if x < lo else hi if x > hi else x

# =====================
# Main Loop (50Hz Logic)
# =====================

def init_csv(path):
    # CSV 파일을 새로 만들고 헤더(열 이름)를 한 번 적는다
    full_path = bpy.path.abspath(path)
    with open(full_path, mode="w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            # 메타 정보
            "episode", "is_reset", "frame", "time", "dt",

            # Genesis 좌표계 위치/회전
            "g_pos_x", "g_pos_y", "g_pos_z", "g_qw", "g_qx", "g_qy", "g_qz",

            # Genesis 좌표계 속도/각속도
            "g_lin_vx", "g_lin_vy", "g_lin_vz", "g_ang_vx", "g_ang_vy", "g_ang_vz",

            # 차체(body frame) 속도/각속도
            "b_lin_vx", "b_lin_vy", "b_lin_vz", "b_ang_vx", "b_ang_vy", "b_ang_vz",

            # 차체(body frame) 가속도/각가속도
            "b_lin_ax", "b_lin_ay", "b_lin_az", "b_ang_ax", "b_ang_ay", "b_ang_az",

            # actual: 리그에서 읽은 steer/throttle
            "steer_rad_actual", "steer_norm_actual", "throttle_raw_actual", "throttle_norm_actual",

            # reverse: 바퀴/스핀에서 역추정한 steer/throttle
            "steer_rad_reverse", "steer_norm_reverse", "throttle_raw_reverse", "throttle_norm_reverse",

            # 보조: 전진속도 성분, 뒷바퀴 스핀, rbc 목표 속도
            "v_long", "spin_R", "rbc_target_speed",
        ])
    print(f"[CarLogger] CSV init: {full_path}")

def append_row(path, row):
    # CSV 파일 맨 아래에 한 줄(row)을 추가한다
    full_path = bpy.path.abspath(path)
    with open(full_path, mode="a", newline="") as f:
        csv.writer(f).writerow(row)

def sample_one_frame(scene, depsgraph, episode_name, is_reset, frame_idx, dt):
    # 현재 샘플 시점에서 차체/바퀴 오브젝트를 "평가된 상태"로 가져온다
    car = get_eval(get_obj(CAR_OBJECT_NAME), depsgraph)
    wFL = get_eval(get_obj(FRONT_LEFT_WHEEL), depsgraph)
    wFR = get_eval(get_obj(FRONT_RIGHT_WHEEL), depsgraph)
    wRL = get_eval(get_obj(REAR_LEFT_WHEEL), depsgraph)
    wRR = get_eval(get_obj(REAR_RIGHT_WHEEL), depsgraph)

    # FPS 계산
    fps = scene.render.fps / scene.render.fps_base

    # 지금 프레임이 float이므로 시간을 프레임/FPS로 계산
    time_sec = frame_idx / fps

    # Blender 좌표계 위치/회전
    loc_B = car.matrix_world.to_translation()
    rot_B = car.matrix_world.to_quaternion().normalized()

    # 속도/각속도 (이전 프레임 대비)
    v_B, w_B = vel_angvel_from_eval(CAR_OBJECT_NAME, car, dt)

    # 차체 회전행렬
    R_body = car.matrix_world.to_3x3()

    # 차체 forward 방향(월드 기준)
    body_fwd_world = R_body @ BLENDER_FORWARD_LOCAL

    # (actual) RBC 리그에서 조향/스로틀 읽기
    steering_actual, steer_norm_actual, throttle_actual, throttle_norm_actual, target_speed = get_actual_rbc_controls()

    # -------------------------
    # (reverse) 바퀴 방향으로 조향각 추정
    # -------------------------
    def wheel_steer_angle(wheel_eval):
        # 바퀴 회전행렬
        R_w = wheel_eval.matrix_world.to_3x3()
        # 바퀴 forward 방향(월드 기준)
        wheel_fwd = R_w @ BLENDER_FORWARD_LOCAL
        # 차체 forward vs 바퀴 forward yaw 차이 = 조향각
        ang = signed_yaw_between(body_fwd_world, wheel_fwd)

        # 바퀴가 180도 뒤집혀있는 경우 각이 이상해질 수 있어서 [-pi/2, pi/2] 근처로 정리
        if ang > math.pi/2:
            ang -= math.pi
        elif ang < -math.pi/2:
            ang += math.pi
        return ang

    # 좌/우 앞바퀴 조향각 평균
    steer_rad_rev = 0.5 * (wheel_steer_angle(wFL) + wheel_steer_angle(wFR))
    # 조향 정규화 (-1~1)
    steer_norm_rev = clamp(steer_rad_rev / MAX_STEER_RAD, -1.0, 1.0)

    # -------------------------
    # (reverse) 뒷바퀴 스핀속도 계산
    # -------------------------
    spin_RL = wheel_spin_rate_clean(REAR_LEFT_WHEEL,  wRL, car, dt)
    spin_RR = wheel_spin_rate_clean(REAR_RIGHT_WHEEL, wRR, car, dt)
    spin_R = 0.5 * (spin_RL + spin_RR)

    # 차체 forward 방향 성분으로 "전진속도"만 뽑음
    v_long = float(v_B.dot(body_fwd_world))
    v_long = clamp(v_long, -50.0, 50.0)

    # 전진이면 +, 후진이면 - 부호
    msg = 1.0 if v_long > 0 else -1.0

    # 너무 느릴 땐 노이즈 때문에 스로틀을 0으로 처리
    if abs(v_long) < V_LONG_EPS:
        throttle_rev = 0.0
    else:
        # 스핀 크기(절댓값) * 방향 부호
        throttle_rev = abs(spin_R) * msg

    # 스로틀 정규
