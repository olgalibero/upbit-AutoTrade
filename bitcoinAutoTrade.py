from slacker import Slacker
import time
import pyupbit
import datetime
import requests

access = "your-access"
secret = "your-secret"


def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer "+token},
                             data={"channel": channel, "text": text}
                             )
    print(response)


myToken = "xoxb-2007319949188-2001383495923-77zp4qFhQWzVjWVTcYXwE8jE"


def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    post_message(myToken, "#project", strbuf)


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + \
        (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# Send a message to #general channel
slack.chat.post_message("#project", "autotrade start")

flag = True

# 자동매매 시작
while True:
    if (flag):
    upbit.buy_market_order("KRW-XRP", 3000000)
    flag = False
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-XRP") + datetime.timedelta(hours=6)
        end_time = start_time + datetime.timedelta(hours=5, minutes=55)

# 9:00 < 현재 < #8:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=60):
            target_price = get_target_price("KRW-XRP", 0.55)
            current_price = get_current_price("KRW-XRP")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-XRP", krw*0.9995)
        else:
            xrp = get_balance("XRP")
            if xrp > 4.5:
                upbit.sell_market_order("KRW-XRP", xrp*0.9995)
            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
