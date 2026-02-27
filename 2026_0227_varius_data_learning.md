# 다양한 데이터 추출 & 학습

- 이전에 진행한 것과 방식은 동일
- 다양한 Blender 움직임을 만들어 데이터를 추출
- Ground Truth 생성 후 MLP 지도학습 진행

---

## Ground Truth 결과

| 직선+우+좌 | N커브 | S커브 | 3코너 | 저속 좌유턴 |
|:-----------:|:-----------:|:-----:|:-----:|:-----------:|
| <a href="https://raw.githubusercontent.com/dwhaha6/Graphics_Study_Genesis_Ai/main/video/gt_rightLeft.mp4"><img src="이미지/best_rightLeft.png" width="180"></a> | <a href="https://raw.githubusercontent.com/dwhaha6/Graphics_Study_Genesis_Ai/main/video/gt_n.mp4"><img src="이미지/best_n.png" width="180"></a> | <a href="https://raw.githubusercontent.com/dwhaha6/Graphics_Study_Genesis_Ai/main/video/gt_s.mp4"><img src="이미지/best_s.png" width="180"></a> | <a href="https://raw.githubusercontent.com/dwhaha6/Graphics_Study_Genesis_Ai/main/video/gt_3corner.mp4"><img src="이미지/best_3corner.png" width="180"></a> | <a href="https://raw.githubusercontent.com/dwhaha6/Graphics_Study_Genesis_Ai/main/video/gt_leftU.mp4"><img src="이미지/best_leftU.png" width="180"></a> |

| 중속 우유턴 | 슬라롬 | 직진(저→고→저) | 직진(고→저→고) | 타이트 코너 |
|:-----------:|:------:|:--------------:|:--------------:|:-----------:|
| <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/gt_rightU.mp4"><img src="images/gt_rightU.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/gt_slalom.mp4"><img src="images/gt_slalom.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/gt_sfs.mp4"><img src="images/gt_sfs.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/gt_fsf.mp4"><img src="images/gt_fsf.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/gt_tight.mp4"><img src="images/gt_tight.png" width="180"></a> |

- Ground Truth 완료, MLP 지도학습 진행

---

## MLP 지도학습 결과

| 직선+우코너 | 직선+좌코너 | S커브 | 3코너 | 저속 좌유턴 |
|:-----------:|:-----------:|:-----:|:-----:|:-----------:|
| <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_export.mp4"><img src="images/mlp_export.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_n.mp4"><img src="images/mlp_n.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_s.mp4"><img src="images/mlp_s.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_3corner.mp4"><img src="images/mlp_3corner.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_leftU.mp4"><img src="images/mlp_leftU.png" width="180"></a> |

| 중속 우유턴 | 슬라롬 | 직진(저→고→저) | 직진(고→저→고) | 타이트 코너 |
|:-----------:|:------:|:--------------:|:--------------:|:-----------:|
| <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_rightU.mp4"><img src="images/mlp_rightU.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_slalom.mp4"><img src="images/mlp_slalom.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_sfs.mp4"><img src="images/mlp_sfs.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_fsf.mp4"><img src="images/mlp_fsf.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_tight.mp4"><img src="images/mlp_tight.png" width="180"></a> |

---

## 학습시키지 않은 새로운 움직임 실험

- 10개의 움직임을 학습
- 새로운 경로에 대해 Blender raw 제어 및 state 입력
- 학습 범위 내 속도·곡률 영역에서 일반화 성능 검증

<a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_new.mp4">
  <img src="images/mlp_new.png" width="300">
</a>
