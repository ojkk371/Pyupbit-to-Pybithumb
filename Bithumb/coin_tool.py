
def price_yield(now_price ,future_price): # 미래가격 대비 현제가 수익율 계산

    fees = now_price *0.005
    y = ((future_price - now_price - fees) / now_price) * 100

    return round(y ,2)



def limit_deal_count(now_price): # 코인 거래 최소 단위

    limit_count = 600 / now_price

    # if limit_count < 0:
    #     return limit_count
    # else:
    #     return round
    return round(limit_count,4)


def sell_event_yield(now_price ,up_prices ,now_avg_buy_prices):  # [(현재가-평균단가-수수료)/현재가*100] 수익률

    fees = now_price *0.005
    y = ((now_avg_buy_prices - up_prices - fees) / now_avg_buy_prices) * 100 * -1

    return round(y ,2)