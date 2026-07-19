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
            maxResults=min(max_results, 100), 
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
                    
            if 'nextPageToken' in response and len(comments) < max_results:
                request = youtube.commentThreads().list
