# Tích hợp OpenClaw vào Roguelike Snake

Tích hợp này **không nhúng toàn bộ mã nguồn OpenClaw** vào game. Game Python kết nối tới OpenClaw Gateway đang chạy cục bộ qua API tương thích Chat Completions.

## Tính năng

- Nhấn **F1** trong game để mở/đóng khung trợ lý.
- Nhập câu hỏi rồi nhấn **Enter**; **Esc** đóng khung.
- Gửi ngữ cảnh cơ bản của lượt chơi (điểm, tầng, máu, tinh thể, khiên, trạng thái) để trợ lý trả lời phù hợp.
- Yêu cầu mạng chạy trong luồng nền để vòng lặp Pygame không bị treo.
- Không cấu hình token thì game vẫn chạy; trợ lý hiển thị hướng dẫn cấu hình.

## 1. Cài và khởi động OpenClaw

Cài đặt theo hướng dẫn chính thức: https://docs.openclaw.ai/install

Khởi chạy onboarding và Gateway theo tài liệu OpenClaw. Endpoint Chat Completions bị tắt mặc định; cần bật trong cấu hình Gateway:

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    }
  }
}
```

Giữ Gateway chỉ truy cập từ máy tin cậy (mặc định local là `http://127.0.0.1:18789`). Bearer token Gateway là thông tin nhạy cảm và có thể cấp quyền vận hành rộng; **không chia sẻ token, không commit token vào Git, không đặt token trực tiếp trong mã nguồn**.

## 2. Thiết lập trong Windows PowerShell

Từ thư mục `roguelike-snake-python`, đặt biến môi trường cho cửa sổ PowerShell hiện tại:

```powershell
$env:OPENCLAW_GATEWAY_URL = "http://127.0.0.1:18789"
$env:OPENCLAW_GATEWAY_TOKEN = "DAN_TOKEN_GATEWAY_CUA_BAN"
$env:OPENCLAW_MODEL = "openclaw/default"
python main.py
```

Thay giá trị mẫu bằng token Gateway thật của bạn. Đừng gửi token vào chat hay đưa vào repository.

## 3. Chạy game

```powershell
python -m pip install -r requirements.txt
python main.py
```

Không cần cài thêm package Python cho kết nối API; client sử dụng thư viện chuẩn.

## 4. Khắc phục sự cố

- **Không kết nối được**: kiểm tra Gateway đang chạy, URL và cổng.
- **HTTP 401/403**: kiểm tra token; không dán token vào log công khai.
- **HTTP 404**: bật `gateway.http.endpoints.chatCompletions.enabled` rồi khởi động lại Gateway.
- **Không có model/cấu hình AI**: chạy `openclaw models status` và hoàn tất thiết lập provider theo tài liệu chính thức.
- **Game không có AI**: vẫn chơi bình thường; tích hợp AI là tính năng tùy chọn.

## Giới hạn

Trợ lý hiện chỉ trả lời câu hỏi dựa trên ngữ cảnh game. Nó không tự điều khiển rắn, không sửa file game và không thực thi lệnh máy tính. API Gateway cần được xem là quyền truy cập nhạy cảm; chỉ kết nối tới Gateway bạn tin cậy.

Tài liệu API: https://docs.openclaw.ai/gateway/openai-http-api
