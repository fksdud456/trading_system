from SystemTrade import *
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from pandas import DataFrame
import account


class KiwoomTrade(QAxWidget, SystemTrade):
    # todo: rq list
    # rqlist = {
    #     'opt10081_req': self._opt10081()
    # }
    stock_list = []

    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)
        self.OnReceiveRealData.connect(self._receive_real_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        res = self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                               [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])
        print('send_order: ', res)

    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _comm_real_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("GetCommRealData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False
        exec('self._' + rqname.split('_')[0] + '(rqname, trcode)')

        # try:
        #     self.tr_event_loop.exit()
        # except AttributeError:
        #     pass

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print('_receive_chejan_data')
        print(gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

    def _receive_real_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)
        elif rqname == "opw00001_req":
            self._opw00001(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opw00001(self, rqname, trcode):
        self.d2_deposit = self._comm_get_data(trcode, "", rqname, 0, "d+2추정예수금")

    def _opw00018(self, rqname, trcode):
        total_purchase_price = self._comm_get_data(trcode, "", rqname, 0, "총매입금액")
        total_eval_price = self._comm_get_data(trcode, "", rqname, 0, "총평가금액")
        total_eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, 0, "총평가손익금액")
        total_earning_rate = self._comm_get_data(trcode, "", rqname, 0, "총수익률(%)")
        estimated_deposit = self._comm_get_data(trcode, "", rqname, 0, "추정예탁자산")

        rows = self._get_repeat_cnt(trcode, rqname)
        for i in range(rows):
            name = self._comm_get_data(trcode, "", rqname, i, "종목명")
            quantity = self._comm_get_data(trcode, "", rqname, i, "보유수량")
            purchase_price = self._comm_get_data(trcode, "", rqname, i, "매입가")
            current_price = self._comm_get_data(trcode, "", rqname, i, "현재가")
            eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, i, "평가손익")
            earning_rate = self._comm_get_data(trcode, "", rqname, i, "수익률(%)")

            print(name, quantity, purchase_price, current_price, eval_profit_loss_price, earning_rate)


    def get_current_price(self, code):
        # 호가요청
        self.set_input_value("종목코드", code)
        self.comm_rq_data("opt10004_req", "opt10004", 0, "2000")

        # 현재가
        self.set_input_value("종목코드", code)
        self.comm_rq_data("opt10001_req", "opt10001", 0, "2000")

    # get_current_price
    def _opt10004(self, rqname, trcode):
        rows = self._get_repeat_cnt(trcode, rqname)
        for i in range(rows):
            h1 = self._comm_get_data(trcode, "", rqname, i, "매도최우선호가")
            h2 = self._comm_get_data(trcode, "", rqname, i, "매수최우선호가")
            print(h1, h2)

    def _opt10001(self, rqname, trcode):
        print(self._comm_get_data(trcode, "", rqname, 0, "현재가"))
        print(self._comm_get_data(trcode, "", rqname, 0, "종목명"))
        print(self._comm_get_data(trcode, "", rqname, 0, "PER"))
        self.stock_list.append({})
        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    # 이건 한 번만 호출해서 theme 별, 종목코드 다 저장해두고
    # 내 종목코드가 어떤 테마에 속하는지 db에서 검색해서 가져오면 될 듯
    # db에 있을건 내 종목의 .. 그거랑
    # theme 관련된건 다른 db
    def get_sector_list(self):
        # 테마 코드와 그룹의 리스트를 반환한다
        # 반환값의
        # 코드와 코드명 구분은 ‘ | ’
        # 코드의 구분은 ‘;’
        # Ex) 100 | 태양광_폴리실리콘; 152 | 합성섬유
        ret = self.dynamicCall("GetThemeGroupList(int)", 0)  # 0: 코드>명
        code = ret.split(';')
        sector_dict = {}
        for i in code:
            sector_list = i.split('|')
            sector_dict.update({sector_list[0]: sector_list[1]})

        return sector_dict

    def get_sector_group_code(self, sector_list):
        """
        :param sector_list: list of sector code
        :return: ticker, sector(code) dict
        """
        print(sector_list)
        ticker_list = []
        for sector in sector_list:
            # 테마코드에 해당하는 종목코드를 반환한다.
            # 반환값의 종목코드간 구분은 ‘;’
            ret = self.dynamicCall("GetThemeGroupCode(QString)", sector)
            for ticker in ret.split(';'):
                # ticker_dict.update({'ticker': ticker, 'sector': sector})
                ticker_list.append({'ticker': ticker, 'sector': sector})
        return ticker_list


if __name__ == "__main__":
    # Execute once a week (for version update)
    # app.start(r'C:\Users\user\Documents\주식매매시스템\KOAStudioSA\KOAStudioSA.exe')
    # app.start(r'C:\CREON\STARTER\coStarter.exe /prj:cp /id:hwangho0 /pwd:nasca0.. /pwdcert:5099jina.. /autostart')

    # 연결 (모의투자용 계좌)
    app = QApplication(sys.argv)
    kiwoom = KiwoomTrade()
    kiwoom.comm_connect()

    account_number = kiwoom.get_login_info("ACCNO")
    account_number = account_number.split(';')[0]

    # # d2 예수금
    # kiwoom.set_input_value("계좌번호", account_number)
    # kiwoom.set_input_value("비밀번호", account.kiwoom['simple_pw'])
    #
    # kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")
    # print(kiwoom.d2_deposit)
    #
    # # 총매입금액, 총평가금액, 총평가손익금액, 총수익률, 추정예탁자산을
    # kiwoom.set_input_value("계좌번호", account_number)
    # kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")
    #
    # # 현재가
    # kiwoom.set_input_value("종목코드", 'A122630')
    # kiwoom.comm_rq_data("opt10001_req", "opt10001", 0, "2000")

    # 주문
    # kiwoom.send_order(rqname='send_order_req',
    #                   screen_no='0101',
    #                   acc_no=account_number,
    #                   # {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
    #                   order_type=1,
    #                   # 종목코드
    #                   code='000660',
    #                   # 주문 갯수
    #                   quantity=10,
    #                   price=0,
    #                   # hoga {'지정가': "00", '시장가': "03"}
    #                   hoga='03',
    #                   order_no="")

    sector_dict = kiwoom.get_sector_list()
    ticker_list = kiwoom.get_sector_group_code(sector_dict.keys())
    print('ticker_list: ', ticker_list)
    a = 0
    # 전체를 다 update할 필요가 있는지 모르겠네.. 내 종목 중에서만
    for ticker in ticker_list:
        # 'ticker': ticker, 'sector': sector
        print(ticker)
        kiwoom.set_input_value("종목코드", ticker['ticker'])
        kiwoom.comm_rq_data("opt10001_req_" + ticker['ticker'], "opt10001", 0, "2000")
        a += 1
        if a == 5:
            break
    print(kiwoom.stock_list)

    # ticker(primary)
    # sector(code)
    # name( = ticker)
    # dividend
    # 배당금(1 회)
    # period(Y / Q / M)
    # dividend
    # yield (배당률? %)
    # PER
    # 월평균성장률( %)?
    # criteria(성장 / 테마 / 배당 / 배당서앙 / 가치