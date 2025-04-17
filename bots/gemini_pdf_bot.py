import os
import PyPDF2
import requests
import base64
from urllib.parse import urlparse

class GeminiPdfBot:
    def __init__(self, api_key=None, history_limit=10):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")
        self.history = []  # List of (role, message)
        self.history_limit = history_limit

    def ask(self, query, pdf_path=None):
        self.history.append(("user", query))
        messages = []
        # Add previous dialog history (text only)
        for role, msg in self.history[-self.history_limit:-1]:
            messages.append({
                "role": "user" if role == "user" else "model",
                "parts": [{"text": msg}]
            })
        # Load PDF bytes from path/url/base64-url
        pdf_bytes = self._load_pdf_bytes(pdf_path) if pdf_path else None
        if not pdf_bytes:
            return "Vui lòng gửi file PDF hợp lệ trước khi đặt câu hỏi. / Please upload a valid PDF file before asking questions."
        b64_pdf = base64.b64encode(pdf_bytes).decode()
        user_parts = [
            {"text": query},
            {"inline_data": {"mime_type": "application/pdf", "data": b64_pdf}}
        ]
        messages.append({"role": "user", "parts": user_parts})
        response = self._ask_gemini(messages)
        self.history.append(("bot", response))
        return response

    def _load_pdf_bytes(self, pdf_path):
        if not pdf_path:
            return None
        if pdf_path.startswith("http://") or pdf_path.startswith("https://"):
            # Download from URL
            resp = requests.get(pdf_path)
            if resp.status_code == 200:
                return resp.content
            else:
                return None
        elif pdf_path.startswith("data:application/pdf;base64,"):
            # Base64 data URL
            b64_data = pdf_path.split(",", 1)[1]
            return base64.b64decode(b64_data)
        else:
            # Local file path
            try:
                with open(pdf_path, "rb") as f:
                    return f.read()
            except Exception:
                return None

    def _ask_gemini(self, messages):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {"contents": messages}
        resp = requests.post(url, headers=headers, params=params, json=data)
        resp.raise_for_status()
        result = resp.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "Sorry, I couldn't get an answer from Gemini."

    def reset_history(self):
        self.history = []
