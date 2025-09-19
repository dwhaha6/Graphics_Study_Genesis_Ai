# CARLA Simulator 정리
- https://github.com/carla-simulator/carla
## 개요
- 오픈소스 자율주행 연구용 시뮬레이터, Unreal Engine 기반
- 주요 목적: 자율 주행 시스템의 개발, 학습, 검증
- 특징적인 기능들:
    - 다양한 센서 시뮬레이션(카메라, LiDAR,Radar, GPS/LMU 등)
    - 날씨, 시간, 조명, 교통 조건 등 환경 설정 가능
    - 맵/ 도로 표준 지원, 도시/교외 등 다양한 시나리오 제공
    - Server-client 구조: 시뮬레이터 서버가 물리 연산/ 센서 렌더링/ 월드 상태 업데이트를 담당, 클라이언트가 API를 통해 제어/ 데이터를 수신
    - ROS/ROS2 브릿지 지원: ROS 노드로 센서/액터 제어 가능
- 권장 사양: 고성능 GPU 권장, 메모리가 많이 필요, 특히 시각 렌더링 모드 혹은 복잡한 맵/ 많은 NPC 사용시 더더욱 그런 것으로 보임
## 주요 구성 요소/ 코어 개념
- Wrold & Client
    - 클라이언트가 시뮬레잍 서버에 접속하여 명령을 보내고 정보를 받음. 월드는 현재 맵/환경을 나타냄
- Actors & Blueprints
    - 차량(vehicle), 보행자(walker), 신호등, 교통 표지판, 센서 등 시뮬 내의 "행위자(actors)" 사용. Blueprints 는 미리 정의된 행위자 모델 묶음으로 필요에 따라 사용자 정의 변경 가능
- Sensors
    - RGB / Depth / Semantic Segmentation 카메라, LiDAR, Radar, IMU, GPS 등 다양ㅎ나 센서 제공. 센서 데이터는 클라이언트 API로 노출됨
- MAPS / Roads
    - 여러 미리 제공되는 "Town" 맵들이 있고 OpenDRIVE 표준을 통한 도로 정의 가능. 사용자 생성 맵도 추가 가능
- Scenario / Traffic / NPCs
    - 자동 차량, 보행자, 교통 규칙, 신호등, 날씨 변화 등의 환경 요소들이 포함됨
    - ScenarioRunner 같은 도구로 다양한 시나리오 정의 가능
- ROS / ROS2 Bridge
    - CARLA와 ROS 간 양방향 통신 가능하게 해 주는 bridge 패키지 있음
    - 센서 데이터 ROS 토픽으로 송출, 차량 조작 명령 받기 가능
    - ROS1/ ROS2 버전들이 존재함
## 설치 및 실행
### 의존 환경 준비
- 운영체제: 일반적으로 Ubuntu(20.04 권장, 22.04도 지원됨)
- GPU 및 드라이버: NVIDIA GPU + 최신 드라이버. 렌더링/ 시각 퀄리티 높은 작업을 위해 권장됨
    - 문서상에는 RTX 2060, 8GB이상의 GPU를 권장한다고 나오지만 대형 맵이나 차후 원하는 세팅으로 돌리려면 훨씬 고사양의 수준이 요구될 것으로 예상됨
    - Unreal Engine 버전: 기본적으로 UE4(Unreal Engine 4.26 이상) 버전이 안정적임. 일부 개발 브랜치는 UE5 기반인 것도 있음
### CARLA 다운로드/설치
```python
# 예: Ubuntu에서 미리 빌드된 버전 사용
# git clone
git clone https://github.com/carla-simulator/carla
cd carla

# 필요한 서브모듈
git submodule update --init

# 빌드 (소스에서)
make clean
make launch      # 또는 make PythonAPI 등의 옵션 추가
```
- 또는 Github Releases 에서 제공하는 바이너리/패키지 버전 다운로드 가능
### Python API 설치
- Python API를 설치해서 클라이언트 코드를 쓸 수 있게 함
```python
cd PythonAPI
# 예: pip 설치
pip install carla-<version-and-arch>.egg
```
### ROS/ROS2 브릿지 설치
- ros-bridge 저장소를 클론하고, 의존성 설치 & 빌드함
- ROS1 혹은 ROS2 환경에 따라
    - ROS2 ex) Ubuntu 20.04 + ROS2 Foxy 등의 조합
    - ROS1 ex) Ubuntu 18.04/20.04 + Melodic / Noetic 등
```python
# ROS2 브릿지 예
mkdir -p ~/carla_ros_bridge && cd ~/carla_ros_bridge
git clone --recurse-submodules https://github.com/carla-simulator/ros-bridge.git src/ros-bridge
cd ~/carla_ros_bridge
rosdep update
rosdep install --from-paths src --ignore-src -r
colcon build
```
- 브릿지를 실행하려면 CARLA 서버 먼저 실행 → 다른 터미널에서 브리지 노드 launch 사용
### 시뮬레이터 실행 예제
- CARLA 서버 실행
```python
# 소스 버전일 경우
./CarlaUE4.sh

# 또는 make launch
make launch
```
- ROS 브리지 + ego 차량 예제 실행
```python
roslaunch carla_ros_bridge carla_ros_bridge.launch             # (ROS1)
# 또는
ros2 launch carla_ros_bridge carla_ros_bridge.launch.py         # (ROS2)
```
- 매개변수 옵션 조정 가능: 맵(town), spawn point, 동기화 모드(synchronous mode), 센서 구성(sensor suite), 날씨 설정 등.
### 장단점 및 주의할 점
![](./화면%20캡처%202025-09-17%20200156.png)
