import pybithumb
import numpy as np
import pandas as pd
import coin_tool


class Bithumb_login:

    def __init__(self):

        self.login_key()  # 로그인 key 입력
        self.bithumb_login()  # 빗썸 로그인 함수
        self.account_info()  # 빗썸 내 계좌 정보 조회 함수

    def login_key(self):  # 자기 자신의 API 키 값들을 넣는다.

        self.conkey = 'Bithumb api 신청해서 발급받은 Connect Key 입력'
        self.seckey = 'Bithumb api 신청해서 발급받은 Secret Key 입력'

    def bithumb_login(self):  # 빗썸에 로그인하여 내 계좌 정보를 가져온다.

        bithumb = pybithumb.client.Bithumb(self.conkey, self.seckey)
        self.bithumb_info = bithumb

    def account_info(self):  # 가져온 내 계좌 정보 값으로 현재 정보들을 추출한다.
        a = []
        b = []

        print("로그인 성공 :", self.bithumb_info)
        print("=" * 150)
        print("<get_balance('')>")
        print(self.bithumb_info.get_balance('')['data'])
        print("=" * 150)
        print('계좌 정보 조회중입니다....')
        print('=' * 150)

        for coin in self.bithumb_info.get_tickers():
            # print(coin,self.bithumb_info.get_balance(coin))
            if self.bithumb_info.get_balance(coin)[0] != 0:
                a.append(coin)  # 보유 코인
                b.append(self.bithumb_info.get_balance(coin)[0])

        c = []
        for set_ in a:  # 보유 코인에 대해서만 호가조회 10줄씩
            c.append(self.bithumb_info.get_orderbook(set_, "KRW", 10))
        #print("c(own_info) :", c)
        #print("=" * 150)

        print("=" * 150)
        # print("a :",a) # 종목확인
        print("보유 코인 :", a)
        print("보유 코인량 :", b)
        self.account = self.bithumb_info.get_balance('')  # 계좌 전체 통계 정보
        self.coin_own = a
        self.coin_vol = b
        self.own_info = c

        print("=" * 150)
        print("현재 보유 원화 : ", self.account["data"]["available_krw"])
        print("현재 보유 코인 종목 수 : ", len(self.coin_own))
        print("=" * 150)
        print('계좌 정보 조회 완료!')
        print('=' * 150)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class account_coin_info(Bithumb_login):

    def __init__(self):
        super().__init__()

        self.my_coin_info = self.own_info
        self.my_coin_name = []
        self.my_coin_count = []
        #self.my_coin_avg_price = [] <- 해결필요 / Main.py 에서 매도할때 필요★
        self.my_coin_type = []
        self.my_now_price = []
        self.my_bids_asks = []
        self.my_down_price = []
        self.my_up_price = []
        self.limit_count = []

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        self.now_coin_info()         # 현재 코인 정보
        self.my_account_data_info()  # 내 계좌 데이터 조회

        
    # 현재 코인 정보
    def now_coin_info(self):

        coin_count = len(self.my_coin_info) # 보유 코인 갯수
        for i in range(coin_count):

            coin_info = self.my_coin_info[i]  # 보유하고 있는 코인 정보를 1개씩 가져온다.
            coin_vol = self.coin_vol[i]
            print('KRW-' + self.my_coin_info[i]['order_currency'], '정보를 조회 합니다')

            coin_name = coin_info['order_currency'] # 코인 이름
            coin_count = coin_vol # 코인종목당 보유량
            #coin_avg_price = coin_info['avg_buy_price'] # 코인 매수 평균 단가 <- 해결필요 / Main.py 에서 매도할때 필요★
            coin_type = coin_info['payment_currency'] # 평단가 기준 화폐('KRW')
            now_price = pybithumb.get_current_price(coin_name,"KRW") # 현재가 조회
            order = pybithumb.get_orderbook(coin_name) # 매도/매수 가격과 수량에대한 정보가 조회 된다.
            down_price = order['bids'][0]['price'] # 매도 호가 정보 (가장최근)
            up_price = order['asks'][0]['price'] # 매수 호가 정보 (가장최근)
            limit_count = coin_tool.limit_deal_count(now_price) # 최소 거래 단위

            self.my_coin_name.append(coin_name)
            self.my_coin_count.append(coin_count)
            #self.my_coin_avg_price.append(float(coin_avg_price)) <- 해결필요 / Main.py 에서 매도할때 필요★
            self.my_coin_type.append(coin_type)
            self.my_now_price.append(float(now_price))
            self.my_down_price.append(float(down_price))
            self.my_up_price.append(float(up_price))
            self.limit_count.append(float(limit_count))

            
    # 내 계좌 데이터 조회
    def my_account_data_info(self): 
        df_1 = [self.my_now_price, self.my_coin_count,
                self.my_coin_type, self.my_down_price, self.my_up_price, self.limit_count] # self.my_coin_avg_price 칼럼도 추가해야함

        df_1 = np.array(df_1)

        df1 = pd.DataFrame(df_1, columns=[self.my_coin_name],
                           index=['now_price', 'coin_count',
                                  'coin_type', 'bid_price', 'ask_price', 'limit_count']) # self.my_coin_avg_price index 도 추가해야함

        print('=' * 150)
        print(df1)
        print('=' * 150)
        print('조회가 완료 되었습니다')
        print('=' * 150)

#account_coin_info() # <- 실행시켜보고싶으면 주석빼고 account_info.py 이 파일만 실행 ㄱㄱ 자기계좌정보 조회하는것임.
