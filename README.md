# AIライティングツール

個人用のAIライティング支援ツールです。Gemini APIとStreamlitで動いています。

## 機能

- ブログ執筆
- メール返信文作成
- 文章要約
- 資料作成(自然言語の指示から構成・本文を生成)
- 文章リライト・校正
- タイトル・件名生成

## セットアップ

1. 依存パッケージをインストール

   ```
   pip install -r requirements.txt
   ```

2. `.env.example` を `.env` にコピーし、Gemini APIキーを設定

   ```
   GEMINI_API_KEY=your_api_key_here
   ```

   APIキーは https://aistudio.google.com/apikey から取得できます。

3. アプリを起動

   ```
   streamlit run app.py
   ```

## 構成

```
app.py                    # Streamlitエントリーポイント(サイドバーで機能切り替え)
core/gemini_client.py      # Gemini API呼び出しの共通処理
features/                  # 各機能ごとのUI・プロンプト定義
```
