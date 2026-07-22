import streamlit as st

from core.gemini_client import MAX_INPUT_CHARS, generate

SYSTEM_INSTRUCTION = """あなたは文章のリライトと校正の専門家です。
意味内容を変えずに、指定されたトーンへの変換や誤字脱字・言い回しの
改善を行ってください。"""

TONE_OPTIONS = [
    "そのまま校正のみ(誤字脱字・言い回し改善)",
    "丁寧・フォーマルに",
    "カジュアル・親しみやすく",
    "簡潔に短く",
    "より詳しく・丁寧に",
]


def render() -> None:
    st.header("文章リライト・校正AI")
    st.caption("文章を貼り付けて、トーン変換や校正を行います。")

    source_text = st.text_area(
        "リライトしたい文章",
        height=200,
        placeholder="ここに文章を貼り付けてください",
        max_chars=MAX_INPUT_CHARS,
    )
    tone = st.selectbox("変換したいトーン", TONE_OPTIONS)

    if st.button("リライトする", type="primary"):
        if not source_text.strip():
            st.warning("文章を入力してください。")
            return

        prompt = f"""以下の文章を「{tone}」の方針でリライトしてください。
意味内容や事実関係は変えないでください。

# 元の文章
{source_text}"""

        with st.spinner("リライト中..."):
            result = generate(prompt, system_instruction=SYSTEM_INSTRUCTION)

        st.markdown("### リライト結果")
        st.text_area("結果", result, height=250)
