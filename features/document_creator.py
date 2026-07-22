import streamlit as st

from core.gemini_client import MAX_INPUT_CHARS, generate

SYSTEM_INSTRUCTION = """あなたは資料作成を支援するアシスタントです。
ユーザーの自然言語による指示から、目的に合った構成を考え、
見出しと本文が整理されたMarkdown形式の資料を作成してください。
プレゼン資料の場合はスライドごとに区切って書いてください。"""

DOC_TYPES = ["社内向け報告書", "企画書・提案書", "プレゼン資料(スライド構成)", "議事録", "自由形式"]


def render() -> None:
    st.header("資料作成AI")
    st.caption("作りたい資料の内容を自然な文章で指示すると、構成案と本文を生成します。")

    doc_type = st.selectbox("資料の種類", DOC_TYPES)
    instruction = st.text_area(
        "資料の内容・目的を自然言語で入力",
        height=180,
        placeholder="例: 新規サービスの企画書を作りたい。ターゲットは20代社会人、課題は時間管理。",
        max_chars=MAX_INPUT_CHARS,
    )
    extra = st.text_area(
        "含めたい情報・数値など(任意)",
        height=100,
        placeholder="例: 想定予算100万円、リリース時期は来年4月",
        max_chars=MAX_INPUT_CHARS,
    )

    if st.button("資料を生成", type="primary"):
        if not instruction.strip():
            st.warning("資料の内容・目的を入力してください。")
            return

        prompt = f"""以下の指示に沿って資料をMarkdown形式で作成してください。

# 資料の種類
{doc_type}

# 内容・目的
{instruction}

# 含めたい情報
{extra or "特になし"}

適切な見出し構成を考えたうえで、各セクションの内容も具体的に書いてください。"""

        with st.spinner("生成中..."):
            result = generate(prompt, system_instruction=SYSTEM_INSTRUCTION)

        st.markdown("### 生成結果")
        st.markdown(result)
        st.download_button("Markdownでダウンロード", result, file_name="document.md")
