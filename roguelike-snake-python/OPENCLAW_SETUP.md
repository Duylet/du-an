# Kết nối OpenClaw với dự án Roguelike Snake (Python)

OpenClaw là trợ lý AI chạy riêng trên máy tính, không phải thư viện Python cần thêm vào `requirements.txt`. Cách tích hợp dự án là cài OpenClaw trên máy của bạn, sau đó trỏ workspace của agent đến thư mục dự án. Tệp `AGENTS.md` trong thư mục này cung cấp hướng dẫn làm việc cho agent.

Tài liệu chính thức: https://docs.openclaw.ai/install  
Workspace và cấu hình: https://docs.openclaw.ai/agent-workspace

## 1. Cài OpenClaw trên Windows

Mở PowerShell và chạy lệnh cài đặt từ tài liệu chính thức:

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Nếu bạn chưa rõ nội dung một script tải từ Internet, hãy mở và đọc tài liệu cài đặt chính thức trước khi chạy. Trình cài đặt có thể cài thành phần cần thiết và khởi chạy bước thiết lập.

Sau khi cài, hoàn thành hướng dẫn onboarding để chọn nhà cung cấp mô hình và xác thực. Không đưa API key, mật khẩu hoặc token vào GitHub hay vào tệp cấu hình được commit.

Kiểm tra:

```powershell
openclaw --version
openclaw doctor
openclaw gateway status
openclaw dashboard
```

## 2. Tải dự án Python về máy

Nếu bạn chưa clone repository:

```powershell
git clone -b feature/openclaw-project-setup https://github.com/Duylet/du-an.git
cd du-an\roguelike-snake-python
```

Nếu nhánh này đã được merge vào `main`, có thể clone nhánh `main` thay thế.

## 3. Cho OpenClaw làm việc với dự án

OpenClaw giữ cấu hình, thông tin xác thực và phiên làm việc riêng trong thư mục trạng thái của nó. Không sao chép thư mục đó vào repository.

Cách đơn giản là cấu hình workspace của agent thành đường dẫn tuyệt đối tới thư mục `roguelike-snake-python` trên máy của bạn, sau khi đã kiểm tra đường dẫn chính xác. Mở cấu hình bằng wizard:

```powershell
openclaw configure
```

Trong cấu hình agent, đặt `agents.defaults.workspace` thành đường dẫn thư mục dự án. Ví dụ minh họa — hãy thay đường dẫn bằng vị trí thật trên máy:

```json5
{
  agents: {
    defaults: {
      workspace: "C:/duong-dan-thuc-te/du-an/roguelike-snake-python"
    }
  }
}
```

Đây là ví dụ cấu hình, không phải tệp cấu hình dùng chung để commit. Giữ nguyên các mục cấu hình hiện có; không thay toàn bộ cấu hình nếu bạn đã thiết lập kênh chat, model hoặc quyền truy cập khác.

Khởi động lại Gateway nếu cần, sau đó kiểm tra:

```powershell
openclaw gateway status
openclaw dashboard
```

Khi hỏi agent về dự án, yêu cầu nó đọc `AGENTS.md`, `README.md` và `main.py` trước khi đề xuất thay đổi.

## 4. An toàn khi dùng agent viết code

- Chỉ cấp quyền truy cập cần thiết; workspace không phải lúc nào cũng là ranh giới bảo mật tuyệt đối.
- Không bật quyền thực thi lệnh hoặc quyền truy cập rộng hơn nếu bạn chưa hiểu tác động.
- Kiểm tra diff trước khi commit; không cho agent tự ý xóa dữ liệu, phát hành hoặc merge.
- Không đưa khóa API, token, mật khẩu hay tệp riêng tư vào Git.
- Với dự án đang dùng Git, làm việc trên nhánh riêng và xem lại thay đổi trước khi merge.

## 5. Chạy game

OpenClaw không thay thế Python hoặc Pygame. Để chạy game trong terminal của dự án:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Lưu ý: thêm tài liệu này vào GitHub chỉ chuẩn bị hướng dẫn tích hợp. Việc cài OpenClaw và cấu hình đường dẫn thực tế phải thực hiện trên máy tính nơi bạn muốn chạy OpenClaw.
