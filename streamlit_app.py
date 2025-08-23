import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='투자독학 포트폴리오', page_icon=':teddy_bear:', layout='wide')

# 상단 로고 (예시 URL, 필요시 본인 로고 URL 또는 로컬 경로로 변경)
st.image("https://github.com/hlynch1004-cyber/blank-app/blob/main/%EB%8D%B0%EC%9D%B4%ED%84%B0/%EB%A1%9C%EA%B3%A0.png?raw=true", width=500)

# 탭 생성
tab_home, tab_portfolio, tab_financials, tab_virtual_portfolio = st.tabs(["홈", "포트폴리오", "종목별 이익", "가상 포트폴리오"])

# ======= 홈 탭 =======
with tab_home:
    st.subheader('반갑습니다. 이온입니다. :blush:')
    st.title('현명한 가치 투자자가 되고자 합니다.')
    st.write('저평가 성장주를 장기 보유하려고 합니다.')
    st.write('저의 유튜브에 다양한 기업 분석 콘텐츠가 있습니다. 함께 성장합시다!')
    st.write('[여기를 눌러보세요!](https://www.youtube.com/@hyunsight101)')

# ======= 포트폴리오 탭 =======
with tab_portfolio:
    st.header('주식 포트폴리오 공개')
    # st.write('---')
    st.write("제가 실제 보유 중인 종목들과 포트폴리오 평가금액 추이입니다. 한국 주식도 정말 하고 싶은데, 가족의 회계법인 관련 문제로 하지 못하고 있습니다. :sob:")

    left_column, right_column = st.columns(2)
    
    # 날짜 생성
    dates = pd.date_range(start="2025-08-18", end=pd.Timestamp.today(), freq="B")

    # 보유 주식 수
    shares = {
        "7095.T": 35,
        "GAMB": 55,
        "RERE": 51,
        "MRNA": 16,
        "ZIM": 13
    }

    # 가격 데이터 프레임 생성
    prices = pd.DataFrame(index=dates, columns=shares.keys())

    # 야후 파이낸스에서 가격 받아오기
    for ticker in shares.keys():
        data = yf.download(ticker, start=dates[0], end=dates[-1] + pd.Timedelta(days=1))["Close"]
        data = data.reindex(dates, method="ffill")
        prices[ticker] = data.values

    # 엔화 → 달러 환산 (7095.T)
    JPY_to_USD = 0.0075
    prices["7095.T"] = prices["7095.T"] * JPY_to_USD

    # 평가 금액 계산
    values = prices.mul(pd.Series(shares))
    portfolio_value = values.sum(axis=1)

    with left_column:
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(portfolio_value.index, portfolio_value.values, marker="o")
        ax.set_title("Portfolio Valuation Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Portfolio Value (USD)")
        ax.grid(True)
        st.pyplot(fig)

    with right_column:
        latest_values = values.iloc[-1]
        fig, ax = plt.subplots(figsize=(7,7))
        ax.pie(
            latest_values,
            labels=latest_values.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.tab20.colors
        )
        ax.set_title("Portfolio Composition by Latest Value")
        ax.axis('equal')
        st.pyplot(fig)

# ======= 종목별 이익 탭 =======
with tab_financials:
    st.header('종목별 이익 그래프')

    st.write("포트폴리오를 구성하는 각 종목의 매출액, 순이익, 영업 현금 흐름을 겹쳐본 그림입니다. 장기적인 성장 추세를 확인할 수 있습니다.")

    img1 = "https://github.com/hlynch1004-cyber/blank-app/blob/main/GAMB_financials_rolling_CAGR.png?raw=true"
    img2 = "https://github.com/hlynch1004-cyber/blank-app/blob/main/7095.T_financials_rolling_CAGR.png?raw=true"
    img3 = "https://github.com/hlynch1004-cyber/blank-app/blob/main/RERE_financials_rolling_CAGR.png?raw=true"
    img4 = "https://github.com/hlynch1004-cyber/blank-app/blob/main/MRNA_financials_rolling_CAGR.png?raw=true"
    img5 = "https://github.com/hlynch1004-cyber/blank-app/blob/main/ZIM_financials_rolling_CAGR.png?raw=true"

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

    # 3행: 2열
    col5, col6 = st.columns(2)
    with col5:
        st.image(img5, caption="ZIM Integrated Shipping Services Ltd. (ZIM)")

# ======= 가상 포트폴리오 탭 =======
with tab_virtual_portfolio:
    st.header('가상 포트폴리오 시뮬레이션')

    st.write("자금을 넣어보고 싶지만 현실적인 금액 부족 때문에 넣지 못하는 종목들의 장기 수익률을 관찰하기 위한 탭입니다.")

    # 가상 투자 설정
    virtual_ticker = "ACN"
    virtual_company = "Accenture plc"
    invest_date = pd.Timestamp("2025-08-22")

    # 가격 데이터 가져오기
    prices_v = yf.download(
        virtual_ticker, 
        start=invest_date, 
        end=pd.Timestamp.today() + pd.Timedelta(days=1)
    )["Close"]

    # 투자일 기준 종가와 최신 종가
    entry_price = prices_v.iloc[0]
    latest_price = prices_v.iloc[-1]

    # 수익률 계산
    return_rate = (latest_price - entry_price) / entry_price * 100

    # 표 생성
    # st.subheader("가상 포트폴리오 현황")
    df_virtual = pd.DataFrame([{
        "기업명": virtual_company,
        "티커 코드": virtual_ticker,
        "(가상) 투자 결정일": invest_date.strftime("%Y-%m-%d"),
        "현재까지의 수익률": f"{float(return_rate):.2f}%"
    }])

    st.dataframe(df_virtual, use_container_width=True)
