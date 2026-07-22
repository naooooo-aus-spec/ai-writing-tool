import streamlit as st

from core.gemini_client import MAX_INPUT_CHARS, generate

SYSTEM_INSTRUCTION = """あなたはビジネスメールの返信作成を支援するアシスタントです。
受信メールの内容を正しく理解し、日本語のビジネスマナーに沿った
自然で失礼のない返信文を作成してください。"""

TONE_OPTIONS = ["丁寧・フォーマル(社外向け)", "標準的・社内向け", "親しみやすい・カジュアル", "簡潔・要点のみ"]


def render() -> None:
    st.header("メール返信文AI")
    st.caption("受信したメールの内容を貼り付けると、返信文の候補を生成します。")

    received_mail = st.text_area(
        "受信したメールの本文",
        height=200,
        placeholder="ここに受信メールの本文を貼り付けてください",
        max_chars=MAX_INPUT_CHARS,
    )
    intent = st.text_area(
        "返信で伝えたい内容(箇条書きでOK)",
        height=100,
        placeholder="例: 日程は来週火曜14時でOK。資料は事前に送ってほしい。",
        max_chars=MAX_INPUT_CHARS,
    )
    tone = st.selectbox("トーン", TONE_OPTIONS)

    if st.button("返信文を生成", type="primary"):
        if not received_mail.strip():
            st.warning("受信メールの本文を入力してください。")
            return

        prompt = f"""以下の受信メールに対する返信文を作成してください。

# 受信メール
{received_mail}

# 返信で伝えたい内容
{intent or "受信メールの内容に対して適切にお礼・回答する"}

# トーン
{tone}

件名案も含めて、そのまま送信できる形式で1つの返信文を出力してください。"""

        with st.spinner("生成中..."):
            result = generate(prompt, system_instruction=SYSTEM_INSTRUCTION)

        st.markdown("### 生成結果")
        st.text_area("返信文(コピーしてお使いください)", result, height=300)
