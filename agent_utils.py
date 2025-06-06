import json
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
import re

def get_ai_recommendation(preference, restaurants):
    from langchain_community.chat_models import ChatOllama

    llm = ChatOllama(model="llama3.2", temperature=0.7)

    today = datetime.today().strftime("%A")
    open_today = [r for r in restaurants if r["hours"].get(today, "") not in ["休息", "不明"]]

    if not open_today:
        return "今天附近的店都沒開，請稍後再試。"

    keywords = ["拉麵", "便當", "飯", "麵", "燒肉", "鍋", "雞排", "壽司", "餃子", "義大利", "炸", "咖哩"]
    matched_keyword = next((kw for kw in keywords if kw in preference), None)

    # 加強嚴格：只要不含關鍵字的就排在後面
    if matched_keyword:
        keyword_matched = [
            r for r in open_today
            if matched_keyword in r["name"] or matched_keyword in r["address"]
        ]
        if not keyword_matched:
            return f"找不到和「{matched_keyword}」有關的餐廳喔，換個說法試試看？"

        selected = keyword_matched[:3]
    else:
        selected = open_today[:3]

    def describe(r):
        hours = ', '.join([f"{day}: {status}" for day, status in r['hours'].items()])
        return (
            f"餐廳名稱：{r['name']}\n"
            f"地址：{r['address']}\n"
            f"營業時間：{hours}\n"
            f"價格：約 {r['price']} 元\n"
            f"卡路里：約 {r['calories']} 大卡"
        )

    context = "\n\n".join([describe(r) for r in selected])

    template = ChatPromptTemplate.from_template("""
你是一位熟悉宜蘭在地美食的推薦助手，請根據使用者輸入與下方餐廳資料，推薦最多三間餐廳。
推薦要有理由，每間風格盡量不同（如價位、口味、份量等）。
語氣自然、清楚，不需過度嘴砲或太冷冰冰。
最後請加一句自然的結尾，例如「這幾家都不錯，你想試哪一間呢？」
請用**繁體中文**回答，**不要使用簡體字**。

<附近餐廳資料>
{context}
</附近餐廳資料>

使用者說：{input}
""")

    chain_input = {"input": preference, "context": context}
    response = llm.invoke(template.format(**chain_input))

    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", response.content.strip())
    return cleaned
