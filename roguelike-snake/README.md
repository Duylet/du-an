# Roguelike Snake — Neon Dungeon

Một game Snake phong cách roguelike chạy trực tiếp trên trình duyệt, không cần cài thư viện hay build.

## Chạy game

1. Tải hoặc clone repository.
2. Mở thư mục `roguelike-snake`.
3. Mở `index.html` bằng trình duyệt hiện đại.

Bạn cũng có thể dùng VS Code với tiện ích Live Server để chạy qua máy chủ local.

## Điều khiển

- **WASD** hoặc **phím mũi tên**: di chuyển.
- **Space**: tạm dừng / tiếp tục.
- **Chạm và vuốt** trên bàn chơi: điều khiển trên màn hình cảm ứng.
- Nút **Chơi lại run**: bắt đầu lượt mới.

## Luật chơi

- Thu thập tinh thể để nhận điểm.
- Tránh tường, chướng ngại vật và chính thân rắn.
- Mỗi 3 tinh thể, chọn một nâng cấp ngẫu nhiên.
- Mỗi 5 tinh thể, tiến xuống tầng tiếp theo; tốc độ và số bẫy tăng dần.
- Bạn có 3 lượt chịu va chạm. Điểm kỷ lục được lưu trong localStorage của trình duyệt.

## Cấu trúc

```text
roguelike-snake/
├── index.html  # Giao diện và HUD
├── style.css   # Giao diện neon responsive
├── game.js     # Vòng lặp game, va chạm, tầng và nâng cấp
└── README.md   # Hướng dẫn
```

## Công nghệ

- HTML5 Canvas
- CSS
- JavaScript thuần (ES6+)

Không cần API key, backend hoặc dependency ngoài. Font Google Fonts là tùy chọn; game vẫn chạy nếu ngoại tuyến với font dự phòng.

## Ý tưởng phát triển tiếp

- Thêm boss và loại quái vật.
- Thêm vật phẩm hiếm, bản đồ sinh theo seed và hiệu ứng âm thanh.
- Thêm màn hình chọn nhân vật, hệ thống meta-progression và bảng xếp hạng.
- Viết test cho va chạm, sinh bản đồ và hệ thống nâng cấp.
