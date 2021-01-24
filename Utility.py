from datetime import datetime
import numpy as np


def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    # slack.chat.post_message('#etf-algo-trading', strbuf)


def printlog(message, *args):
    """인자로 받은 문자열을 파이썬 셸에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)


@staticmethod
def change_format(data):
    strip_data = data.lstrip('-0')
    if strip_data == '':
        strip_data = '0'

    try:
        format_data = format(int(strip_data), ',d')
    except:
        format_data = format(float(strip_data))

    if data.startswith('-'):
        format_data = '-' + format_data

    return format_data


def list_from_csv(path):
    csv_data = np.loadtxt(path, delimiter=",", dtype=str)
    list_data = csv_data.tolist()
    return list_data

