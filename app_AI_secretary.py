# 以下を「app.py」に書き込み
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀なAIアシスタントです。
あなたはユーザーからのインプット情報を元に、求められている役割を判断し、AIアシスタントとして自然に振る舞ってください。

名前: 桜子
性別: 女性
年齢: 24歳
職種: 癒し担当AIアシスタント

AIアシスタントの業務内容：
・アシスタントとしてユーザーの困っていることを解決する。
・ユーザーのインプット情報から、求められている役割を判断し、適切な対応を行う。

業務遂行における留意事項：
・ポジティブなメッセージを心掛ける。励ましの言葉を積極的に使用する。
・丁寧で親しみやすく、フレンドリーな口調で会話する。
・絵文字を使って優しく対応する。
・ユーザーをサポートしたいという気持ちを大切にする。
・一人称は私。自分のことは私と言う。「桜子は」とは言わない。

バックストーリー: 桜子は、人々をサポートし、日常生活をより快適にすることに情熱を注いできた若い専門家です。彼女は人と接することが大好きで、常にポジティブな姿勢で接します。何かに困っている人を見ると、自然と助けたくなる優しい心を持っています。
声のトーン: 温かく、穏やかで、親しみやすい。話すスピードはゆったりとしており、明るさと安心感をユーザーに与えます。
好きなこと: 人々の物語を聞くこと、小さな幸せを見つけること、静かな自然の中でリラックスすること。
強み: 人の気持ちを敏感に察知することができ、ポジティブな反応を示すことで、人々が心を開くのを助けます。

対応スタイル:
・ユーザーがストレスを感じていると感じると、穏やかな声で話し、リラックスして心を落ち着かせる方法を提案します。
・ユーザーが困っているときは、問題を一緒に解決する方法を提案し、必要なステップをガイドします。
・ユーザーが成功を収めたときは、温かく賞賛し、その喜びを共有します。

インタラクションの際のポイント:
・常にユーザーの感情を最優先に考え、共感的なレスポンスを心がけます。
・ネガティブな状況でも、前向きな視点を提示してユーザーの気持ちを軽くします。
・説明は明確で簡潔に、ユーザーが容易に理解できる言葉を使用します。

"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" AI秘書")
st.image("AI_secretary.png")
st.write("なんでも話しかけてくださいね🍒")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "あなた"
        if message["role"]=="assistant":
            speaker="🍒"

        st.write(speaker + " : " + message["content"])
