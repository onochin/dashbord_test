from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(page_title="売上ダッシュボード", layout="wide")

DATA_PATH = Path(__file__).parent / "csv" / "sales_transactions.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """CSVを読み込み、表示用の型に整える。"""
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m")
    return df


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """サイドバーの条件でデータを絞り込む。"""
    st.sidebar.header("フィルタ")

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    selected_dates = st.sidebar.date_input(
        "日付",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date = end_date = selected_dates

    regions = sorted(df["region"].dropna().unique())
    channels = sorted(df["channel"].dropna().unique())
    categories = sorted(df["product_category"].dropna().unique())

    selected_regions = st.sidebar.multiselect("地域", regions, default=regions)
    selected_channels = st.sidebar.multiselect("チャネル", channels, default=channels)
    selected_categories = st.sidebar.multiselect(
        "商品カテゴリ",
        categories,
        default=categories,
    )

    filtered_df = df[
        (df["date"].dt.date >= start_date)
        & (df["date"].dt.date <= end_date)
        & (df["region"].isin(selected_regions))
        & (df["channel"].isin(selected_channels))
        & (df["product_category"].isin(selected_categories))
    ].copy()

    return filtered_df


def format_yen(value: float) -> str:
    """金額を円表記にする。"""
    return f"¥{value:,.0f}"


def main() -> None:
    st.title("売上ダッシュボード")
    st.caption("sales_transactions.csv を使った学習用のシンプルなダッシュボード")

    if not DATA_PATH.exists():
        st.error(f"CSVファイルが見つかりません: {DATA_PATH}")
        st.stop()

    df = load_data()
    filtered_df = filter_data(df)

    total_revenue = filtered_df["revenue"].sum()
    total_profit = filtered_df["gross_profit"].sum()
    transaction_count = filtered_df["transaction_id"].nunique()

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("総売上", format_yen(total_revenue))
    kpi2.metric("粗利", format_yen(total_profit))
    kpi3.metric("取引件数", f"{transaction_count:,}")

    st.divider()

    monthly_sales = (
        filtered_df.groupby("month", as_index=False)["revenue"]
        .sum()
        .sort_values("month")
    )
    regional_sales = (
        filtered_df.groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue")
    )
    category_sales = (
        filtered_df.groupby("product_category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    chart1, chart2 = st.columns(2)

    with chart1:
        st.subheader("月別売上")
        if monthly_sales.empty:
            st.info("表示できるデータがありません。")
        else:
            st.line_chart(monthly_sales.set_index("month")["revenue"], use_container_width=True)

    with chart2:
        st.subheader("地域別売上")
        if regional_sales.empty:
            st.info("表示できるデータがありません。")
        else:
            st.bar_chart(regional_sales.set_index("region")["revenue"], use_container_width=True)

    st.subheader("カテゴリ別売上")
    if category_sales.empty:
        st.info("表示できるデータがありません。")
    else:
        st.bar_chart(
            category_sales.set_index("product_category")["revenue"],
            use_container_width=True,
        )

    st.subheader("明細表")
    display_df = filtered_df.sort_values("date", ascending=False).copy()
    if not display_df.empty:
        display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
        display_df["month"] = display_df["month"].dt.strftime("%Y-%m")

    st.dataframe(display_df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
