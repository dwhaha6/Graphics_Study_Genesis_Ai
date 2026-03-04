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

## MLP 지도학습 결과(이미지 클릭시 MLP 결과 영상 재생)

| 직선+우+좌 | N커브 | S커브 | 3코너 | 저속 좌유턴 |
|:-----------:|:-----------:|:-----:|:-----:|:-----------:|
| <a href="https://github.com/user-attachments/assets/8822b801-3b97-4dfc-8193-d31f424028d5"><img src="이미지/mlp_rightLeft.png" width="180"></a><br>-----------------<br>PosErr μ=0.1667m <br> max=0.8075m<br>VErr μ=0.1200 <br> max=0.5855 | <a href="https://github.com/user-attachments/assets/51aacd5a-37ed-4ec4-b7cf-a14c3bf264b1"><img src="이미지/mlp_n.png" width="180"></a><br>-----------------<br>PosErr μ=0.0543m <br> max=0.1409m<br>VErr μ=0.1237 <br> max=0.6772 | <a href="https://github.com/user-attachments/assets/4d40fd7e-2c26-4f4d-b1a2-6676560331fa"><img src="이미지/mlp_s.png" width="180"></a><br>-----------------<br>PosErr μ=0.0523m <br> max=0.1121m<br>VErr μ=0.0641 <br> max=0.1978 | <a href="https://github.com/user-attachments/assets/1f979491-1594-4e5f-9580-2dc2efc7add4"><img src="이미지/mlp_3corner.png" width="180"></a><br>-----------------<br>PosErr μ=0.0844m <br> max=0.1948m<br>VErr μ=0.0694 <br> max=0.3033 | <a href="https://github.com/user-attachments/assets/5fa0d3c8-095d-4a2f-8363-1d862aa8d8cc"><img src="이미지/mlp_leftU.png" width="180"></a><br>-----------------<br>PosErr μ=0.0333m <br> max=0.0809m<br>VErr μ=0.2596 <br> max=0.5654 |

| 우측 유턴 | 슬라롬 | 직진(저속->고속->저속) | 직진(고속→저속→고속) | 타이트 코너 |
|:-----------:|:------:|:--------------:|:--------------:|:-----------:|
| <a href="https://github.com/user-attachments/assets/2129179e-8eae-41bb-9a05-3ecbb1fef9d8"><img src="이미지/mlp_rightU.png" width="180"></a><br>-----------------<br>PosErr μ=0.0357m <br> max=0.0917m<br>VErr μ=0.1135 <br> max=0.5633 | <a href="https://github.com/user-attachments/assets/50a16cce-22c0-4da4-a592-d0752d17b5f6"><img src="이미지/mlp_slalom.png" width="180"></a><br>-----------------<br>PosErr μ=0.1460m <br> max=0.6721m<br>VErr μ=0.2056 <br> max=0.7504 | <a href="https://github.com/user-attachments/assets/acffaa71-1a44-494f-8a5c-48051236c93e"><img src="이미지/mlp_straight_sfs.png" width="180"></a><br>-----------------<br>PosErr μ=0.0259m <br>  max=0.0776m<br>VErr μ=0.0412 <br> max=0.1526 | <a href="https://github.com/user-attachments/assets/a8f27a16-2b62-4f7d-a38d-76bba74ede45"><img src="이미지/mlp_straight_fsf.png" width="180"></a><br>-----------------<br>PosErr μ=0.0241m <br> max=0.0792m<br>VErr μ=0.0503 <br> max=0.4102 | <a href="https://github.com/user-attachments/assets/179adbb2-a176-4ff6-b70f-3efc8a4711ad"><img src="이미지/mlp_tight_corner.png" width="180"></a><br>-----------------<br>PosErr μ=0.0327m <br>  max=0.0839m<br>VErr μ=0.0452 <br> max=0.1729 |


---

## 학습시키지 않은 새로운 움직임 실험(이미지 클릭시 영상 재생)

- 새로운 경로에 대해 Blender raw 제어 및 state 입력
- 학습 범위 내 속도·곡률 영역에서 일반화 성능 검증

| 시도1 | 시도2 | 시도3 |
|:-----------:|:------:|:--------------:|
| <a href="https://github.com/user-attachments/assets/53e9daab-df20-46ad-8033-3ab87817747e"><img src="이미지/try1.png" width="180"></a><br>-----------------<br>PosErr μ=0.0424m <br> max=0.1323m<br>VErr μ=0.0558 <br> max=0.1492 | <a href="https://github.com/user-attachments/assets/7d9e59be-409d-4e87-9ee7-7a120a03ea43"><img src="이미지/try2.png" width="180"></a><br>-----------------<br>PosErr μ=0.0405m <br> max=0.0855m<br>VErr μ=0.0577 <br> max=0.1482 | <a href="https://github.com/user-attachments/assets/85e47ad6-02f4-467a-8690-1fcc33f85809"><img src="이미지/try3.png" width="180"></a><br>-----------------<br>PosErr μ=0.2540m <br> max=0.9366m<br>VErr μ=0.1579 <br> max=0.9549 |
