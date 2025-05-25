# agent_utils.py

import json
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from datetime import datetime

def get_ai_recommendation(preference, restaurants):
    from langchain.prompts import ChatPromptTemplate
    from langchain_community.chat_models import ChatOllama

    # 初始化 LLM
    llm = ChatOllama(model="llama3.2", temperature=0.7)

    # Step 1: 過濾今日有營業的餐廳
    today = datetime.today().strftime("%A")  # e.g., 'Monday'
    open_today = [r for r in restaurants if r["hours"].get(today, "") not in ["休息", "不明"]]

    # 若沒有符合的店家，回傳提示
    if not open_today:
        return "今天沒有符合條件的餐廳喔！"

    # Step 2: 整理格式提供給模型
    def describe(r):
        hours = ', '.join([f"{day}: {status}" for day, status in r['hours'].items()])
        return f"餐廳名稱：{r['name']}\n地址：{r['address']}\n營業時間：{hours}\n平均價格：{r['price']} 元\n預估卡路里：{r['calories']} 大卡"

    context = "\n\n".join([describe(r) for r in open_today])

    # Step 3: 提示詞
    template = ChatPromptTemplate.from_template("""
你是一個美食推薦助理，請根據下列附近餐廳資料與使用者需求推薦餐廳。
請綜合考量「價格（根據使用者偏好）」與「當天是否有營業」。

<餐廳資料>
{context}
</餐廳資料>

使用者說：{input}
你的回應：
""")

    chain_input = {"input": preference, "context": context}
    response = llm.invoke(template.format(**chain_input))
    return response.content.strip()
