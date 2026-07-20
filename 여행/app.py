import streamlit as st
import random
from datetime import datetime
import urllib.parse


st.set_page_config(
    page_title="랜덤 여행 추천기",
    page_icon="🎲",
    layout="wide"
)


# -----------------------------
# 여행 데이터
# -----------------------------

places = [

{
"name":"경복궁",
"region":"서울",
"type":"역사",
"cost":3000,
"desc":"조선 시대 대표 궁궐로 한국의 역사를 느낄 수 있는 장소",
"image":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Gyeongbokgung_Palace%2C_Seoul%2C_Korea.jpg/640px-Gyeongbokgung_Palace%2C_Seoul%2C_Korea.jpg"
},

{
"name":"성수동",
"region":"서울",
"type":"카페",
"cost":20000,
"desc":"감성 카페와 편집숍이 많은 서울 핫플레이스",
"image":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Seongsu-dong_Seoul.jpg/640px-Seongsu-dong_Seoul.jpg"
},

{
"name":"해운대 해수욕장",
"region":"부산",
"type":"바다",
"cost":0,
"desc":"부산을 대표하는 아름다운 해변",
"image":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Haeundae_Beach.jpg/640px-Haeundae_Beach.jpg"
},

{
"name":"감천문화마을",
"region":"부산",
"type":"관광",
"cost":0,
"desc":"알록달록한 집들이 있는 부산 대표 관광지",
"image":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Gamcheon_Culture_Village.jpg/640px-Gamcheon_Culture_Village.jpg"
},

{
"name":"성산일출봉",
"region":"제주",
"type":"자연",
"cost":5000,
"desc":"제주 대표 자연 명소",
"image":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Seongsan_Ilchulbong.jpg/640px-Seongsan_Ilchulbong.jpg"
},

{
"name":"협재해수욕장",
"region":"제주",
"type":"바다",
"cost":0,
"desc":"맑은 바다와 아름다운 풍경을 가진 해변",
"image":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Hyeopjae_Beach.jpg/640px-Hyeopjae_Beach.jpg"
},

{
"name":"전주 한옥마을",
"region":"전주",
"type":"문화",
"cost":10000,
"desc":"전통 한옥과 먹거리가 가득한 여행지",
"image":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Jeonju_Hanok_Village.jpg/640px-Jeonju_Hanok_Village.jpg"
},

{
"name":"경주 불국사",
"region":"경주",
"type":"역사",
"cost":6000,
"desc":"신라 시대 대표 문화유산",
"image":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Bulguksa_Temple.jpg/640px-Bulguksa_Temple.jpg"
},

{
"name":"강릉 경포대",
"region":"강릉",
"type":"바다",
"cost":0,
"desc":"동해 바다와 산책을 즐길 수 있는 장소",
"image":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Gyeongpo_Beach.jpg/640px-Gyeongpo_Beach.jpg"
},

{
"name":"여수 밤바다",
"region":"여수",
"type":"야경",
"cost":15000,
"desc":"아름다운 야경으로 유명한 여행지",
"image":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Yeosu_Night_Sea.jpg/640px-Yeosu_Night_Sea.jpg"
}

]


fortunes = [
"🍀 오늘은 새로운 장소에서 좋은 추억을 만들 운입니다.",
"📸 오늘 찍은 사진은 오래 기억될 것입니다.",
"🌊 자연과 함께하면 좋은 에너지를 얻습니다.",
"☕ 카페에서 작은 행복을 발견합니다.",
"✨ 즉흥 여행이 최고의 선택입니다."
]


quotes = [
"여행은 새로운 나를 발견하는 시간입니다.",
"좋은 여행은 좋은 기억을 남깁니다.",
"떠나는 순간 일상은 모험이 됩니다.",
"추억은 여행이 남기는 가장 큰 선물입니다."
]


# -----------------------------
# 화면
# -----------------------------

st.title("🎲 랜덤 여행 추천기")

st.write(
"지역을 선택하고 랜덤으로 여행지를 추천받아보세요!"
)


regions = sorted(
list(set(
[x["region"] for x in places]
))
)


selected_region = st.sidebar.selectbox(
"📍 지역 선택",
["전체"] + regions
)


number = st.sidebar.slider(
"추천 장소 개수",
1,
5,
3
)


# -----------------------------
# 추천
# -----------------------------

if st.button(
"🎲 여행 코스 추천받기",
use_container_width=True
):

    if selected_region == "전체":
        data = places
    else:
        data = [
            x for x in places
            if x["region"] == selected_region
        ]


    result = random.sample(
        data,
        min(number,len(data))
    )


    st.success(
        "오늘의 여행 코스가 완성되었습니다!"
    )


    total = sum(
        x["cost"] for x in result
    )


    for i,item in enumerate(result,1):

        st.divider()

        col1,col2 = st.columns(
            [1,2]
        )


        with col1:
            st.image(
                item["image"],
                use_container_width=True
            )


        with col2:

            st.header(
                f"{i}. {item['name']}"
            )

            st.write(
                f"📍 지역 : {item['region']}"
            )

            st.write(
                f"🏷 종류 : {item['type']}"
            )

            st.write(
                item["desc"]
            )

            st.write(
                f"💰 예상 비용 : {item['cost']:,}원"
            )


            map_url = (
                "https://www.google.com/maps/search/?api=1&query="
                +
                urllib.parse.quote(
                    item["name"]
                )
            )


            st.markdown(
                f"[🗺 지도 보기]({map_url})"
            )


    st.divider()


    c1,c2,c3 = st.columns(3)


    c1.metric(
        "추천 장소",
        f"{len(result)}곳"
    )


    c2.metric(
        "총 예상 비용",
        f"{total:,}원"
    )


    c3.metric(
        "추천 점수",
        f"{random.randint(85,100)}점"
    )


    st.subheader(
        "🍀 오늘의 여행 운세"
    )

    st.info(
        random.choice(fortunes)
    )


    st.subheader(
        "💬 여행 명언"
    )

    st.success(
        random.choice(quotes)
    )


    st.caption(
        "생성 시간 : "
        +
        datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )
    )


else:

    st.info(
        "왼쪽에서 지역을 선택하고 버튼을 눌러주세요."
    )
