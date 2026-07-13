import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="글로벌 TOP 10 주식 대시보드",
    page_icon="📈",
    layout="wide"
)

st.title("🌐 글로벌 시가총액 TOP 10 주식 데이터 분석")
st.markdown("최근 1년 동안의 글로벌 주요 기업들의 주가 변화를 실시간으로 확인하세요.")

# 2. 글로벌 시가총액 주요 TOP 10 기업 티커 정의 (yfinance 연동 기준)
COMPANIES = {
    "NVIDIA (NVDA)": "NVDA",
    "Apple (AAPL)": "AAPL",
    "Alphabet / Google (GOOGL)": "GOOGL",
    "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN",
    "TSMC (TSM)": "TSM",
    "Broadcom (AVGO)": "AVGO",
    "Meta Platforms (META)": "META",
    "Tesla (TSLA)": "TSLA",
    "Berkshire Hathaway (BRK-B)": "BRK-B"
}

# 3. 사이드바 구성 (사용자 인터페이스)
st.sidebar.header("⚙️ 대시보드 설정")

# 기업 다중 선택 기능 (기본값으로 전체 선택)
selected_companies = st.sidebar.multiselect(
    "시각화할 기업을 선택하세요:",
    options=list(COMPANIES.keys()),
    default=list(COMPANIES.keys())
)

# 데이터 캐싱 처리 (속도 향상 및 API 호출 최적화)
@st.cache_data(ttl=3600)  # 1시간 동안 캐시 유지
def load_stock_data(tickers):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) # 최근 1년
    
    combined_df = pd.DataFrame()
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            if not df.empty:
                # 수정종가(Close) 기준으로 수익률 계산을 위해 저장
                combined_df[name] = df['Close']
        except Exception as e:
            st.sidebar.error(f"{name} 데이터를 불러오는 중 오류 발생: {e}")
            
    # 날짜 인덱스를 표준 형식으로 정리
    combined_df.index = combined_df.index.date
    return combined_df

# 데이터 로드 실행
if selected_companies:
    tickers_to_fetch = {name: COMPANIES[name] for name in selected_companies}
    with st.spinner("야후 파이낸스에서 실시간 주가 데이터를 가져오는 중..."):
        data = load_stock_data(tickers_to_fetch)
    
    # 4. 데이터 시각화 섹션
    if not data.empty:
        # --- 시각화 종류 선택 (라디오 버튼) ---
        chart_type = st.radio(
            "차트 종류 선택:",
            ("단순 주가 변화 ($)", "누적 수익률 변화 (%)"),
            horizontal=True
        )

        # Plotly 차트 생성
        fig = go.Figure()

        if chart_type == "단순 주가 변화 ($)":
            for col in data.columns:
                fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=col))
            fig.update_layout(
                yaxis_title="주가 (USD)",
                hovermode="x unified"
            )
        
        elif chart_type == "누적 수익률 변화 (%)":
            # 1년 전 첫 거래일 주가를 0% 기준으로 잡고 누적 수익률 계산
            normalized_data = (data / data.iloc[0] - 1) * 100
            for col in normalized_data.columns:
                fig.add_trace(go.Scatter(x=normalized_data.index, y=normalized_data[col], mode='lines', name=col))
            fig.update_layout(
                yaxis_title="누적 수익률 (%)",
                hovermode="x unified"
            )

        # 공통 레이아웃 트윅
        fig.update_layout(
            title=f"최근 1년간 주가 추이 ({chart_type})",
            xaxis_title="날짜",
            template="plotly_white",
            height=600,
            legend=dict(orient="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Streamlit 화면에 차트 출력
        st.plotly_chart(fig, use_container_width=True)

        # 5. 하단 데이터 테이블 보여주기
        st.subheader("📊 최근 주가 데이터 표")
        st.dataframe(data.tail(10), use_container_width=True)
        
    else:
        st.warning("선택한 기업의 데이터를 불러오지 못했습니다.")
else:
    st.info("왼쪽 사이드바에서 기업을 하나 이상 선택해 주세요.")
