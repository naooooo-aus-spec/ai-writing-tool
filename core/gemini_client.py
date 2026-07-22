import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types

load_dotenv()

DEFAULT_MODEL = "gemini-3.1-flash-lite"

MAX_REQUESTS_PER_WINDOW = 20
WINDOW_SECONDS = 3600

MAX_INPUT_CHARS = 8000


@st.cache_resource
def get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY が設定されていません。.env ファイルに設定してください。"
        )
    return genai.Client(api_key=api_key)


def _enforce_rate_limit() -> None:
    now = time.time()
    recent = [t for t in st.session_state.get("_request_times", []) if now - t < WINDOW_SECONDS]
    if len(recent) >= MAX_REQUESTS_PER_WINDOW:
        st.error(
            f"リクエスト数の上限({MAX_REQUESTS_PER_WINDOW}回/時間)に達しました。"
            "しばらく時間をおいてから再度お試しください。"
        )
        st.stop()
    recent.append(now)
    st.session_state["_request_times"] = recent


def generate(
    prompt: str,
    system_instruction: str | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
) -> str:
    _enforce_rate_limit()
    try:
        client = get_client()
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        )
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
        return response.text or ""
    except RuntimeError as e:
        st.error(str(e))
    except genai_errors.ClientError:
        st.error(
            "AIへのリクエストが拒否されました。APIキーが正しいか、"
            "利用上限に達していないかを確認してください。"
        )
    except genai_errors.ServerError:
        st.error("AIサービス側で問題が発生しています。しばらくしてから再度お試しください。")
    except Exception as e:
        print(f"[gemini_client] unexpected error: {e!r}")
        st.error("予期しないエラーが発生しました。ネットワーク接続を確認し、しばらくしてから再度お試しください。")
    st.stop()
    raise AssertionError("unreachable")  # st.stop() は例外を送出しスクリプトを終了させる
