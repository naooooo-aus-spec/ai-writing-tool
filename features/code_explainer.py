import streamlit as st

from core.gemini_client import MAX_INPUT_CHARS, generate

SYSTEM_INSTRUCTION = """あなたはコードレビューと解説の専門家です。
与えられたコードの処理内容を、指定された詳細度に応じて
分かりやすく日本語で解説してください。"""

DETAIL_OPTIONS = ["概要のみ(全体の流れ)", "標準(処理を行ごとに解説)", "詳しく(初心者向けに丁寧に)"]


def render() -> None:
    st.header("コード解説AI")
    st.caption("コードを貼り付けると、処理内容を日本語で解説します。")

    source_code = st.text_area(
        "解説したいコード",
        height=300,
        placeholder="ここにコードを貼り付けてください",
        max_chars=MAX_INPUT_CHARS,
    )
    detail = st.radio("解説の詳しさ", DETAIL_OPTIONS, horizontal=True)

    if st.button("解説する", type="primary"):
        if not source_code.strip():
            st.warning("解説したいコードを入力してください。")
            return

        prompt = f"""以下のコードを解説してください。

# 解説の詳しさ
{detail}

# コード
{source_code}"""

        with st.spinner("解説中..."):
            result = generate(prompt, system_instruction=SYSTEM_INSTRUCTION)

        st.markdown("### 解説結果")
        st.markdown(result)
