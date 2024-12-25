import MetaTrader5 as mt5
import sys

login = sys.argv[1]
pw = sys.argv[2]
server = sys.argv[3]

if not mt5.initialize(
        login=int(login), server=server, password=pw):
    print(f"error: {mt5.last_error()}")
else:
    account_info = mt5.account_info()._asdict()
    print(account_info)
mt5.shutdown()
