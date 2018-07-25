import json
from itertools import permutations
from IPython.display import display
from pprint import pprint
import pandas as pd
from query_function2 import query_ticket, trans_ticket, query_station, query_station2, query_price
# from qlog import Logger
import logging
from multiprocessing import Pool

logticket = logging.getLogger('MainLog')
logticket.setLevel(logging.DEBUG)
fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
fh = logging.FileHandler('log//ticket.log', encoding='utf8')
fh.setFormatter(fmt)
fh.setLevel(logging.DEBUG)
logticket.addHandler(fh)

train_code_list = ['BJP', 'SHH', 'TJP', 'CQW', 'CSQ', 'CCT', 'CDW', 'FZS', 'GZQ', 'GIW', 'HHC', 'HBB', 'HFH', 'HZH', 'VUQ', 'JNK', 'KMM', 'LSO', 'LZJ', 'NNZ', 'NJH', 'NCG', 'SYT',
'SJP', 'TYV', 'WMR', 'WHN', 'XNO', 'XAY', 'YIJ', 'ZZF', 'SZQ', 'XMS']

def single_task(x):
    day, ty = '2018-07-29', 'ADULT'
    logticket = logging.getLogger("MainLog")
    logticket.info(f"正在查询{x[0]},{x[1]}")
    ss, es = x[0], x[1]
    rawtiket_data = query_ticket(day, ss, es, ty, logticket)
    if(len(rawtiket_data)!=0):
        trans_ticket(rawtiket_data)

if __name__ =='__main__':
    df_empty = pd.DataFrame(columns=['列车代码', '起点站', '列车编号', '终点站', '出发站', '到达站', '出发时间', '到达时间',
                                     '历时', '起点站发车日期', '是否可以预订', '备注', 'seat_types', '软卧',
                                     '无座', '商务座/特等座', '一等座', '二等座'])
    df_empty.to_csv('ticket.csv', index=False, encoding='utf8')
    # with open("station_data//station_name_map.json", "r", encoding='utf8') as f:
    #     data = json.load(f)
    
    # train_code_list = [station['站点代码'] for station in data.values()][:10] #2747个站点
    # train_code_list = [station['站点代码'] for station in data.values()] #2747个站点
    
    with Pool(8) as p:
        p.map(single_task, permutations(train_code_list, 2))
    # for x in permutations(train_code_list, 2):
    #     single_task(x)

    df_all = pd.read_csv('ticket.csv', encoding='utf8')
    print(df_all)
    df_all_2 = df_all.drop_duplicates()
    df_all_2.to_csv('ticket2.csv', encoding='utf8', index=False)
    print(df_all.shape)
    logticket.info(f"总DFshape为{df_all.shape}")
    print(df_all_2.shape)
    logticket.info(f"去重后DFshape为{df_all_2.shape}")
