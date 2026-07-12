import streamlit as st
import requests

st.set_page_config(
    page_title="오늘 뭐 입지?",
    page_icon="👕",
    layout="centered"
)

API_KEY = st.secrets["WEATHER_API_KEY"]

st.title("🌤 오늘 뭐 입지?")
st.write("오늘 날씨에 맞는 옷과 음악을 추천해드립니다!")

city = st.text_input("도시를 입력하세요", "Seoul")


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=kr"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


if st.button("오늘 날씨 보기"):

    weather = get_weather(city)

    if weather:

        temp = weather["main"]["temp"]
        feels = weather["main"]["feels_like"]
        humidity = weather["main"]["humidity"]
        weather_main = weather["weather"][0]["description"]

        st.subheader("🌦 현재 날씨")

        st.write(f"**기온:** {temp}℃")
        st.write(f"**체감온도:** {feels}℃")
        st.write(f"**습도:** {humidity}%")
        st.write(f"**날씨:** {weather_main}")

        st.divider()

        if temp >= 28:

            st.header("👕 추천 옷차림")

            st.image(
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=800",
                use_container_width=True
            )

            st.success("민소매, 반팔, 반바지, 샌들")

            music = "여름 신나는 노래"

        elif temp >= 20:

            st.header("👕 추천 옷차림")

            st.image(
                "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=800",
                use_container_width=True
            )

            st.success("얇은 셔츠, 긴팔티, 청바지")

            music = "산책하기 좋은 노래"

        elif temp >= 10:

            st.header("👕 추천 옷차림")

            st.image(
                "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800",
                use_container_width=True
            )

            st.success("가디건, 자켓, 맨투맨")

            music = "감성 노래"

        else:

            st.header("👕 추천 옷차림")

            st.image(
                "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800",
                use_container_width=True
            )

            st.success("패딩, 코트, 목도리")

            music = "겨울 감성 음악"

        st.divider()

        st.header("🎵 추천 음악")

        youtube = f"https://www.youtube.com/results?search_query={music}"

        st.link_button(
            "유튜브에서 음악 듣기",
            youtube
        )

    else:
        st.error("도시를 찾을 수 없습니다.")
