# 売上ダッシュボード

`csv/sales_transactions.csv` を使って表示する、学習用の静的売上ダッシュボードです。`index.html` は GitHub Pages でそのまま公開できます。

## 機能

- サイドバーで日付、地域、チャネル、商品カテゴリをフィルタ
- KPI として総売上、粗利、取引件数を表示
- 月別売上、地域別売上、カテゴリ別売上をグラフ表示
- フィルタ後の明細表を表示

## 実行方法

### GitHub Pages で公開する場合

1. GitHub のリポジトリ設定を開きます。
2. `Pages` を選びます。
3. `Deploy from a branch` を選びます。
4. ブランチは `main`、フォルダは `/ (root)` を選びます。
5. 保存すると、しばらくして `index.html` が公開されます。

### ローカルで確認する場合

`fetch()` で CSV を読むため、`file://` 直開きではなくローカルサーバーを使います。

```bash
cd ~/codex_projects/dashbord/test
python3 -m http.server 8000
```

ブラウザで `http://localhost:8000` を開きます。

## ファイル

- `index.html`: GitHub Pages 用の静的ダッシュボード
- `app.py`: Streamlit 版のダッシュボード
- `requirements.txt`: Streamlit 版の依存関係
- `csv/sales_transactions.csv`: 入力データ

## 補足

- CSV は `utf-8-sig` を想定して読み込みます。
- 集計には `revenue` と `gross_profit`、取引件数には `transaction_id` を使っています。
- GitHub Pages では Python は動かないため、公開用は `index.html` を使います。
