import streamlit as st

from core.gemini_client import MAX_INPUT_CHARS, generate

SYSTEM_INSTRUCTION = """あなたは文章要約の専門家です。
元の文章の重要なポイントを漏らさず、指定された形式・分量で
分かりやすく要約してください。"""

FORMAT_OPTIONS = ["文章形式", "箇条書き"]


def render() -> None:
    st.header("文章要約AI")
    st.caption("長文を貼り付けると、指定した形式・分量で要約します。")

    source_text = st.text_area(
        "要約したい文章",
        height=250,
        placeholder="ここに要約したい文章を貼り付けてください",
        max_chars=MAX_INPUT_CHARS,
    )
    output_format = st.radio("出力形式", FORMAT_OPTIONS, horizontal=True)
    length = st.select_slider(
        "要約の分量",
        options=["ひとこと(1-2文)", "短め(3-4文)", "標準(5-8文)", "詳しめ"],
        value="標準(5-8文)",
    )

    if st.button("要約する", type="primary"):
        if not source_text.strip():
            st.warning("要約したい文章を入力してください。")
            return

        prompt = f"""以下の文章を要約してください。

# 出力形式
{output_format}

# 分量の目安
{length}

# 元の文章
{source_text}"""

        with st.spinner("要約中..."):
            result = generate(prompt, system_instruction=SYSTEM_INSTRUCTION)

        st.markdown("### 要約結果")
        st.markdown(result)
