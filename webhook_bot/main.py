import pandas as pd
import datetime
import time
import ccxt
import pprint as pp

hourly_interval = 0
horizon = 0
profit_margin = 0

#ポジション情報を取得
# return {'side':side, 'size':size, 'pnl':pnl, 'value':value}
def get_bybit_position(bybit, symbol):
    poss = bybit.privateLinearGetPositionList({"symbol": symbol})['result']
    size = pnl = value = 0.0
    # print(poss)
    for p in poss:
        if p['side'] == 'Buy':
            size += float(p['size'])
            pnl += float(p['unrealised_pnl'])
            value += float(p['position_value'])
        if p['side'] == 'Sell':
            size -= float(p['size'])
            pnl += float(p['unrealised_pnl'])
            value += float(p['position_value'])
    if size == 0: 
        side = 'NONE'
    elif size > 0:
        side = 'BUY'
    else:
        side = 'SELL'
    return {'side':side, 'size':size, 'pnl':pnl, 'value':value}

#Bybitへ注文
def order_bybit(exchange, symbol, order_side, order_size):
    order = exchange.private_linear_post_order_create(
        {
            "side": order_side,
            "symbol": symbol,
            "order_type": "Market",
            "qty": order_size,
            "time_in_force": "GoodTillCancel",
            "reduce_only": False,
            "close_on_trigger": False
        }
    )
    print(order)



def main():
    df_tmp = pd.read_pickle('./alert_tmp.pkl')
    

    while True:
        #ポジション確認
        position = get_bybit_position(exchange, symbol='BTCUSDT')

        if position["side"] == "NONE":
                print("NONE")
        else:
            # ポジション有り
            print(position["side"])
            print(position["size"])
            print(position["pnl"])
            print(position["value"])
            print(position["pnl"] / position["value"] * 100 * 100 )

            if position["pnl"] / position["value"] * 100 * 100 >= profit_margin:
                print('利確')


        df_new = pd.read_pickle('./alert_tmp.pkl')

        # アラート確認
        if df_tmp.equals(df_new):
            # 更新無し
            print('更新無し')
            time.sleep(hourly_interval * 3)
            
        else:
            # 更新有り
            df_tmp = df_new
            

        print(df_tmp)
        

        #ポジション確認間隔
        time.sleep(hourly_interval * 6)
if __name__ == '__main__':


    hourly_interval = 1
    horizon = 2
    profit_margin = 25  # %
    
    exchange = ccxt.bybit({"apiKey":apiKey, "secret":secretKey})
    # print(order_bybit(exchange, symbol='BTCUSDT', order_side='Sell', order_size=0.01))


    main()
