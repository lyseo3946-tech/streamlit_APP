import streamlit as st
import random
from datetime import datetime


# 페이지 설정
st.set_page_config(
    page_title="랜덤 여행 추천기",
    page_icon="🎲",
    layout="centered"
)


# 여행 데이터
travel_data = {
    "서울": [
        ("경복궁", "역사 관광", 3000),
        ("남산서울타워", "야경", 21000),
        ("익선동", "카페 거리", 15000),
        ("한강공원", "산책", 0),
        ("성수동", "핫플레이스", 20000),
        ("롯데월드", "놀이공원", 62000),
        ("북촌한옥마을", "문화 체험", 0),
    ],

    "부산": [
        ("해운대", "바다 여행", 0),
        ("광안리", "야경", 0),
        ("감천문화마을", "관광", 0),
        ("국제시장", "먹거리", 15000),
        ("흰여울문화마을", "산책", 0),
        ("송도 케이블카", "체험", 17000),
    ],

    "제주": [
        ("성산일출봉", "자연 관광", 5000),
        ("협재해수욕장", "바다", 0),
        ("우도", "섬 여행", 15000),
        ("오설록", "카페", 12000),
        ("카멜리아힐", "정원", 10000),
        ("용머리해안", "자연", 2000),
    ]
}


fortunes = [
    "🍀 오늘은 예상하지 못한 즐거운 일이 생길 운입니다.",
    "🌈 새로운 장소에서 특별한 추억을 만들 수 있습니다.",
    "📸 오늘 찍은 사진은 오래 기억될 것입니다.",
    "☕ 카페에서 작은 행복을 발견하는 날입니다.",
    "🌊 자연과 함께하면 좋은 에너지를 얻습니다.",
    "✨ 즉흥적인 선택이 최고의 여행이 됩니다."
]


quotes = [
    "여행은 돌아왔을 때 더 성장한 나를 만나는 시간입니다.",
    "좋은 여행은 좋은 기억을 남깁니다.",
    "새로운 길에서 새로운 나를 발견합니다.",
    "인생은 여행이고 순간은 추억입니다."
]


# 제목
st.title("🎲 랜덤 여행 추천기")
st.write("버튼 하나로 오늘의 여행 코스를 추천받아보세요!")


# 사이드바
st.sidebar.title("⚙️ 여행 설정")

region = st.sidebar.selectbox(
    "지역 선택",
    list(travel_data.keys())
)


place_count = st.sidebar.slider(
    "추천 장소 개수",
    2,
    5,
    3
)


# 추천 버튼
if st.button("🎲 랜덤 여행 추천받기"):

    selected = random.sample(
        travel_data[region],
        place_count
    )


    total_cost = sum(
        item[2] for item in selected
    )


    st.success("✨ 여행 코스가 완성되었습니다!")


    st.subheader("🗺 오늘의 여행 코스")


    for idx, item in enumerate(selected, 1):

        name = item[0]
        category = item[1]
        cost = item[2]


        st.markdown("---")

        st.subheader(
            f"{idx}. {name}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"📌 종류 : {category}"
            )

        with col2:
            st.write(
                f"💰 예상 비용 : {cost:,}원"
            )


    st.markdown("---")


    a, b, c = st.columns(3)

    a.metric(
        "추천 장소",
        f"{len(selected)}곳"
    )

    b.metric(
        "예상 비용",
        f"{total_cost:,}원"
    )

    b.metric(
        "추천 점수",
        f"{random.randint(85,100)}점"
    )


    st.subheader("🍀 오늘의 여행 운세")

    st.info(
        random.choice(fortunes)
    )


    st.subheader("💬 오늘의 여행 명언")

    st.success(
        random.choice(quotes)
    )


    st.subheader("📅 추천 시간")

    st.write(
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


    result = "\n".join(
        [
            f"{i+1}. {x[0]} ({x[1]})"
            for i, x in enumerate(selected)
        ]
    )


    st.download_button(
        label="📥 여행 코스 저장",
        data=result,
        file_name="my_trip.txt"
    )


else:

    st.info(
        "왼쪽에서 지역을 선택하고 버튼을 눌러주세요."
    )


st.divider()

st.caption(
    "Made with Streamlit 🎈"
)
