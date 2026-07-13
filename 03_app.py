parking-app/
│
├── import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


st.set_page_config(
    page_title="서울 공영주차장 지도",
    layout="wide"
)


st.title("🚗 서울시 공영주차장 요금 지도")
st.write(
    "CSV 데이터를 업로드하면 자치구별 유료 공영주차장을 지도에서 확인할 수 있습니다."
)


# ----------------------------
# 파일 업로드
# ----------------------------

uploaded_file = st.file_uploader(
    "서울 공영주차장 CSV 업로드",
    type=["csv", "xlsx"]
)


if uploaded_file:

    # 파일 읽기
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(
            uploaded_file,
            encoding="utf-8"
        )

    else:
        df = pd.read_excel(uploaded_file)


    st.subheader("데이터 미리보기")
    st.dataframe(df.head())


    # ----------------------------
    # 컬럼 자동 탐색
    # ----------------------------

    def find_column(columns, keywords):

        for col in columns:
            for k in keywords:
                if k in col:
                    return col

        return None


    name_col = find_column(
        df.columns,
        ["주차장명", "명칭", "시설명"]
    )

    gu_col = find_column(
        df.columns,
        ["자치구", "구"]
    )

    lat_col = find_column(
        df.columns,
        ["위도", "LAT", "lat"]
    )

    lon_col = find_column(
        df.columns,
        ["경도", "LON", "lon"]
    )

    fee_col = find_column(
        df.columns,
        ["요금", "기본요금", "시간요금"]
    )


    if not all(
        [name_col, gu_col, lat_col, lon_col, fee_col]
    ):

        st.error(
            """
            필요한 컬럼을 찾지 못했습니다.

            필요한 항목:
            - 주차장명
            - 자치구
            - 위도
            - 경도
            - 요금
            """
        )

        st.stop()


    # ----------------------------
    # 데이터 정리
    # ----------------------------

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


    # 요금 숫자화
    df["요금_숫자"] = (
        df[fee_col]
        .astype(str)
        .str.extract(r"(\d+)")
    )

    df["요금_숫자"] = pd.to_numeric(
        df["요금_숫자"],
        errors="coerce"
    )


    # ----------------------------
    # 유료 주차장 필터
    # ----------------------------

    paid_df = df[
        df["요금_숫자"].fillna(0) > 0
    ].copy()


    st.success(
        f"유료 공영주차장 {len(paid_df)}개 발견"
    )


    # ----------------------------
    # 자치구 선택
    # ----------------------------

    gus = sorted(
        paid_df[gu_col]
        .dropna()
        .unique()
    )


    selected_gu = st.selectbox(
        "서울시 자치구 선택",
        gus
    )


    filtered = paid_df[
        paid_df[gu_col] == selected_gu
    ]


    # ----------------------------
    # 요금 범위
    # ----------------------------

    max_fee = int(
        filtered["요금_숫자"].max()
    )


    fee_limit = st.slider(
        "최대 시간 요금",
        0,
        max_fee,
        max_fee
    )


    filtered = filtered[
        filtered["요금_숫자"]
        <= fee_limit
    ]


    st.write(
        f"검색 결과: {len(filtered)}개"
    )


    # ----------------------------
    # 지도 생성
    # ----------------------------

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
        자치구: {row[gu_col]}<br>
        요금: {row[fee_col]}<br>
        주소: {row.get('주소','')}
        """

        folium.Marker(
            [
                row[lat_col],
                row[lon_col]
            ],
            popup=popup,
            tooltip=row[name_col],
            icon=folium.Icon(
                color="blue",
                icon="car",
                prefix="fa"
            )
        ).add_to(m)


    st_folium(
        m,
        width=1200,
        height=650
    )


    # ----------------------------
    # 결과 테이블
    # ----------------------------

    st.subheader("검색 결과")

    show_cols = [
        name_col,
        gu_col,
        fee_col
    ]

    if "주소" in filtered.columns:
        show_cols.append("주소")


    st.dataframe(
        filtered[show_cols]
        .reset_index(drop=True)
    )

else:

    st.info(
        "서울 공영주차장 CSV 파일을 업로드하세요."
    )
├── requirements.txt
└── README.md
