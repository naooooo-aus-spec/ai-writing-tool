import streamlit as st

from core.gemini_client import MAX_INPUT_CHARS, generate

SYSTEM_INSTRUCTION = """あなたはコピーライティングの専門家です。
内容を的確に表しつつ、読者の興味を引くタイトル・件名案を複数考えてください。"""


def render() -> None:
    st.header("タイトル・件名生成AI")
    st.caption("文章の内容やテーマから、タイトルや件名の案を複数生成します。")

    content = st.text_area(
        "内容・本文・テーマ",
        height=200,
        placeholder="タイトルを付けたい本文、または内容の概要を入力してください",
        max_chars=MAX_INPUT_CHARS,
    )
    style = st.selectbox(
        "スタイル",
        ["ブログ記事タイトル", "メール件名", "SNS投稿の見出し", "資料・書類のタイトル"],
    )
    count = st.slider("生成する案の数", 3, 10, 5)

    if st.button("タイトル案を生成", type="primary"):
        if not content.strip():
            st.warning("内容・テーマを入力してください。")
            return

        prompt = f"""以下の内容に対して、「{style}」として使えるタイトル・件名案を{count}個、
箇条書きで提案してください。それぞれ簡単な一言コメントを添えてください。

# 内容
{content}"""

        with st.spinner("生成中..."):
            result = generate(prompt, system_instruction=SYSTEM_INSTRUCTION)

        st.markdown("### 生成結果")
        st.markdown(result)
