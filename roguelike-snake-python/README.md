# Roguelike Snake — Neon Dungeon (Python)

Game rắn săn mồi 2D theo phong cách roguelike, viết bằng Python và Pygame.

## Tính năng

- Điều khiển bằng WASD hoặc phím mũi tên.
- Nhặt tinh thể để tăng điểm và chiều dài.
- Chướng ngại vật và các tầng khó dần.
- Cứ 3 tinh thể được chọn một trong ba nâng cấp ngẫu nhiên.
- Nâng cấp: tăng tốc, hồi sinh lực, tăng điểm thưởng hoặc nhận khiên.
- Lưu điểm cao trên máy bằng tệp trong thư mục người dùng.
- Giao diện neon, không cần hình ảnh hay tài nguyên bên ngoài.

## Cài đặt

Cần Python 3.10 trở lên.

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo:

**Windows**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Cài thư viện và chạy game:

```bash
python -m pip install -r requirements.txt
python main.py
```

## Điều khiển

| Phím | Tác dụng |
|---|---|
| WASD / Mũi tên | Di chuyển |
| Enter | Bắt đầu / chơi lại |
| P | Tạm dừng / tiếp tục |
| 1, 2, 3 | Chọn nâng cấp |
| Esc | Thoát |

## Luật chơi

- Đụng tường, thân rắn hoặc chướng ngại vật sẽ mất một mạng.
- Khi còn mạng, rắn sẽ trở về khu vực trung tâm.
- Mỗi tinh thể cho 10 điểm cộng điểm thưởng hiện tại.
- Cứ 5 tinh thể, tầng mới xuất hiện cùng chướng ngại vật bổ sung.
- Điểm cao được lưu cục bộ; không gửi dữ liệu ra mạng.

## Cấu trúc

- `main.py`: vòng lặp game, vẽ giao diện, điều khiển và logic.
- `requirements.txt`: thư viện cần cài.
