import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title='투자독학 포트폴리오', page_icon=':teddy_bear:', layout='wide')

# Header Section
with st.container():
    st.subheader('반갑습니다. 이온입니다. :blush:')
    st.title('현명한 가치 투자자가 되고자 합니다.')
    st.write('저평가 성장주를 장기 보유하려고 합니다.')
    st.write('저의 유튜브에 다양한 기업 분석 콘텐츠가 있습니다. 함께 성장합시다!')
    st.write('[여기를 눌러보세요!](https://www.youtube.com/@hyunsight101)')

with st.container():
    st.write('---')
    st.header('주식 포트폴리오 공개')
    st.markdown("<br>", unsafe_allow_html=True)  # 적당한 공백
    st.write(
        """
        제가 실제 보유 중인 종목들과 포트폴리오 평가금액 추이입니다.
        한국 주식도 정말 하고 싶은데, 가족의 회계법인 관련 문제로 하지 못하고 있습니다. :sob:
        """
    )

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

with st.container():
    left_column, right_column = st.columns(2)
    
    with left_column:
        dates = pd.date_range(start="2025-08-18", end=pd.Timestamp.today(), freq="B")

        # 보유 주식 수
        shares = {
            "7095.T": 35,
            "GAMB": 55,
            "RERE": 51,
            "MRNA": 16,
            "ZIM": 13
        }

        # 수작업 데이터 프레임 틀 생성
        prices = pd.DataFrame(index=dates, columns=shares.keys())

        # 각 종목 가격을 야후 파이낸스에서 받아오기 (수작업 유지)
        for ticker in shares.keys():
            data = yf.download(ticker, start=dates[0], end=dates[-1] + pd.Timedelta(days=1))["Close"]
            # 데이터가 부족하면 마지막 값 반복
            data = data.reindex(dates, method="ffill")
            prices[ticker] = data.values

        # 엔화를 달러로 환산 (7095.T만)
        JPY_to_USD = 0.0075
        prices["7095.T"] = prices["7095.T"] * JPY_to_USD

        # 평가 금액 계산
        values = prices.mul(pd.Series(shares))
        portfolio_value = values.sum(axis=1)

        # Streamlit에서 포트폴리오 그래프 표시
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(portfolio_value.index, portfolio_value.values, marker="o")
        ax.set_title("Portfolio Valuation Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Portfolio Value")
        ax.grid(True)

        st.pyplot(fig)
    with right_column:
        # 가장 최근 날짜 기준 각 종목 평가 금액
        latest_values = values.iloc[-1]
        
        # Streamlit 스타일의 원그래프
        fig, ax = plt.subplots(figsize=(7,7))
        ax.pie(
            latest_values,
            labels=latest_values.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.tab20.colors
        )
        ax.set_title("Portfolio Composition by Latest Value")
        ax.axis('equal')  # 원형 비율 유지
        
        st.pyplot(fig)

img1 = "https://github.com/hlynch1004-cyber/blank-app/blob/main/GAMB_financials_rolling_CAGR.png?raw=true"
img2 = "https://github.com/hlynch1004-cyber/blank-app/blob/main/7095.T_financials_rolling_CAGR.png?raw=true"
img3 = "https://github.com/hlynch1004-cyber/blank-app/blob/main/RERE_financials_rolling_CAGR.png?raw=true"
img4 = "https://github.com/hlynch1004-cyber/blank-app/blob/main/MRNA_financials_rolling_CAGR.png?raw=true"
img5 = "https://github.com/hlynch1004-cyber/blank-app/blob/main/ZIM_financials_rolling_CAGR.png?raw=true"  # 5번째 이미지

with st.container():
    st.write('---')
    st.header('종목별 이익 그래프')

    # 1행: 2열
    col1, col2 = st.columns(2)
    with col1:
        st.image(img1, caption="Gambling.com Group Limited (GAMB)")
    with col2:
        st.image(img2, caption="Macbee Planet, Inc. (7095)")
    
    # 2행: 2열
    col3, col4 = st.columns(2)
    with col3:
        st.image(img3, caption="ATRenew Inc. (RERE)")
    with col4:
        st.image(img4, caption="Moderna, Inc. (MRNA)")
    
    # 3행: 1열
    st.image(img5, caption="ZIM Integrated Shipping Services Ltd. (ZIM)")
