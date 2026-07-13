import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="Global Top10 Stocks Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🌍 Global Market Cap TOP10 Dashboard")
st.write("최근 1년간 글로벌 시가총액 상위 기업들의 주가를 비교합니다.")

# -----------------------------
# 기업 목록
# -----------------------------
stocks = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Meta": "META",
    "Broadcom": "AVGO",
    "Tesla": "TSLA",
    "Berkshire Hathaway": "BRK-B",
    "TSMC": "TSM"
}

selected = st.sidebar.multiselect(
    "기업 선택",
    list(stocks.keys()),
    default=["Apple", "Microsoft", "NVIDIA"]
)

chart_type = st.sidebar.selectbox(
    "차트 종류",
    ["주가", "수익률"]
)

# -----------------------------
# 데이터 다운로드
# -----------------------------
@st.cache_data
def load_stock(ticker):
    end = datetime.today()
    start = end - timedelta(days=365)

    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False
    )

    return df

plot_df = pd.DataFrame()

metrics = st.columns(max(1, len(selected)))

for i, company in enumerate(selected):

    ticker = stocks[company]
    df = load_stock(ticker)

    if df.empty:
        continue

    close = df["Close"].copy()

    if chart_type == "수익률":
        close = (close / close.iloc[0] - 1) * 100

    temp = pd.DataFrame({
        "Date": df.index,
        "Value": close.values,
        "Company": company
    })

    plot_df = pd.concat([plot_df, temp], ignore_index=True)

    price = float(df["Close"].iloc[-1])
    change = (float(df["Close"].iloc[-1]) / float(df["Close"].iloc[0]) - 1) * 100

    metrics[i].metric(
        company,
        f"${price:,.2f}",
        f"{change:.2f}%"
    )

# -----------------------------
# Plotly 그래프
# -----------------------------
if not plot_df.empty:

    ylabel = "Price (USD)" if chart_type == "주가" else "Return (%)"

    fig = px.line(
        plot_df,
        x="Date",
        y="Value",
        color="Company"
    )

    fig.update_layout(
        height=650,
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title=ylabel
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("데이터를 불러올 수 없습니다.")

# -----------------------------
# 테이블
# -----------------------------
st.subheader("주가 정보")

table = []

for company in selected:

    ticker = stocks[company]
    df = load_stock(ticker)

    if df.empty:
        continue

    price = float(df["Close"].iloc[-1])
    change = (price / float(df["Close"].iloc[0]) - 1) * 100

    table.append({
        "Company": company,
        "Ticker": ticker,
        "Current Price($)": round(price,2),
        "1Y Return(%)": round(change,2)
    })

st.dataframe(
    pd.DataFrame(table),
    use_container_width=True
)

st.caption("Data Source : Yahoo Finance")
