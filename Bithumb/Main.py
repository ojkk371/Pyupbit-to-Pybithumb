###main

import account_info
import set_coin_info
import coin_tool


uuid = []
Profit_percent = [0.7 , 1 , 1.5] # 수익율 설정

while 1:

    # 정보 조회

    buy_coin_info = set_coin_info.Base_coin_info()  # 매수 필요 정보
    sell_coin_info = account_info.account_coin_info() # 매도 필요 정보
    bithumb_info = sell_coin_info.bithumb_info

##############################################################################################
    # 매수 필요 정보

    set_coin_name = buy_coin_info.set_coin_name  # 설정 코인 이름 정보
    set_future_yields = buy_coin_info.set_price_yield  # 미래가격 대비 수익율 정보
    set_down_price = buy_coin_info.set_down_price  # 설정 코인 매수가 정보
    set_limit_deal_counts = buy_coin_info.set_limit_count  # 설정코인 최소 거래 갯수 정보

##############################################################################################

   # 매도 필요 정보

    now_coin_names = sell_coin_info.my_coin_name # 보유 코인 이름
    now_up_prices = sell_coin_info.my_up_price  # 보유 코인 매도가 정보
    now_prices = sell_coin_info.my_now_price # 보유 코인 현재가 정보
    now_coin_counts = sell_coin_info.my_coin_count  # 보유코인 갯수 정보
    now_avg_buy_prices = sell_coin_info.my_coin_avg_price # 보유 코인 평균 단가

    #AI_modell_accuracy = sell_coin_info.AI_modell_accuracy # 예측 모델 정확도

##############################################################################################

    uuid_count = len(uuid)

    if uuid_count == 0:

        print('*' * 140)
        print('미채결건이 존재하지 않습니다')
        pass

    else:
        print('*' * 140)
        print('미채결 건수', len(uuid), '건 발생')
        print(uuid)

        for i in uuid:
            print('*' * 140)
            print(i)
            bithumb_info.cancel_order(i)

        print('미체결 건수 처리 완료')

        del uuid[:]  # 주문ID

    # 매수 거래 시스템

    print('*' * 140)
    print('매수거래가 시작되었습니다')

    for i, coin in enumerate(set_coin_name):
        print('*' * 140)
        print(coin, '의 거래가 시작됩니다.')

        if Profit_percent[1] > set_future_yields[i] >= Profit_percent[0]:

            buy_info = bithumb_info.buy_limit_order(coin, set_down_price[i], set_limit_deal_counts[i] * 1)

            if 'error' in buy_info[0].keys():
                pass
            else:
                uuid.append(buy_info[0]['uuid'])
                print(coin, '   ', set_limit_deal_counts[i] * 1, '개 매수 주문 되었습니다')

        elif Profit_percent[2] > set_future_yields[i] >= Profit_percent[1]:

            buy_info = bithumb_info.buy_limit_order(coin,  set_down_price[i], set_limit_deal_counts[i] * 2)

            if 'error' in buy_info[0].keys():
                pass
            else:
                uuid.append(buy_info[0]['uuid'])
                print(coin, '   ',round(set_limit_deal_counts[i] * 2), '개 매수 주문 되었습니다')

        elif set_future_yields[i] >= Profit_percent[2]:

            buy_info = bithumb_info.buy_limit_order(coin, set_down_price[i], set_limit_deal_counts[i] * 3)

            if 'error' in buy_info[0].keys():
                pass
            else:
                uuid.append(buy_info[0]['uuid'])
                print(coin, '   ', set_limit_deal_counts[i] * 3, '개 매수 주문 되었습니다')

    print('*' * 140)
    print('매도가 시작됩니다')

    for i, counts in enumerate(now_coin_counts):  # C = [z 개수 > 0 ]
        #count = float(counts)
        print(now_coin_names[i], '의 거래가 시작됩니다.')
        if counts > 0:
            sell_coin = now_coin_names[i]
            sell_event_yield = coin_tool.sell_event_yield(now_prices[i], now_up_prices[i], now_avg_buy_prices[i])
            print(sell_event_yield)
            if Profit_percent[1] > sell_event_yield >= Profit_percent[0] :
                sell_info = bithumb_info.sell_limit_order(sell_coin, now_up_prices[i], now_coin_counts[i] * (1 / 6))

                if 'error' in sell_info[0].keys():
                    pass
                else:
                    uuid.append(sell_info[0]['uuid'])
                    print(now_coin_names[i], '   ', now_coin_counts[i] * (1 / 6), '개 매도주문 하였습니다')

            elif Profit_percent[2] > sell_event_yield >= Profit_percent[1] :
                sell_info = bithumb_info.sell_limit_order(sell_coin, now_up_prices[i], now_coin_counts[i] * (2 / 6))

                if 'error' in sell_info[0].keys():
                    pass
                else:
                    uuid.append(sell_info[0]['uuid'])
                    print(now_coin_names[i], '   ', now_coin_counts[i] * (2 / 6), '개 매도주문 하였습니다')

            elif Profit_percent[2]  > sell_event_yield >= Profit_percent[1]:
                sell_info = bithumb_info.sell_limit_order(sell_coin, now_up_prices[i], now_coin_counts[i] * (3 / 6))

                if 'error' in sell_info[0].keys():
                    pass
                else:
                    uuid.append(sell_info[0]['uuid'])
                    print(now_coin_names[i], '   ', now_coin_counts[i] * (3 / 6), '개 매도주문 하였습니다')

            elif sell_event_yield > 3:

                sell_info = bithumb_info.sell_limit_order(sell_coin, now_up_prices[i], now_coin_counts[i])

                if 'error' in sell_info[0].keys():
                    pass
                else:
                    uuid.append(sell_info[0]['uuid'])
                    print(now_coin_names[i], '전량 매도 하였습니다')


            elif sell_event_yield < -1 * Profit_percent[2] * 0.30:

                sell_info = bithumb_info.sell_limit_order(sell_coin, now_up_prices[i], now_coin_counts[i])

                if 'error' in sell_info[0].keys():
                    pass
                else:
                    uuid.append(sell_info[0]['uuid'])
                    print(now_coin_names[i], '전량 매도 하였습니다')

        print(now_coin_names[i], '의 거래가 끝났습니다')
        print('*' * 140)



