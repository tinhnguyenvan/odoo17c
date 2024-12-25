import MetaTrader5 as mt5
from datetime import datetime
import sys

login = sys.argv[1]
pw = sys.argv[2]
server = sys.argv[3]


start_time = datetime(1970, 1, 1)
end_time = datetime.now()

mt5.initialize(login=int(login), password=pw, server=server)

start_time = datetime(2020, 1, 1)
end_time = datetime.now()

deals = mt5.history_deals_get(start_time, end_time)
results = []
if deals:
    for deal in deals:
        print(deal._asdict())
        #results.append(deal._asdict())
    #print(results)
mt5.shutdown()
