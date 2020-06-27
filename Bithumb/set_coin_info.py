import pybithumb
import numpy as np
import pandas as pd
import Price_prediction
import coin_tool

# 설정 코인

class Prediction:

    def __init__(self):
        self.set_coin_name = ['ETH', 'XRP', 'POWR','KNC', 'COSM']
        # self.base_coin_name= ['KRW-BTC','KRW-ETH','KRW-XRP','KRW-BCH','KRW-STEEM','KRW-POWR','KRW-EOS',
        #                       'KRW-TRX','KRW-KNC','KRW-ENJ','KRW-THETA','KRW-COSM','KRW-MBL','KRW-HBAR']

        self.set_df = [] # 조회된 데이터
        self.set_future_prices = []  #코인마다 신경망 예측가격 별 리스트를 넣어준다
        self.set_future_price_LSTM = [] # LSTM 예측 가격


        self.data_inquiry()
        self.futuer_price()

    def data_inquiry(self):

        print('코인별 데이터 조회를 실행합니다....')
        print('='*150)

        for i in self.set_coin_name:

            self.set_df.append(pybithumb.get_ohlcv(i, interval="minute15", count=100).loc[::-1].reset_index().rename(columns={'index': 'date'}))
            print(i + ' 데이터 조회를 완료 하였습니다')
        print('=' * 150)


    def futuer_price(self):

        print('가격 예측을 진행합니다')
        print('='*150)

        self.base_coin_names = [i[4:] for i in self.set_coin_name]

        for i in range(len(self.base_coin_names)):

            print(self.base_coin_names[i], '가격 예측시작')
            val = Price_prediction.predcoin(self.base_coin_names[i], self.set_df[i])

            for j in range(len(val)):

                if j == 0:
                    val[j] = round(val[j][0][0], 2)
                else:
                    val[j] = round(val[j][0], 2)

            self.set_future_prices.append(val)

        for i in self.set_future_prices:
            self.set_future_price_LSTM.append(i[0])

        print('가격 예측를 완료 하였습니다')
        print('=' * 150)


class Base_coin_info(Prediction):

    def __init__(self):

        super().__init__()


        self.set_now_price = [] # 현재가
        self.set_down_price = [] # 매수 호가
        self.set_up_price = [] # 매도 호가
        self.set_price_yield = [] # 수익율정보
        self.set_limit_count = [] # 최소 거래 단위

        self.coin_name_inquiry()
        self.base_account_data_info()

    def coin_name_inquiry(self):

        print('설정 코인 정조보회를 시작합니다')
        print('=' * 150)

        for i,coin_name in enumerate(self.set_coin_name):
            print(coin_name,'정보를 조회 합니다')
            now_price = pybithumb.get_current_price(coin_name,"KRW")  # 현재가 조회 검색 조회가 (거래단위-코인이름) 이렇게 되야 된다 ex)(KRW-BTC)
            order = pybithumb.get_orderbook(coin_name) # 매수/매도 호가 조회
            #bids_asks = order[0]['orderbook_units'] # 매수/매도 호가 가격 정보를 가져온다.
            down_price = order['bids'][0]['price'] # 매도 호가 정보
            up_price = order['asks'][0]['price'] # 매수 호가 정보
            future_yield = coin_tool.price_yield(now_price, self.set_future_price_LSTM[i])
            limit_count = coin_tool.limit_deal_count(now_price)  # 최소 거래 단위

            self.set_now_price.append(now_price)
            self.set_down_price.append(down_price)
            self.set_up_price.append(up_price)
            self.set_price_yield.append(future_yield)
            self.set_limit_count.append(limit_count)

        print('설정 코인 정조보회 마쳤습니다')
        print('=' * 150)

    def base_account_data_info(self):

        print('설정코인 DATA표 를 생성합니다')
        print('=' * 150)

        df_1 = [self.set_now_price ,self.set_future_price_LSTM ,
                self.set_price_yield,self.set_down_price,self.set_up_price,self.set_limit_count]

        df = np.array(df_1)


        df1 = pd.DataFrame(df, columns=[self.set_coin_name],
                           index=['now_price', 'future_price_LSTM', 'price_yield',
                                    'ask_price','bid_price','limit_count'])

        print(df1)
        print('=' * 150)
        print('조회가 완료 되었습니다')
        print('=' * 150)



