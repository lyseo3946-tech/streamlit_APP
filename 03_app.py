import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


st.set_page_config(
    page_title="서울 공영주차장 지도",
    layout="wide"
)

st.title("🚗 서울시 공영주차장 요금 지도")


# -------------------------
# 파일 업로드
# -------------------------

file = st.file_uploader(
    "서울시 공영주차장 데이터 업로드",
    type=["csv", "xlsx"]
)


if file is None:
    st.info("파일을 업로드하세요.")
    st.stop()


# -------------------------
# 파일 읽기
# -------------------------

try:

    if file.name.endswith(".csv"):

        try:
            df = pd.read_csv(
                file,
                encoding="utf-8"
            )

        except:
            df = pd.read_csv(
                file,
                encoding="cp949"
            )

    else:
        df = pd.read_excel(file)


except Exception as e:

    st.error(f"파일 오류 : {e}")
    st.stop()



st.subheader("데이터 확인")
st.dataframe(df.head())


# -------------------------
# 컬럼 직접 선택
# -------------------------

st.subheader("데이터 컬럼 지정")


columns = list(df.columns)


name_col = st.selectbox(
    "주차장명 컬럼",
    columns
)


gu_col = st.selectbox(
    "자치구 컬럼",
    columns
)


lat_col = st.selectbox(
    "위도(Y) 컬럼",
    columns
)


lon_col = st.selectbox(
    "경도(X) 컬럼",
    columns
)


fee_col = st.selectbox(
    "요금 컬럼",
    columns
)



# -------------------------
# 데이터 정리
# -------------------------


df[lat_col] = pd.to_numeric(
    df[lat_col],
    errors="coerce"
)


df[lon_col] = pd.to_numeric(
    df[lon_col],
    errors="coerce"
)


df = df.dropna(
    subset=[
        lat_col,
        lon_col
    ]
)



# 요금 숫자 변환

df["요금_숫자"] = (
    df[fee_col]
    .astype(str)
    .str.extract(r"(\d+)")
)


df["요금_숫자"] = pd.to_numeric(
    df["요금_숫자"],
    errors="coerce"
)



# -------------------------
# 유료 주차장만
# -------------------------

paid = df[
    df["요금_숫자"] > 0
].copy()



if len(paid) == 0:

    st.warning(
        "요금 데이터에서 유료 주차장을 찾지 못했습니다."
    )

    st.stop()



st.success(
    f"유료 주차장 {len(paid)}개"
)



# -------------------------
# 자치구 선택
# -------------------------

gus = sorted(
    paid[gu_col]
    .dropna()
    .astype(str)
    .unique()
)



selected_gu = st.selectbox(
    "서울시 자치구 선택",
    gus
)



filtered = paid[
    paid[gu_col].astype(str)
    == selected_gu
]



# -------------------------
# 요금 필터
# -------------------------

max_fee = int(
    filtered["요금_숫자"].max()
)


fee_limit = st.slider(
    "최대 주차 요금",
    0,
    max_fee,
    max_fee
)


filtered = filtered[
    filtered["요금_숫자"] <= fee_limit
]


st.write(
    f"검색 결과 : {len(filtered)}개"
)



# -------------------------
# 지도 표시
# -------------------------

center = [
    filtered[lat_col].mean(),
    filtered[lon_col].mean()
]


m = folium.Map(
    location=center,
    zoom_start=13
)



for _, row in filtered.iterrows():

    popup = f"""
    <b>{row[name_col]}</b><br>
    자치구 : {row[gu_col]}<br>
    요금 : {row[fee_col]}
    """

    folium.Marker(
        location=[
            row[lat_col],
            row[lon_col]
        ],
        popup=popup,
        tooltip=row[name_col],
        icon=folium.Icon(
            color="red",
            icon="car",
            prefix="fa"
        )
    ).add_to(m)



st_folium(
    m,
    width=1200,
    height=600
)



# -------------------------
# 결과표
# -------------------------

st.subheader("주차장 목록")


show = [
    name_col,
    gu_col,
    fee_col
]


st.dataframe(
    filtered[show]
)
