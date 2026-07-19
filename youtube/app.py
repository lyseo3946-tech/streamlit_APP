import streamlit as pd
import streamlit as st
import googleapiclient.discovery
import googleapiclient.errors
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
from datetime import datetime

# 한글 폰트 설정 (Streamlit Cloud 환경 고려)
# 리눅스 서버 기준 기본 폰트인 나눔 폰트나 폰트 경로를 지정해야 깨지지 않습니다.
import matplotlib.font_manager as fm

# 페이지 설정
st.set_page_config(page_title="유튜브 댓글 분석기", layout="wide")
st.title("📊 유튜브 댓글 분석기")
st.markdown("유튜브 영상의 댓글을 수집하고 시간대별 추이 및 워드클라우드를 분석합니다.")

# 사이드바에서 API 키 및 설정 입력
st.sidebar.header("🔧 설정")
api_key = st.sidebar.text_input("YouTube API Key를 입력하세요", type="password")
video_url = st.sidebar.text_input("유튜브 영상 링크를 입력하세요")
max_comments = st.sidebar.slider("수집할 댓글 개수 설정", min_value=10, max_value=500, value=100, step=10)

# 유튜브 비디오 ID 추출 함수
def extract_video_id(url):
    regex = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    if match:
        return match.group(4)
    return None

# 유튜브 댓글 수집 함수
def get_youtube_comments(api_key, video_id, max_results):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    comments = []
    
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_results, 100), # 한 번에 최대 100개
            textFormat="plainText"
        )
        
        while request and len(comments) < max_results:
            response = request.execute()
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'published_at': comment['publishedAt'],
                    'like_count': comment['likeCount']
                })
                if len(comments) >= max_results:
                    break
                    
            # 다음 페이지가 있으면 계속 수집
            if 'nextPageToken' in response and len(comments) < max_results:
                request = youtube.commentThreads().list_next(request, response)
            else:
                break
                
        return pd.DataFrame(comments)
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return None

# 메인 로직
if st.sidebar.button("분석 시작하기"):
    if not api_key:
        st.warning("API Key를 입력해주세요.")
    elif not video_url:
        st.warning("유튜브 링크를 입력해주세요.")
    else:
        video_id = extract_video_id(video_url)
        
        if not video_id:
            st.error("올바른 유튜브 URL 형식이 아닙니다.")
        else:
            # 1. 영상 임베드 화면 표시
            st.subheader("📺 선택한 영상")
            st.video(video_url)
            
            with st.spinner("댓글을 수집하고 분석하는 중입니다..."):
                df = get_youtube_comments(api_key, video_id, max_comments)
                
            if df is not None and not df.empty:
                # 전처리: 날짜 데이터 변환
                df['published_at'] = pd.to_datetime(df['published_at'])
                df['date_hour'] = df['published_at'].dt.to_period('H').dt.to_timestamp()
                
                # 데이터 기본 정보 레이아웃
                st.success(f"총 {len(df)}개의 댓글을 성공적으로 수집했습니다!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # 2. 시간대별 댓글 작성 추이
                    st.subheader("📈 시간대별 댓글 작성 추이")
                    time_counts = df.groupby('date_hour').size().reset_index(name='count')
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    sns.lineplot(data=time_counts, x='date_hour', y='count', marker='o', color='#FF0000', ax=ax)
                    ax.set_title("Comment Trend over Time")
                    ax.set_xlabel("Time")
                    ax.set_ylabel("Number of Comments")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    
                with col2:
                    # 3. 댓글 반응도 (좋아요 수가 많은 상위 댓글)
                    st.subheader("🔥 가장 반응이 뜨거운 댓글 (좋아요 순)")
                    top_liked = df.sort_values(by='like_count', ascending=False).head(5)
                    for idx, row in top_liked.iterrows():
                        st.markdown(f"**{row['author']}** (👍 {row['like_count']}개)")
                        st.caption(f"{row['text']}")
                        st.write("---")
                        
                # 4. 워드클라우드 시각화
                st.subheader("☁️ 댓글 워드클라우드")
                
                # 간단한 텍스트 정제 (특수문자 제거 및 공백 기준 분리)
                all_text = " ".join(df['text'].values)
                cleaned_text = re.sub(r'[^\w\s]', '', all_text)
                words = cleaned_text.split()
                
                # 2글자 이상 단어만 필터링
                words = [word for word in words if len(word) > 1]
                word_counts = Counter(words)
                
                if word_counts:
                    # Streamlit Cloud 환경에서 한글 깨짐 방지를 위해 기본 폰트 경로 우회 설정 가능
                    # 여기서는 나눔고딕 등의 폰트가 설치되어 있다고 가정하거나 폰트 미지정 시 기본 폰트 사용
                    try:
                        wc = WordCloud(width=800, height=400, background_color='white', font_path='NanumGothic.ttf').generate_from_frequencies(word_counts)
                    except:
                        # 폰트 파일이 없을 경우 기본 폰트로 생성 (한글이 깨질 수 있으므로 나눔폰트 다운로드 권장)
                        wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
                        st.caption("⚠️ 한글 폰트(NanumGothic.ttf) 파일이 루트 폴더에 없으면 워드클라우드 내 한글이 깨질 수 있습니다.")
                        
                    fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
                    ax_wc.imshow(wc, interpolation='bilinear')
                    ax_wc.axis('off')
                    st.pyplot(fig_wc)
                else:
                    st.info("워드클라우드를 생성할 만큼 충분한 단어가 없습니다.")
                    
                # 데이터프레임 확인
                with st.expander("📥 수집된 전체 댓글 데이터 보기"):
                    st.dataframe(df[['author', 'text', 'published_at', 'like_count']])
            else:
                st.warning("수집된 댓글이 없거나 영상 설정을 확인해주세요.")
