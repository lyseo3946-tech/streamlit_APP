import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


st.set_page_config(
    page_title="서울 공영주차장 지도",
    layout="wide"
)

st.title("🚗 서울시 공영주차장 요금 지도")


# -----------------------------
# 파일 업로드
# -----------------------------

uploaded_file = st.file_uploader(
    "서울시 공영주차장 데이터 업로드 (CSV/XLSX)",
    type=["csv", "xlsx"]
)


if uploaded_file is None:
    st.info("공영주차장 파일을 업로드하세요.")
    st.stop()


# -----------------------------
# 데이터 읽기
# -----------------------------

try:
    if uploaded_file.name.endswith(".csv"):

        try:
            df = pd.read_csv(
                uploaded_file,
                encoding="utf-8"
            )

        except:
            df = pd.read_csv(
                uploaded_file,
                encoding="cp949"
            )

    else:
        df = pd.read_excel(uploaded_file)


except Exception as e:
    st.error(f"파일 읽기 오류: {e}")
    st.stop()



st.subheader("데이터 확인")
st.dataframe(df.head())


# -----------------------------
# 컬럼 자동 찾기
# -----------------------------

def search_column(columns, words):

    for col in columns:
        col = str(col)

        for word in words:
            if word in col:
                return col

    return None



name_col = search_column(
    df.columns,
    ["주차장명", "주차장", "명칭", "시설명"]
)

gu_col = search_column(
    df.columns,
    ["자치구", "구"]
)

lat_col = search_column(
    df.columns,
    ["위도", "LAT", "lat"]
)

lon_col = search_column(
    df.columns,
    ["경도", "LON", "lon"]
)

fee_col = search_column(
    df.columns,
    ["기본요금", "요금", "주차요금", "금액"]
)



missing = []

if name_col is None:
    missing.append("주차장명")

if gu_col is None:
    missing.append("자치구")

if lat_col is None:
    missing.append("위도")

if lon_col is None:
    missing.append("경도")

if fee_col is None:
    missing.append("요금")



if missing:

    st.error(
        "필수 컬럼을 찾지 못했습니다: "
        + ", ".join(missing)
    )

    st.write("현재 데이터 컬럼:")
    st.write(list(df.columns))

    st.stop()



# -----------------------------
# 데이터 정리
# -----------------------------


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



# 요금 숫자 추출

df["요금숫자"] = (
    df[fee_col]
    .astype(str)
    .str.extract(r"(\d+)")
)


df["요금숫자"] = pd.to_numeric(
    df["요금숫자"],
    errors="coerce"
)



# -----------------------------
# 유료 주차장만 표시
# -----------------------------


paid = df[
    df["요금숫자"] > 0
].copy()



if len(paid) == 0:

    st.warning(
        "유료 주차장 데이터가 없습니다."
    )

    st.stop()



st.success(
    f"유료 주차장 {len(paid)}개 검색됨"
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
# 지도
# -----------------------------


map_center = [
    result[lat_col].mean(),
    result[lon_col].mean()
]


m = folium.Map(
    location=map_center,
    zoom_start=13
)



for _, row in result.iterrows():

    popup_text = f"""
    <b>{row[name_col]}</b><br>
    자치구 : {row[gu_col]}<br>
    요금 : {row[fee_col]}
    """

    folium.Marker(
        location=[
            row[lat_col],
            row[lon_col]
        ],
        popup=popup_text,
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



# -----------------------------
# 결과표
# -----------------------------


st.subheader("주차장 목록")


columns = [
    name_col,
    gu_col,
    fee_col
]


if "주소" in result.columns:
    columns.append("주소")


st.dataframe(
    result[columns]
)
