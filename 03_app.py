import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


st.set_page_config(
    page_title="서울 공영주차장 지도",
    layout="wide"
)


st.title("🚗 서울시 유료 공영주차장 지도")


# -----------------------------
# 데이터 읽기 (캐싱)
# -----------------------------

@st.cache_data
def load_data(file):

    if file.name.endswith(".csv"):

        try:
            return pd.read_csv(
                file,
                encoding="utf-8"
            )

        except:
            return pd.read_csv(
                file,
                encoding="cp949"
            )

    else:

        return pd.read_excel(file)



# -----------------------------
# 파일 업로드
# -----------------------------

file = st.file_uploader(
    "공영주차장 데이터 업로드",
    type=["csv", "xlsx"]
)


if file is None:
    st.info("파일을 업로드하세요.")
    st.stop()



df = load_data(file)



st.success(
    f"데이터 {len(df):,}건 로드 완료"
)



# 너무 큰 데이터 보호
if len(df) > 50000:

    st.warning(
        "데이터가 커서 처음 50,000개만 분석합니다."
    )

    df = df.head(50000)



# -----------------------------
# 컬럼 선택
# -----------------------------

st.subheader("컬럼 설정")


cols = list(df.columns)


name_col = st.selectbox(
    "주차장명",
    cols
)


gu_col = st.selectbox(
    "자치구",
    cols
)


lat_col = st.selectbox(
    "위도(Y)",
    cols
)


lon_col = st.selectbox(
    "경도(X)",
    cols
)


fee_col = st.selectbox(
    "요금",
    cols
)



# -----------------------------
# 데이터 변환
# -----------------------------


df[lat_col] = pd.to_numeric(
    df[lat_col],
    errors="coerce"
)


df[lon_col] = pd.to_numeric(
    df[lon_col],
    errors="coerce"
)



df["요금숫자"] = (
    df[fee_col]
    .astype(str)
    .str.extract(r"(\d+)")
)


df["요금숫자"] = pd.to_numeric(
    df["요금숫자"],
    errors="coerce"
)



df = df.dropna(
    subset=[
        lat_col,
        lon_col
    ]
)



# -----------------------------
# 유료 주차장만
# -----------------------------


paid = df[
    df["요금숫자"] > 0
].copy()



if paid.empty:

    st.error(
        "유료 주차장을 찾지 못했습니다."
    )

    st.stop()



st.success(
    f"유료 주차장 {len(paid):,}개"
)



# -----------------------------
# 자치구 선택
# -----------------------------


gu_list = sorted(
    paid[gu_col]
    .dropna()
    .astype(str)
    .unique()
)



selected_gu = st.selectbox(
    "자치구 선택",
    gu_list
)



result = paid[
    paid[gu_col].astype(str)
    == selected_gu
]



# -----------------------------
# 요금 필터
# -----------------------------


max_fee = int(
    result["요금숫자"].max()
)


fee = st.slider(
    "최대 기본요금",
    0,
    max_fee,
    max_fee
)



result = result[
    result["요금숫자"] <= fee
]



st.write(
    f"검색 결과 : {len(result)}개"
)



# -----------------------------
# 지도 생성
# -----------------------------


center = [
    result[lat_col].mean(),
    result[lon_col].mean()
]


m = folium.Map(
    location=center,
    zoom_start=12
)



# ★ 중요: 지도 마커 최대 300개 제한
map_data = result.head(300)



for _, row in map_data.iterrows():

    popup = f"""
    <b>{row[name_col]}</b><br>
    자치구 : {row[gu_col]}<br>
    요금 : {row[fee_col]}
    """


    folium.CircleMarker(
        location=[
            row[lat_col],
            row[lon_col]
        ],
        radius=6,
        popup=popup,
        color="red",
        fill=True,
        fill_color="red"
    ).add_to(m)



st.caption(
    "지도에는 최대 300개 주차장만 표시됩니다."
)



st_folium(
    m,
    width=900,
    height=550
)



# -----------------------------
# 표 출력
# -----------------------------


st.subheader("주차장 목록")


show_cols = [
    name_col,
    gu_col,
    fee_col
]


st.dataframe(
    result[show_cols],
    height=400
)
