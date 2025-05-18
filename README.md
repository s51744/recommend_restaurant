# 🍱 宜蘭大學午餐 AI 推薦系統

這是一個使用本地 LLaMA 模型與 Google Places API 的 AI 助理，能夠根據使用者偏好推薦宜蘭大學附近的午餐地點。

---

## 📦 安裝需求

### 1.環境
請先安裝 Python 3.10以上版本及ollama。

### 2. 使用 [`uv`](https://github.com/astral-sh/uv) 安裝依賴（建議）
```bash
pip install uv
ollama run llama3.2
uv venv
uv pip install -r requirements.txt

uv run streamlit run main.py
