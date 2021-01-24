from Utility import *

class SystemTrade:
    def __init__(self):
        pass

    def start_app(self):
        pass

    def check_creon_system(self):
        """시스템 연결 상태를 점검한다."""
        # 관리자 권한으로 프로세스 실행 여부

        # 연결 여부 체크

        # 주문 관련 초기화 - 계좌 관련 코드가 있을 때만 사용

        return True

    def get_current_price(self, code):
        """인자로 받은 종목의 현재가, 매수호가, 매도호가를 반환한다."""
        pass

    def get_ohlc(self, code, qty):
        """인자로 받은 종목의 OHLC 가격 정보를 qty 개수만큼 반환한다."""
        pass

    def get_stock_balance(self, code):
        """인자로 받은 종목의 종목명과 수량을 반환한다."""
        pass

    def get_current_cash(self):
        """증거금 100% 주문 가능 금액을 반환한다."""
        pass

    def get_target_price(self, code):
        """매수 목표가를 반환한다."""
        pass

    def get_movingaverage(self, code, window):
        """인자로 받은 종목에 대한 이동평균가격을 반환한다."""
        pass


    def buy_etf(self, code):
        """인자로 받은 종목을 최유리 지정가 FOK 조건으로 매수한다."""
        pass

    def sell_all(self):
        """보유한 모든 종목을 최유리 지정가 IOC 조건으로 매도한다."""
        pass
