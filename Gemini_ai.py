import os
import streamlit as st
import requests
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
# Step 1: 檢查金鑰
GOOGLE_API_KEY = "AIzaSyDnt2c7wig5FMew0S8vqAIOUuUcH0gzYto"
if not GOOGLE_API_KEY:
    st.error("❌ Google API 金鑰未正確載入，請檢查 .env 檔案。")

# Step 2: 搜尋附近餐廳
def search_nearby_restaurants(location="24.7444,121.7403", radius=1000, keyword="午餐"):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": GOOGLE_API_KEY,
        "location": location,
        "radius": radius,
        "keyword": keyword,
        "type": "restaurant",
        "language": "zh-TW"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("status") != "OK":
        st.error(f"❌ Google API 錯誤：{data.get('status')} - {data.get('error_message', '')}")
        return []
    return data.get("results", [])

# 自訂提示
template = """
你是一個美食推薦助理，請根據下列附近餐廳資料與使用者需求推薦午餐地點：

<餐廳資料>
{context}
</餐廳資料>


使用者說: {input}
你的回應：
"""
prompt = ChatPromptTemplate.from_template(template)

# Step 3: 建立 LLM Chain
llm = ChatOllama(model="llama3.2", temperature=0.7)
prompt = ChatPromptTemplate.from_template(template)
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Step 4: 使用者互動
if st.button("取得附近餐廳資訊"):
    restaurants = search_nearby_restaurants()
    if not restaurants:
        st.warning("⚠️ 找不到附近餐廳。")
    else:
        restaurant_info = "\n".join([f"{r['name']} - {r.get('vicinity', '')}" for r in restaurants])
        st.session_state.restaurant_context = restaurant_info
        st.success("✅ 已載入附近餐廳資訊！")

user_input = st.text_input("你想吃什麼或有什麼偏好？")

if user_input and "restaurant_context" in st.session_state:
    chain_input = {
        "input": user_input,
        "context": st.session_state.restaurant_context
    }
    response = llm_chain.invoke(chain_input)
    st.write(response["text"])

