import streamlit as st

from core.gemini_client import MAX_INPUT_CHARS, generate

SYSTEM_INSTRUCTION = """あなたはプロのブログライターです。
読者にとって読みやすく、具体的で価値のある文章を書きます。
指示された条件(テーマ、トーン、文字数、見出し構成など)を守って、
Markdown形式でブログ記事の下書きを作成してください。"""

TONE_OPTIONS = ["丁寧・フォーマル", "カジュアル・親しみやすい", "熱意のある・情熱的", "客観的・専門的"]


def render() -> None:
    st.header("ブログ執筆AI")
    st.caption("テーマや条件を入力すると、ブログ記事の下書きを生成します。")

    theme = st.text_input("テーマ・タイトル案", placeholder="例: リモートワークの生産性を上げる方法")
    keywords = st.text_input("含めたいキーワード(カンマ区切り・任意)", placeholder="例: 集中力, ツール, 習慣")
    tone = st.selectbox("トーン", TONE_OPTIONS)
    length = st.slider("目安の文字数", 300, 3000, 1000, step=100)
    outline = st.text_area(
        "構成の希望(任意)",
        placeholder="例: 導入 → 課題 → 解決策3つ → まとめ",
        height=80,
        max_chars=MAX_INPUT_CHARS,
    )

    if st.button("ブログ記事を生成", type="primary"):
        if not theme.strip():
            st.warning("テーマを入力してください。")
            return

        prompt = f"""以下の条件でブログ記事の下書きをMarkdown形式で書いてください。

テーマ: {theme}
キーワード: {keywords or "指定なし"}
トーン: {tone}
目安の文字数: {length}文字
構成の希望: {outline or "おまかせ"}

見出し(##)を適切に使い、読みやすい段落分けをしてください。"""

        with st.spinner("生成中..."):
            result = generate(prompt, system_instruction=SYSTEM_INSTRUCTION)

        st.markdown("### 生成結果")
        st.markdown(result)
        st.download_button("Markdownでダウンロード", result, file_name="blog_draft.md")
