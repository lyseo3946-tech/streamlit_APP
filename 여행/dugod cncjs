import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="랜덤 여행 추천기",
    page_icon="🎲",
    layout="wide"
)

# -----------------------------
# 여행 데이터
# -----------------------------
travel_data = {
    "서울": [
        {"name":"경복궁","type":"관광","cost":3000},
        {"name":"남산타워","type":"야경","cost":21000},
        {"name":"익선동","type":"카페","cost":15000},
        {"name":"한강공원","type":"산책","cost":0},
        {"name":"성수동","type":"핫플","cost":20000},
        {"name":"롯데월드","type":"놀이공원","cost":62000},
    ],
    "부산":[
        {"name":"해운대","type":"바다","cost":0},
        {"name":"광안리","type":"야경","cost":0},
        {"name":"감천문화마을","type":"관광","cost":0},
        {"name":"송도해상케이블카","type":"체험","cost":17000},
        {"name":"국제시장","type":"먹거리","cost":15000},
        {"name":"흰여울문화마을","type":"산책","cost":0},
    ],
    "제주":[
        {"name":"성산일출봉","type":"관광","cost":5000},
        {"name":"협재해수욕장","type":"바다","cost":0},
        {"name":"카멜리아힐","type":"정원","cost":10000},
        {"name":"우도","type":"섬여행","cost":15000},
        {"name":"용머리해안","type":"자연","cost":2000},
        {"name":"오설록","type":"카페","cost":12000},
    ]
}

fortunes = [
    "🍀 오늘은 새로운 장소에서 좋은 추억이 생깁니다.",
    "🌈 즉흥적인 여행이 최고의 선택입니다.",
    "📸 사진이 아주 잘 나오는 날입니다.",
    "☕ 카페에서 뜻밖의 행운을 만날 수 있습니다.",
    "🌊 물가로 떠나면 좋은 기운이 들어옵니다.",
    "🍜 맛집 탐방 운이 최고입니다.",
    "✨ 오늘의 여행 만족도는 매우 높습니다.",
    "🚶 천천히 걸을수록 더 많은 즐거움을 발견합니다."
]

quotes = [
    "여행은 유일하게 돈을 쓰고도 더 부자가 되는 경험이다.",
    "가장 좋은 여행은 아직 떠나지 않은 여행이다.",
    "인생은 짧고 세상은 넓다.",
    "새로운 길은 새로운 풍경을 보여준다.",
    "추억은 여행이 남기는 가장 큰 선물이다."
]

# -----------------------------
# 제목
# -----------------------------
st.title("🎲 랜덤 여행 추천기")
st.write("### 오늘 어디로 떠나볼까요?")

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("여행 설정")

region = st.sidebar.selectbox(
    "지역 선택",
    list(travel_data.keys())
)

count = st.sidebar.slider(
    "추천 장소 개수",
    2,
    5,
    3
)

# -----------------------------
# 버튼
# -----------------------------
if st.button("🎲 랜덤 여행 추천받기", use_container_width=True):

    places = random.sample(travel_data[region], count)

    total_cost = sum(p["cost"] for p in places)

    score = random.randint(80,100)

    st.success("추천이 완료되었습니다!")

    st.subheader("🗺 오늘의 여행 코스")

    for i, p in enumerate(places,1):

        with st.container(border=True):

            col1,col2=st.columns([4,1])

            with col1:
                st.markdown(f"## {i}. {p['name']}")
                st.write(f"**분류** : {p['type']}")
                st.write(f"**예상 비용** : {p['cost']:,}원")

            with col2:
                st.metric("추천점수",f"{random.randint(85,100)}점")

    st.divider()

    c1,c2,c3=st.columns(3)

    c1.metric("총 장소",len(places))
    c2.metric("예상 비용",f"{total_cost:,}원")
    c3.metric("여행 만족도",f"{score}%")

    st.divider()

    st.subheader("🍀 오늘의 여행 운세")
    st.info(random.choice(fortunes))

    st.subheader("💬 오늘의 여행 명언")
    st.success(random.choice(quotes))

    st.subheader("📅 추천 생성 시간")
    st.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    route = "\n".join(
        [f"{i+1}. {p['name']} ({p['type']})"
         for i,p in enumerate(places)]
    )

    st.download_button(
        "📥 추천 결과 다운로드",
        route,
        file_name="travel_course.txt"
    )

else:
    st.info("왼쪽에서 지역을 선택한 후 '랜덤 여행 추천받기' 버튼을 눌러보세요.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
