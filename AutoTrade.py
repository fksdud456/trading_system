

from CreonTrade import *
from KiwoomTrade import *


# code = ''
# slack = Slacker(code)
import time
import os

os.system('taskkill /IM coStarter* /F /T')
os.system('taskkill /IM CpStart* /F /T')
os.system('wmic process where "name like \'%coStarter%\'" call terminate')
os.system('wmic process where "name like \'%CpStart%\'" call terminate')
time.sleep(5)

time.sleep(60)

if __name__ == '__main__':
    trade = CreonTrade()
    try:
        symbol_list = ['A122630', 'A252670', 'A233740', 'A250780', 'A225130',
                       'A280940', 'A261220', 'A217770', 'A295000', 'A176950']
        bought_list = []  # 매수 완료된 종목 리스트
        target_buy_count = 5  # 매수할 종목 수
        buy_percent = 0.19
        printlog('check_creon_system() :', trade.check_creon_system())  # 크레온 접속 점검
        stocks = trade.get_stock_balance('ALL')  # 보유한 모든 종목 조회
        total_cash = int(trade.get_current_cash())  # 100% 증거금 주문 가능 금액 조회
        buy_amount = total_cash * buy_percent  # 종목별 주문 금액 계산
        trade.set_buy_amount(buy_amount)
        printlog('100% 증거금 주문 가능 금액 :', total_cash)
        printlog('종목별 주문 비율 :', buy_percent)
        printlog('종목별 주문 금액 :', buy_amount)
        printlog('시작 시간 :', datetime.now().strftime('%m/%d %H:%M:%S'))
        soldout = False;

        while True:
            t_now = datetime.now()
            t_9 = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
            t_start = t_now.replace(hour=9, minute=5, second=0, microsecond=0)
            t_sell = t_now.replace(hour=15, minute=15, second=0, microsecond=0)
            t_exit = t_now.replace(hour=15, minute=20, second=0, microsecond=0)
            today = datetime.today().weekday()
            if today == 5 or today == 6:  # 토요일이나 일요일이면 자동 종료
                printlog('Today is', 'Saturday.' if today == 5 else 'Sunday.')
                sys.exit(0)
            if t_9 < t_now < t_start and soldout == False:
                soldout = True
                trade.sell_all()
            if t_start < t_now < t_sell:  # AM 09:05 ~ PM 03:15 : 매수
                for sym in symbol_list:
                    if len(bought_list) < target_buy_count:
                        trade.buy_etf(sym)
                        time.sleep(1)
                if t_now.minute == 30 and 0 <= t_now.second <= 5:
                    trade.get_stock_balance('ALL')
                    time.sleep(5)
            if t_sell < t_now < t_exit:  # PM 03:15 ~ PM 03:20 : 일괄 매도
                if trade.sell_all() == True:
                    dbgout('`sell_all() returned True -> self-destructed!`')
                    sys.exit(0)
            if t_exit < t_now:  # PM 03:20 ~ :프로그램 종료
                dbgout('`self-destructed!`')
                sys.exit(0)
            time.sleep(3)
    except Exception as ex:
        dbgout('`main -> exception! ' + str(ex) + '`')
