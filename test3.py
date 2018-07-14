import json
from itertools import permutations
from IPython.display import display
from pprint import pprint
from query_function import query_ticket, trans_ticket, query_station, query_station2, query_price

with open("station_data//station_name_map.json", "r", encoding='utf8') as f:
    data = json.load(f)
train_code_list = [station['站点代码'] for station in data.values()][:10] #2747个站点
day, ty = '2018-07-23', 'ADULT'
for x in permutations(train_code_list, 2):
    ss, es = x[0], x[1]
    rawtiket_data = query_ticket(day, ss, es, ty)
    ticket_data = trans_ticket(rawtiket_data)
    display(ticket_data)
# day, ss, es, ty = '2018-07-23', 'BJP', 'SHH', 'ADULT'
# rawtiket_data = query_ticket(day, ss, es, ty)
# ticket_data = trans_ticket(rawtiket_data)
# df = ticket_data
# print(ticket_data)
# station_data = query_station2(ticket_data, day)
# print(station_data)






# (tn, fno, tno, st, dd) = ['240000G1032F', '01', '10', 'OM9', '2018-07-23']
# for i in range(10):
#     price_data = query_price(tn, fno, f"{str(i).zfill(2)}", st, dd)
#     # print(price_data['data'])
#     print(price_data)

# df_L = []
# for index, rows in df.iterrows():
#     df_empty = pd.DataFrame(columns=['日期', 'train_no', 'from_station_no', 'to_station_no', 
#                                      'A1', 'A2', 'A3', 'A4', 'A6', 'A9', 'F', 'M', 'O', 'WZ'])
    # tn, fs, ts = rows['列车编号'], rows['出发站'], rows['到达站']
    # data = query_station(tn,fs,ts,day)['data']['data']
    # for row in data:
    #     df_empty.loc[row['station_no'],['日期', 'station_train_code', 'train_no', 'station_no', 'station_name',
    #                     'arrive_time', 'start_time',
    #                     'stopover_time', 'isEnabled', 
    #                     'start_station_name', 'end_station_name', 
    #                     'train_class_name']] = [day, data[0]['station_train_code'], tn, row['station_no'], row['station_name'],
    #                                                     row['arrive_time'], row['start_time'], row['stopover_time'], row['isEnabled'],
    #                                                     data[0]['start_station_name'], data[0]['end_station_name'], data[0]['train_class_name']]
    # df_L.append(df_empty)
    # df_all = pd.concat(df_L, ignore_index=True)