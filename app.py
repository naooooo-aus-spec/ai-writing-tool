import hmac
import os

import streamlit as st
from dotenv import load_dotenv

from features import (
    blog_writer,
    code_explainer,
    document_creator,
    email_reply,
    summarizer,
    title_generator,
    tone_rewriter,
)

load_dotenv()

st.set_page_config(page_title="AIライティングツール", page_icon="✍️", layout="centered")

FEATURES = {
    "ブログ執筆": blog_writer,
    "メール返信文": email_reply,
    "文章要約": summarizer,
    "資料作成": document_creator,
    "文章リライト・校正": tone_rewriter,
    "タイトル・件名生成": title_generator,
    "コード解説": code_explainer,
}


def check_password() -> bool:
    """APP_PASSWORD との照合。未設定時はスキップ(ローカル利用向けの後方互換)。"""
    app_password = os.environ.get("APP_PASSWORD")
    if not app_password:
        return True

    if st.session_state.get("authenticated"):
        return True

    entered = st.text_input("パスワード", type="password")
    if entered:
        if hmac.compare_digest(entered.encode("utf-8"), app_password.encode("utf-8")):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("パスワードが違います。")
    return False


def main() -> None:
    if not check_password():
        st.stop()

    st.sidebar.title("✍️ AIライティングツール")

    if not os.environ.get("GEMINI_API_KEY"):
        st.sidebar.error("GEMINI_API_KEY が未設定です。.env ファイルを確認してください。")

    choice = st.sidebar.radio("機能を選択", list(FEATURES.keys()))
    st.sidebar.divider()
    st.sidebar.caption("Powered by Gemini API")

    FEATURES[choice].render()


if __name__ == "__main__":
    main()
