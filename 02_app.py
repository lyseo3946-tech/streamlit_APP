import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px


# =============================
# 페이지 설정
# =============================
st.set_page_config(
    page_title="Global Top10 Stocks Dashboard",
    page_icon="📈",
    layout="wide"
)


st.title("🌍 Global Market Cap TOP10 Dashboard")
st.write(
    "최근 1년간 글로벌 시가총액 상위 기업들의 주가 변화를 비교합니다."
)


# =============================
# 글로벌 TOP10 기업
# =============================
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


# =============================
# 사이드바
# =============================
selected = st.sidebar.multiselect(
    "기업 선택",
    list(stocks.keys()),
    default=[
        "Apple",
        "Microsoft",
        "NVIDIA"
    ]
)


chart_type = st.sidebar.selectbox(
    "차트 종류",
    [
        "주가",
        "수익률"
    ]
)



# =============================
# 데이터 로딩
# =============================
@st.cache_data(ttl=3600)
def load_stock(ticker):

    try:

        stock = yf.Ticker(ticker)

        df = stock.history(
            period="1y",
            auto_adjust=True
        )


        if df.empty:
            return None


        df = df.reset_index()


        return df


    except Exception:
        return None



# =============================
# 차트 데이터 생성
# =============================

plot_df = pd.DataFrame()

metrics = st.columns(max(len(selected), 1))


for i, company in enumerate(selected):


    ticker = stocks[company]


    df = load_stock(ticker)


    if df is None:
        continue


    close = df["Close"].astype(float)


    # 수익률 계산
    if chart_type == "수익률":

        value = (
            close / close.iloc[0] - 1
        ) * 100

    else:

        value = close



    temp = pd.DataFrame({

        "Date": df["Date"],

        "Value": value.values,

        "Company": company

    })


    plot_df = pd.concat(
        [
            plot_df,
            temp
        ],
        ignore_index=True
    )


    current_price = close.iloc[-1]


    return_rate = (
        close.iloc[-1]
        /
        close.iloc[0]
        -
        1
    ) * 100



    metrics[i].metric(

        label=company,

        value=f"${current_price:,.2f}",

        delta=f"{return_rate:.2f}%"

    )



# =============================
# Plotly 차트
# =============================

if not plot_df.empty:


    y_label = (
        "Price (USD)"
        if chart_type == "주가"
        else "Return (%)"
    )


    fig = px.line(

        plot_df,

        x="Date",

        y="Value",

        color="Company",

        title=f"최근 1년 {chart_type} 변화"

    )


    fig.update_layout(

        height=650,

        template="plotly_white"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


else:

    st.warning(
        "주가 데이터를 불러오지 못했습니다."
    )



# =============================
# 테이블
# =============================

st.subheader("📊 기업 성과")


table = []


for company in selected:


    ticker = stocks[company]


    df = load_stock(ticker)


    if df is None:
        continue


    close = df["Close"].astype(float)


    price = close.iloc[-1]


    change = (
        close.iloc[-1]
        /
        close.iloc[0]
        -
        1
    ) * 100



    table.append({

        "Company": company,

        "Ticker": ticker,

        "Current Price($)": round(
            float(price),
            2
        ),

        "1Y Return(%)": round(
            float(change),
            2
        )

    })



if table:

    st.dataframe(

        pd.DataFrame(table),

        use_container_width=True,

        hide_index=True

    )


else:

    st.info(
        "표시할 데이터가 없습니다."
    )



st.caption(
    "Data Source : Yahoo Finance | Built with Streamlit + Plotly"
)
