# 다양한 데이터 추출 & 학습

- 이전에 진행한 것과 방식은 동일
- 다양한 Blender 움직임을 만들어 데이터를 추출
- Ground Truth 생성 후 MLP 지도학습 진행

---

## Ground Truth 결과(이미지 클릭시 Ground Truth 영상 재생)



| 직선+우+좌 | N커브 | S커브 | 3코너 | 저속 좌유턴 |
|:-----------:|:-----------:|:-----:|:-----:|:-----------:|
| <a href="https://github.com/user-attachments/assets/fd8e22ee-9496-421a-b9b3-7bf837660745"><img src="이미지/best_rightLeft.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/9935096d-d20b-4336-bbca-c90486ef9bdc"><img src="이미지/best_n.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/66f6d5d9-0b65-46b0-b378-c858ed37f1cf"><img src="이미지/best_s.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/021965da-b7be-473e-a6ba-741b2c44bdab"><img src="이미지/best_3corner.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/420e65b6-9254-4d79-9cc6-6c5353f3106b"><img src="이미지/best_leftU.png" width="180"></a> |

| 우측 유턴 | 슬라롬 | 직진(저속->고속->저속) | 직진(고속→저속→고속) | 타이트 코너 |
|:-----------:|:------:|:--------------:|:--------------:|:-----------:|
| <a href="https://github.com/user-attachments/assets/d8e6af30-1ea0-44c0-98d2-0c0c260af716"><img src="이미지/best_rightU.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/fad77c58-995e-489f-be7c-e1fc2fbe40a3"><img src="이미지/best_slalom.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/f2e2d760-40f4-40fa-b0c7-7a2e172821ed"><img src="이미지/best_straight_sfs.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/ba5649e1-2e63-455e-9b21-f1da11556839"><img src="이미지/best_straight_fsf.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/263cdb29-4393-46e3-8212-0410ebd7ed60"><img src="이미지/best_tight_corner.png" width="180"></a> |

- 다양한 움직임에 대한 Ground Truth 완료

---

## MLP 지도학습 결과(진행중)

| 직선+우+좌 | N커브 | S커브 | 3코너 | 저속 좌유턴 |
|:-----------:|:-----------:|:-----:|:-----:|:-----------:|
| <a href="https://github.com/user-attachments/assets/fd8e22ee-9496-421a-b9b3-7bf837660745"><img src="이미지/best_rightLeft.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/9935096d-d20b-4336-bbca-c90486ef9bdc"><img src="이미지/best_n.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/c01ab093-27d3-4078-9fca-889afcf7a32f"><img src="이미지/mlp_s.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/021965da-b7be-473e-a6ba-741b2c44bdab"><img src="이미지/best_3corner.png" width="180"></a> | <a href="https://github.com/user-attachments/assets/420e65b6-9254-4d79-9cc6-6c5353f3106b"><img src="이미지/best_leftU.png" width="180"></a> |

| 중속 우유턴 | 슬라롬 | 직진(저→고→저) | 직진(고→저→고) | 타이트 코너 |
|:-----------:|:------:|:--------------:|:--------------:|:-----------:|
| <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_rightU.mp4"><img src="images/mlp_rightU.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_slalom.mp4"><img src="images/mlp_slalom.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_sfs.mp4"><img src="images/mlp_sfs.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_fsf.mp4"><img src="images/mlp_fsf.png" width="180"></a> | <a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_tight.mp4"><img src="images/mlp_tight.png" width="180"></a> |

---

## 학습시키지 않은 새로운 움직임 실험(진행중)

- 10개의 움직임을 학습
- 새로운 경로에 대해 Blender raw 제어 및 state 입력
- 학습 범위 내 속도·곡률 영역에서 일반화 성능 검증

<a href="https://raw.githubusercontent.com/USERNAME/REPO/main/videos/mlp_new.mp4">
  <img src="images/mlp_new.png" width="300">
</a>
