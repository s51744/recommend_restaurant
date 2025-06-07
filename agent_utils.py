import json
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import re

def get_ai_recommendation(preference, restaurants):
    from langchain_community.chat_models import ChatOllama

    llm = ChatOllama(model="llama3.2", temperature=0.7)

    # 特殊關鍵詞處理
    if "周俊丞" in preference:
        return "周俊丞根本不會想跟你吃飯，你省省吧!"

    # 過濾今日營業的店
    today = datetime.today().strftime("%A")
    open_today = [r for r in restaurants if r["hours"].get(today, "") not in ["休息", "不明"]]

    if not open_today:
        return "今天附近的店都沒開，請稍後再試。"

    # 根據 category 判斷是否有符合使用者需求的類別
    keyword = None
    for r in open_today:
        for cat in r.get("category", []):
            if cat in preference:
                keyword = cat
                break
        if keyword:
            break

    if not keyword:
        return "很抱歉，資料裡沒有符合你需求的餐廳喔！"

    # 根據 category 選出最多三間符合的餐廳
    matched = [r for r in open_today if keyword in r.get("category", [])]
    selected = matched[:3]

    def describe(r):
        hours = ', '.join([f"{day}: {status}" for day, status in r['hours'].items()])
        categories = '、'.join(r.get("category", [])) if r.get("category") else "無標示"
        return (
            f"餐廳名稱：{r['name']}\n"
            f"地址：{r['address']}\n"
            f"類別：{categories}\n"
            f"營業時間：{hours}\n"
            f"價格：約 {r['price']} 元\n"
            f"卡路里：約 {r['calories']} 大卡"
        )

    context = "\n\n".join([describe(r) for r in selected])

    # 正確使用 System + Human Message 分開設定 prompt
    system_template = """
你是一位宜蘭美食推薦助手，請嚴格遵守以下規範產生回應：

1️⃣ 特別關鍵字處理：
如果使用者輸入包含「周俊丞」，請只輸出：
「周俊丞根本不會想跟你吃飯，你省省吧!」
並立刻停止回覆，禁止任何額外內容。

2️⃣ 餐廳推薦規則：
- 只能推薦今天有營業的餐廳
- 僅可推薦 category 欄位中包含使用者輸入關鍵字的餐廳
- 所有推薦資料必須來自 JSON 中提供的內容，不可虛構
- 如無符合餐廳，請只回覆：「很抱歉，資料裡沒有符合你需求的餐廳喔！」

3️⃣ 推薦格式：
- 最多推薦 3 間
- 每間需提供推薦理由（如價格、份量、特色）
- 推薦需有不同風格
- 使用自然、親切、台灣口吻，像在和朋友說話
- 結尾請加：「這幾家都不錯，你想試哪一間呢？」

4️⃣ 嚴禁事項：
- 禁止使用簡體字、英文、emoji
- 不可創造不存在的店名
- 不可同時輸出「找不到」與「推薦」
- 不可說明推理過程，只輸出推薦結果
"""

    human_template = """
以下是今天有營業的餐廳資料，請根據使用者的輸入進行推薦。

<附近餐廳資料>
{context}
</附近餐廳資料>

使用者說：{input}
"""

    # 設定提示模板
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ])

    chain_input = {"input": preference, "context": context}
    messages = prompt.format_messages(**chain_input)
    response = llm.invoke(messages)

    # 去除 Markdown 粗體格式（保險）
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", response.content.strip())
    return cleaned
