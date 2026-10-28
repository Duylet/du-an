"""Optional OpenClaw Gateway client for Roguelike Snake.

The game works without OpenClaw. Configure OPENCLAW_GATEWAY_URL and
OPENCLAW_GATEWAY_TOKEN only if you have a trusted local Gateway.
"""
import json
import os
import urllib.error
import urllib.request


class OpenClawError(RuntimeError):
    """A safe, user-facing connection or API error."""


class OpenClawClient:
    def __init__(self):
        self.base_url = os.getenv("OPENCLAW_GATEWAY_URL", "http://127.0.0.1:18789").rstrip("/")
        self.token = os.getenv("OPENCLAW_GATEWAY_TOKEN", "").strip()
        self.model = os.getenv("OPENCLAW_MODEL", "openclaw/default")

    def ask(self, question, game_context=""):
        if not self.token:
            raise OpenClawError(
                "Chưa cấu hình OPENCLAW_GATEWAY_TOKEN. Hãy xem OPENCLAW_INTEGRATION.md."
            )
        url = self.base_url + "/v1/chat/completions"
        content = (game_context + "\n\nCâu hỏi của người chơi: " + question).strip()
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Bạn là trợ lý hướng dẫn game Roguelike Snake. Trả lời ngắn gọn bằng tiếng Việt. Không tuyên bố đã thay đổi game hoặc máy tính."},
                {"role": "user", "content": content},
            ],
            "stream": False,
        }
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.token,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                result = json.loads(response.read().decode("utf-8"))
            answer = result["choices"][0]["message"]["content"]
            if not isinstance(answer, str) or not answer.strip():
                raise OpenClawError("OpenClaw trả về câu trả lời trống.")
            return answer.strip()[:2500]
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                raise OpenClawError("Xác thực Gateway thất bại. Kiểm tra token và cấu hình.") from None
            if exc.code == 404:
                raise OpenClawError("Không tìm thấy endpoint. Hãy bật chatCompletions trong cấu hình OpenClaw.") from None
            if exc.code == 429:
                raise OpenClawError("Gateway đang giới hạn yêu cầu. Hãy thử lại sau.") from None
            raise OpenClawError(f"Gateway trả về HTTP {exc.code}.") from None
        except (urllib.error.URLError, TimeoutError):
            raise OpenClawError("Không kết nối được OpenClaw Gateway. Kiểm tra Gateway và URL.") from None
        except (KeyError, IndexError, TypeError, json.JSONDecodeError):
            raise OpenClawError("Phản hồi từ OpenClaw không đúng định dạng mong đợi.") from None
