import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# 페이지 설정 (초기 페이지를 더 넓게 설정)
st.set_page_config(layout="centered", page_title="Betting Odds", page_icon="📊")

# 타이틀 추가
st.title('BetterJin309')
st.subheader('Betting Odds')

# 스포츠 나열
sports = ['축구','농구','야구']

# 리그 나열
league = {
    '축구' : ['EPL','EFL','라리가','분데스리가','세리에A','리그1','K리그 1','K리그 2','A리그','에레디비시에'],
    '농구' : ['KBL','W-KBL','NBA'],
    '야구' : ['KBO','MLB','NPB']
}

selected_sport = st.selectbox('종목 선택', sports)

if selected_sport:
    selected_league = st.selectbox(f'리그 선택', league[selected_sport])
    

url_mapping = {
    'EPL': 'https://www.zentoto.com/sports/soccer/epl/fixtures',
    'EFL': 'https://www.zentoto.com/sports/soccer/championship/fixtures',
    '라리가': 'https://www.zentoto.com/sports/soccer/laliga/fixtures',
    '분데스리가': 'https://www.zentoto.com/sports/soccer/bundesliga/fixtures',
    '세리에A': 'https://www.zentoto.com/sports/soccer/serie-a/fixtures',
    '리그1': 'https://www.zentoto.com/sports/soccer/ligue1/fixtures',
    'K리그 1': 'https://www.zentoto.com/sports/soccer/k-classic/fixtures',
    'K리그 2': 'https://www.zentoto.com/sports/soccer/k-challenge/fixtures',
    'A리그': 'https://www.zentoto.com/sports/soccer/australia-league/fixtures',
    '에레디비시에': 'https://www.zentoto.com/sports/soccer/eredivisie/fixtures',
    'NBA': 'https://www.zentoto.com/sports/basketball/nba/fixtures',
    'KBL': 'https://www.zentoto.com/sports/basketball/kbl/fixtures',
    'W-KBL': 'https://www.zentoto.com/sports/basketball/wkbl/fixtures',
    'KBO': 'https://www.zentoto.com/sports/baseball/kbo/fixtures',
}

url = url_mapping.get(selected_league, '')


if st.button('배당 조회'):
    result = []

    if selected_sport == '농구' : # 농구 일 경우
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 나무 태그 : 경기
        games = soup.select('.league-game')
        result = []

        for game in games[:10] :
            date = game.select_one('.w15').text.strip()[5:]
            home = game.select_one('.col-10.text-right > a').text
            home_link = 'https://www.zentoto.com' + game.select_one('.col-10.text-right > a').attrs['href']
            away = game.select_one('.col-10.text-left > a').text
            away_link = 'https://www.zentoto.com' + game.select_one('.col-10.text-left > a').attrs['href']

            win = game.select_one('.row.cell-1x.dist-table > div:nth-of-type(1) > p').text
            lose = game.select_one('.row.cell-1x.dist-table > div:nth-of-type(2) > p').text

            preview = 'https://www.zentoto.com' + game.select_one('.w10 > a').attrs['href']

            vs = 'vs'
            result.append([date, home, home_link, vs, away, away_link, win, lose, preview])
            

        df = pd.DataFrame(result, columns=['일시', '홈', '홈링크', '', '어웨이', '어웨이링크', '승', '패', 'preview'])

        # HTML 테이블로 변환
        def make_clickable(row):
            home = f'<a href="{row["홈링크"]}" target="_blank" style="text-decoration:none; color:inherit;">{row["홈"]}</a>'
            away = f'<a href="{row["어웨이링크"]}" target="_blank" style="text-decoration:none; color:inherit;">{row["어웨이"]}</a>'
            preview = f'<a href="{row["preview"]}" target="_blank">링크</a>'
            return [row['일시'], home, away, row['승'], row['패'], preview]
        
        # 테이블 변환
        styled_df = df.apply(make_clickable, axis=1, result_type='expand')
        styled_df.columns = ['일시', '홈', '어웨이', '승', '패','프리뷰']

        st.markdown(
            styled_df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

    elif selected_sport == '축구' : # 축구일 경우

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 나무 태그 : 경기
        games = soup.select('.league-game')
        result = []

        for game in games[:10] :
            date = game.select_one('.w15').text.strip()[5:]
            home = game.select_one('.col-10.text-right > a').text
            home_link = 'https://www.zentoto.com' + game.select_one('.col-10.text-right > a').attrs['href']
            away = game.select_one('.col-10.text-left > a').text
            away_link = 'https://www.zentoto.com' + game.select_one('.col-10.text-left > a').attrs['href']

            win = game.select_one('.row.cell-1x.dist-table > div:nth-of-type(1) > p').text
            draw = game.select_one('.row.cell-1x.dist-table > div:nth-of-type(2) > p').text
            lose = game.select_one('.row.cell-1x.dist-table > div:nth-of-type(3) > p').text

            preview = 'https://www.zentoto.com' + game.select_one('.w10 > a').attrs['href']

            vs = 'vs'
            result.append([date, home, home_link, vs, away, away_link, win, draw, lose, preview])
            

        df = pd.DataFrame(result, columns=['일시', '홈', '홈링크', '', '어웨이', '어웨이링크', '승', '무', '패', 'preview'])



        # HTML 테이블로 변환
        def make_clickable(row):
            home = f'<a href="{row["홈링크"]}" target="_blank" style="text-decoration:none; color:inherit;">{row["홈"]}</a>'
            away = f'<a href="{row["어웨이링크"]}" target="_blank" style="text-decoration:none; color:inherit;">{row["어웨이"]}</a>'
            preview = f'<a href="{row["preview"]}" target="_blank">링크</a>'
            return [row['일시'], home, away, row['승'], draw, row['패'], preview]
        
        # 테이블 변환
        styled_df = df.apply(make_clickable, axis=1, result_type='expand')
        styled_df.columns = ['일시', '홈', '어웨이', '승','무','패','프리뷰']

        st.markdown(
            styled_df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )



    elif selected_sport == '야구' : # 야구일 경우
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 나무 태그 : 경기
        games = soup.select('.league-game')
        result = []

        for game in games[:10] :
            date = game.select_one('.w15').text.strip()[5:]
            home = game.select_one('.col-10.text-right > a').text
            home_link = 'https://www.zentoto.com' + game.select_one('.col-10.text-right > a').attrs['href']
            away = game.select_one('.col-10.text-left > a').text
            away_link = 'https://www.zentoto.com' + game.select_one('.col-10.text-left > a').attrs['href']

            win = game.select_one('.row.cell-1x.dist-table > div:nth-of-type(1) > p').text
            draw = game.select_one('.row.cell-1x.dist-table > div:nth-of-type(2) > p').text
            lose = game.select_one('.row.cell-1x.dist-table > div:nth-of-type(3) > p').text

            preview = 'https://www.zentoto.com' + game.select_one('.w10 > a').attrs['href']

            vs = 'vs'
            result.append([date, home, vs, away, win, draw, lose, preview])
            

        df = pd.DataFrame(result, columns=['일시','홈','','어웨이','승','무','패','preview'])


        # HTML 테이블로 변환
        def make_clickable(row):
            home = f'<a href="{row["홈링크"]}" target="_blank" style="text-decoration:none; color:inherit;">{row["홈"]}</a>'
            away = f'<a href="{row["어웨이링크"]}" target="_blank" style="text-decoration:none; color:inherit;">{row["어웨이"]}</a>'
            preview = f'<a href="{row["preview"]}" target="_blank">링크</a>'
            return [row['일시'], home, away, row['승'], draw, row['패'], preview]
        
        # 테이블 변환
        styled_df = df.apply(make_clickable, axis=1, result_type='expand')
        styled_df.columns = ['일시', '홈', '어웨이', '승','무','패','프리뷰']

        st.markdown(
            styled_df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

    else:
        pass


if not url:
    st.error("URL을 확인하세요. 선택한 리그에 대한 데이터가 없습니다.")
else:
    response = requests.get(url)
