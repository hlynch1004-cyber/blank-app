import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title='My Webpage', page_icon=':tada:', layout='wide')

# Header Section
with st.container():
    st.subheader('반갑습니다. 이온입니다. :blush:')
    st.title('현명한 가치 투자자가 되고자 합니다.')
    st.write('저평가 성장주를 장기 보유하려고 합니다.')
    st.write('저의 유튜브에 다양한 기업 분석 콘텐츠가 있습니다. 함께 성장합시다!')
    st.write('[여기를 눌러보세요!](https://www.youtube.com/@hyunsight101)')

# What I do
with st.container():
    st.write('---')
    left_column, right_column = st.columns(2)
    with left_column:
        st.header('What I do')
        st.markdown("<br>", unsafe_allow_html=True)  # 적당한 공백
        st.write(
            """
            On my YouTube channel, I share my value-investing stock analysis with you.
            - I am just a beginner. Sure, my analysis may not be correct with a high possibility.
            - But I grow and grow every day, and I believe that eventually I would be an 'intelligent investor' someday.

            If this sounds interesting to you, consider subscribing and turning on the notifications!
            """
        )
        st.write('[YouTube Channel >](https://www.youtube.com/@hyunsight101)')
    
    # 오른쪽에 그래프 추가
    with right_column:
        import yfinance as yf
        import matplotlib.pyplot as plt
        import pandas as pd

        # 예시 날짜 (최근 10 영업일)
        dates = pd.date_range(start="2025-08-01", periods=10, freq="B")

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
