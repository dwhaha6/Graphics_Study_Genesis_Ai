# Genesis 샘플 실행 레포트_2022204067 강동욱

> **용도**: WSL/Ubuntu에서 Genesis(및 샘플) 설치·실행 결과를 기록하고, 재현 가능한 절차와 트러블슈팅을 정리하는 보고서

---
## 0) 목차
### 1. 메타데이터
### 2. 목적 및 개요
### 3. 환경 준비 (Prerequisites)
### 4. 설치 절차 (Installation)
### 5. 샘플 실행 (Experiments)
### 6. 트러블슈팅 모음 (문제-원인-해결)
### 7. 어려웠던 점 & 잘된 점 & 요약
## 1) 메타데이터
- **작성자**: 강동욱
- **작성일**: 2025-09-05
- **프로젝트/과목**: grapics_study_genesis_ai


### 시스템 사양
| 항목 | 값 |
|---|---|
| OS | Windows 11 |
| WSL | WSL2 (커널 버전) |
| Linux | Ubuntu 24.04 LTS  |
| CPU | AMD Ryzen 5 5600 6-Core Processor(3.50 GHz) |
| GPU | RTX 4060 (VRAM 8GB) |
| NVIDIA Driver | 580.97 |
| CUDA Toolkit | 12.6 |
| Python | 3.12.3 |
| PyTorch | 2.8.0+cu126 |
| Genesis | 0.3.3 |

---

## 2) 목적 및 개요
- 이 문서는 Windows + WSL2(Ubuntu) 환경에서 Genesis 시뮬레이터 및 예제(샘플)를 **설치·실행**하고, **결과/성능/이슈**를 정리하여 **재현 가능한 레포트**를 만드는 것을 목표로 한다.
- 결과물: (1) 본 보고서, (2) 스크린샷/동영상 증거, (3) 명령어/환경설정 로그

---

## 3) 환경 준비 (Prerequisites)

### 3.1 WSL/Ubuntu 기본 설치
- PowerShell(관리자)에서 WSL 설치:
  ```powershell
  wsl --install
  ```
- 첫 실행 시 Ubuntu 사용자/비밀번호 설정 후 버전 확인:
  ```bash
  lsb_release -a
  ```
- 아래와 같이 나오면 정상  
![](/images/캡처2.png)
- wsl --install -d Ubuntu-22.04 와 같이 특정버전을 선택해 다운로드 가능
### 이후 모든 명령어는 powershell이 아닌 우분투에서 실행
### 3.2 NVIDIA/CUDA 준비 (CUDA Toolkit 12.6)
- cuda install linux 12.6(원하는 버전)을 구글에 검색
- 맨위의 사이트로 들어가 아래의 사진처럼 세팅
![](/images/캡쳐1.png)
> CUDA 설치 전에 아래와 같이 과거 키를 제거(충돌 방지) 후, WSL용 CUDA 저장소 키를 등록하고 툴킷을 설치할 것을 추천
```bash
# (권장) 과거 NVIDIA 키 제거
sudo apt-key del 7fa2af80
# 이후 밑에 있는 코드들을 순서대로 실행(사진의 코드와 동일)
$ wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
$ sudo dpkg -i cuda-keyring_1.1-1_all.deb
$ sudo apt-get update
$ sudo apt-get -y install cuda-toolkit-12-6
```
### 3.3 nvcc(PATH) 설정 (nvcc 인식 안 될 때)
- nvcc --version 명령어로 cuda의 설치를 확인, 이 때 설치가 인식이 되지 않는다면 아래의 과정을 따름
```bash
# 홈 디렉터리에서 .bashrc 편집
nano ~/.bashrc
# 맨 아래에 추가(CUDA 경로를 맨 앞에 둬서, 같은 이름의 실행파일이 있어도 CUDA 쪽이 먼저 선택되게 하는 설정)
export PATH=/usr/local/cuda-12.6/bin${PATH:+:${PATH}}

# 확인
nvcc --version
```
- 아래와 같이 나오면 정상  
![](/images/캡처3.png)
### 3.4 기본 패키지 업데이트 & 가상환경 활성화
```bash
# 패키지 목록을 최신상태 및 최신 버전으로 업그레이드
sudo apt update && sudo apt upgrade -y
# 파이썬 인터프리터와 pip, 가상환경 모듈 다운로드
sudo apt install -y python3 python3-pip python3-venv
# 홈디렉터리로 이동하고 원하는 이름의 디렉터리를 생성 후 이동
cd ~
mkdir gen
cd gen
# 작업 디렉터리에서 가상환경 생성/활성화
python3 -m venv env1
source env1/bin/activate
```

---

## 4) 설치 절차 (Installation)

### 4.1 PyTorch (CUDA 12.6 빌드)
- 구글에 pytorch cuda install 검색 후 맨 위 사이트 접속
![](/images/캡처4.png)
- 그림과 같이 세팅 후 밑에 나온 명령어를 복사해 실행
``` bash
# 설치가 완료되었다면 아래 명령어로 확인
pip list
```


### 4.2 Genesis
- 이제 genesis ai 깃허브로 접속해 Quick Installation 목차로 이동
![](/images/캡처5.png)
- 가장 최신 버전 설치를 위한 명령어
``` bash
pip install --upgrade pip
pip install git+https://github.com/Genesis-Embodied-AI/Genesis.git
```


## 5) 샘플 실행 (Experiments)
- 각 샘플 실행은 영상으로 대체

---

## 6) 트러블슈팅 모음 (문제-원인-해결)
| 번호 | 증상/에러 메시지 | 원인(추정) | 해결 방법 |
|---:|---|---|---|
| 1 | cpu 과부하 현상 | genesis에서 gpu를 감지하지 못 해 cpu에만 부하가 걸림 | export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH 명령어 실행 후 해결 |
| 2 | 뷰어 영상 끊김현상 | WSL의 실시간 뷰어는 끊기는 현상이 다소 있다고 보고됨 | 실시간으로 뷰어를 생성하지 않고 mp4 형태의 영상으로 저장 | 
| 3 | CUDA 인식 실패 | nvcc 컴파일러와 실행파일이 시스템 PATH에 없음, 즉 nvcc같은 CUDA Toolkit 도구를 쉘/스크립트가 찾지 못 하였음 | .bashrc 파일에 명령어를 삽입해 cuda가 인식되도록 설정 |


---



---

## 7) 어려웠던 점 & 잘된 점 & 요약

### 어려웠던 점
- genesis에서 gpu를 감지하지 못 해 cpu에만 부하가 걸리는 상황이 다소 발생했음.
- **처음 몇초동안 프레임 드랍이 일어남**(초기 컴파일/로딩 때문).
- 일부 샘플들은 요구되는 사양이 높아 실행시키는 게 어려웠음.
- 프레임이 정상이더라도 뷰어 영상이 끊기는 현상이 다소 발생했음.
### 잘 된 점
- `LD_LIBRARY_PATH` 설정 후 **GPU 가속 정상 동작**(genesis 사용자 가이드문서 참조).
- **헤드리스 + mp4 녹화**로 실시간 끊김 문제 우회 성공.
- **가상환경** 덕분에 PyTorch/Genesis **버전 충돌 없이** 설치·실행.

### 요약
- WSLg(리눅스 창 띄우기)로 **실시간 뷰어**는 화면이 가끔 끊김.
- 대신 **카메라로 mp4 저장**하면 영상이 **부드럽게** 나옴.
- **GPU 사용 설정**과 가상환경(venv)의 필요성을 확실히 알게 됨.
