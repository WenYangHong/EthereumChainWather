import sys
import signal
import threading
import time
from all import Web3Tranaction
from datetime import datetime
Web3Tranaction = Web3Tranaction()
def quit(signum, frame):
    sys.exit()

def process_fun():
    # 查询区块上的数据 每隔10秒执行一次
    while True:
        Web3Tranaction.getTranaction()
        time.sleep(10)

# 守护进程
if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)

        p = threading.Thread(target=process_fun)
        #注册成为主进程
        p.setDaemon(True)
        p.start()

        #如果没有主进程, 就用循环代理
        while True:
            pass

    except Exception as e:
        pass


