# 뷰어 렌더링 문제 원인 조사

## 뷰어를 끄고 돌렸을 때의 fps
https://github.com/user-attachments/assets/354a524b-f0fd-4ee9-aeb7-a7dbcca97d00
- 렌더링이 문제라는 건데 4070ti gpu가 렌더링에서 문제가 있을 리 없음
## 정확한 원인
### 뷰어 렌더링 = CPU 작업
- Genesis는 PyRender 라이브러리를 사용
- PyRender는 OpenGL로 CPU에서 렌더링
- GPU는 시뮬레이션을 잘 해주지만 CPU의 화면 출력에서 문제가 생긴 것

### CPU 병목 현상
[매 스텝마다]
```
GPU 시뮬레이션 (빠름) → GPU→CPU 데이터 전송 (느림) → CPU 렌더링 (느림) → 화면
         ↑                                                          ↓   
         └──────────────────── GPU가 CPU를 기다림 ────────────────────┘
```
### 결론
- GPU는 본인 일(시뮬레이션)을 다 마치고 CPU가 렌더링 끝내기를 기다림
- GPU 사용률이 뷰어를 껐을 때 대비 절반밖에 나오지 못 함
## 바꿀 수는 없나?
### Genesis 공식 문서
```
The viewer's camera uses the `Rasterizer` backend 
regardless of `gs.renderers.*` when creating the scene.
```
- 어떤 렌더러로 설정하든 무시하고 무조건 Rasteizer를 사용한다는 내용
### 실제 코드 확인
```
# Line 93-107
self._pyrender_viewer = pyrender.Viewer(
    context=self.context,
    viewport_size=self._res,
    run_in_thread=self._run_in_thread,
    ...
)
```
- 뷰어를 **하드코딩**으로 pyrender.Viewer를 사용하게 해놓음
- 코드를 아무리 바꿔봐도 결국 렌더링을 CPU로 돌아갔던 이유임
## 왜 이렇게 만들었을까?
1. 호환성: PyRender는 모든 플랫폼에서 작동
2. 안정성: 실시간 뷰어에서 안정성이 중요하기에 성능보다 안정성을 채택
3. 개발 비용: Nvidia는 자체 GPU뷰어를 개발했으나 Genesis는 오픈소스이기에 그럴 리소스가 없음
## 대안이 아예 없는가?
- Isaac Gym으로 이전(GPU 뷰어 지원)
    - 하지만 Genesis를 포기해야 하기에 대안이라고 보기 힘듦
- cpu로 돌려서 26~30 fps로 만족하며 실시간 뷰어 보기
### 카메라 렌더링 사용하기(GPU,빠름)
#### 개인적으로 가장 좋다고 생각되는 대안입니다.
1. 렌더링 없이 시뮬레이션만을 돌리기에 GPU를 100% 활용하여 시뮬레이션이 병목없이 매우 빠르게 돌아감
2. 그렇게 빠르게 뽑아낸 영상을 원하는 fps로 렌더링하기에 mp4 영상도 매우 깔끔함
3. 실시간으로 뷰어를 보진 못 해도 원하는 목적이 **실시간** 동영상이 아닌 시뮬레이션의 결과를 **깔끔하게** 보는 것이라면 매우 괜찮은 대안이라고 생각이 듦
### 카메라 렌더링으로 만든 동영상
[https://github.com/user-attachments/assets/6fe6a8cc-825d-45de-b913-f04f66fa2fcc](https://github.com/user-attachments/assets/d6ef1c6b-c70a-4689-9225-ec37911b8e1e)
