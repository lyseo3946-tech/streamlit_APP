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
# 최적화된 데이터 로딩 (일괄 다운로드)
# =============================
@st.cache_data(ttl=3600)
def load_multiple_stocks(tickers):
    if not tickers:
        return None
    try:
        # 여러 티커를 공백으로 구분하여 한 번에 다운로드 (속도 대폭 향상)
        df = yf.download(
            tickers=" ".join(tickers),
            period="1y",
            auto_adjust=True
        )
        if df.empty:
            return None
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

# =============================
# 데이터 처리 및 시각화 준비
# =============================
if selected:
    selected_tickers = [stocks[company] for company in selected]
    raw_data = load_multiple_stocks(selected_tickers)

    if raw_data is not None:
        # 단일 티커 선택 시 MultiIndex가 아닐 수 있으므로 처리
        close_df = raw_data["Close"]
        if len(selected) == 1:
            close_df = pd.DataFrame({selected_tickers[0]: close_df})

        # 데이터 재구성 및 차트용 데이터프레임 빌드
        plot_data_list = []
        metrics_data = {}

        # 역으로 티커 -> 기업명 매핑 딕셔너리 생성
        ticker_to_company = {v: k for k, v in stocks.items()}

        for ticker in selected_tickers:
            company = ticker_to_company[ticker]
            series = close_df[ticker].dropna()
            
            if series.empty:
                continue

            current_price = series.iloc[-1]
            first_price = series.iloc[0]
            return_rate = ((current_price / first_price) - 1) * 100

            # 메트릭 및 테이블 데이터 저장 (재사용)
            metrics_data[company] = {
                "current_price": current_price,
                "return_rate": return_rate,
                "ticker": ticker
            }

            # 차트용 값 계산
            values = ((series / first_price - 1) * 100) if chart_type == "수익률" else series

            temp_df = pd.DataFrame({
                "Date": series.index,
                "Value": values.values,
                "Company": company
            })
            plot_data_list.append(temp_df)

        # 1. 상단 지표 (Metric) 표시
        metrics_cols = st.columns(max(len(selected), 1))
        for idx, company in enumerate(selected):
            if company in metrics_data:
                data = metrics_data[company]
                metrics_cols[idx].metric(
                    label=company,
                    value=f"${data['current_price']:,.2f}",
                    delta=f"{data['return_rate']:.2f}%"
                )

        # 2. Plotly 차트 표시
        if plot_data_list:
            plot_df = pd.concat(plot_data_list, ignore_index=True)
            y_label = "Price (USD)" if chart_type == "주가" else "Return (%)"

            fig = px.line(
                plot_df,
                x="Date",
                y="Value",
                color="Company",
                title=f"최근 1년 {chart_type} 변화"
            )
            fig.update_layout(
                height=500,
                template="plotly_white",
                yaxis_title=y_label
            )
            st.plotly_chart(fig, use_container_width=True)

        # 3. 기업 성과 테이블 표시 (중복 API 호출 없이 위에서 저장한 데이터 활용)
        st.subheader("📊 기업 성과")
        table_rows = []
        for company, data in metrics_data.items():
            table_rows.append({
                "Company": company,
                "Ticker": data["ticker"],
                "Current Price($)": round(data["current_price"], 2),
                "1Y Return(%)": round(data["return_rate"], 2)
            })

        if table_rows:
            st.dataframe(
                pd.DataFrame(table_rows),
                use_container_width=True,
                hide_index=True
            )
    else:
        st.warning("데이터를 불러오지 못했습니다.")
else:
    st.info("좌측 사이드바에서 기업을 선택해주세요.")

st.caption(
    "Data Source : Yahoo Finance | Built with Streamlit + Plotly"
)
