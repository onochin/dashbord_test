# 売上ダッシュボード

`csv/sales_transactions.csv` を使って表示する、学習用の Streamlit 売上ダッシュボードです。

## 機能

- サイドバーで日付、地域、チャネル、商品カテゴリをフィルタ
- KPI として総売上、粗利、取引件数を表示
- 月別売上、地域別売上、カテゴリ別売上をグラフ表示
- フィルタ後の明細表を表示

## 実行方法

1. 仮想環境の作成と必要なライブラリのインストール

```bash
cd ~/codex_projects/dashbord
uv venv
uv pip install -r test/requirements.txt
```

2. アプリの起動

```bash
cd ~/codex_projects/dashbord/test
uv run streamlit run app.py
```

番外: `streamlit run app.py` で実行する場合は、`test` ディレクトリで親階層の仮想環境を読み込みます。

```bash
cd ~/codex_projects/dashbord/test
source ../.venv/bin/activate
streamlit run app.py
```

## ファイル

- `app.py`: ダッシュボード本体
- `csv/sales_transactions.csv`: 入力データ

## 補足

- CSV は `utf-8-sig` を想定して読み込みます。
- 集計には `revenue` と `gross_profit`、取引件数には `transaction_id` を使っています。
