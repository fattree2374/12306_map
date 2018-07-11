import time
import requests
import pandas as pd
from pprint import pprint

headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
         'Accept': '*/*',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
         'Cache-Control': 'no-cache',
         'Connection': 'keep-alive',
        #  'Cookie': 'JSESSIONID=87D34B368A5D0973EDA348879BF5A133; route=c5c62a339e7744272a54643b3be5bf64; RAIL_EXPIRATION=1531382078259; RAIL_DEVICEID=V6rA7TcAJzuR09qGWIMGHSS2NJ-ll9sDe4CzOj43SpTKRr_ZLjv-cdemhZvCuMF9NFeU7Cz5XUQlfAv31VP1bXpLjPhM47t6TRqBuNdkubF3EMNG88aKaqOuEtGucpNWFesrxaG-AZLfIihw0-AMFicKoF2Fo9g2; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2018-07-23; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; BIGipServerportal=3134456074.17695.0000; BIGipServerotn=1658388746.50210.0000; _jc_save_toDate=2018-07-10',
         'DNT': '1',
         'Host': 'kyfw.12306.cn',
         'If-Modified-Since': '0',
         'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init'}

# 第一个查询
def query_ticket(train_date, from_station, to_station, ticket_type):
    url='https://kyfw.12306.cn/otn/leftTicket/query'
    payload = {'leftTicketDTO.train_date': train_date, #日期
           'leftTicketDTO.from_station': from_station, #起点站
           'leftTicketDTO.to_station': to_station, #目的站
           'purpose_codes': ticket_type} #车票类型
    try:
        r = requests.get(url, params=payload, headers=headers)
        data = r.json()['data']['result']
        return data
    except Exception:
        time.sleep(1)
        print('延迟1秒')
        query_ticket(train_date, from_station, to_station, ticket_type)

def trans_ticket(ticket_list):
    df_empty = pd.DataFrame(columns=['起点站', '列车编号', '终点站', '出发站', '到达站', '出发时间', '到达时间',
                                     '历时', '起点站发车日期', '是否可以预订', '备注', 'seat_types', '软卧',
                                     '无座', '商务座/特等座', '一等座', '二等座'])
    for ticket in ticket_list:
        ticket_split = ticket.split('|')
        # print(ticket_split[3], ticket_split[30])
        # pprint(ticket_split)
        df_empty.loc[ticket_split[3],['备注', '列车编号', '起点站', '终点站', '出发站',
                                      '到达站', '出发时间', '到达时间',
                                      '历时', '是否可以预订', '起点站发车日期', '软卧', '无座',
                                      '二等座', '一等座', '商务座/特等座', 'seat_types']] = [ticket_split[1], ticket_split[2], 
                                                      ticket_split[4],
                                                      ticket_split[5], ticket_split[6], ticket_split[7],
                                                      ticket_split[8], ticket_split[9], ticket_split[10], 
                                                      ticket_split[11], ticket_split[13], ticket_split[23],
                                                      ticket_split[26], ticket_split[30], ticket_split[31],
                                                      ticket_split[32], ticket_split[35]]

    return df_empty

# 第二个查询，输入的是出发站和到达站，而不是起点站和终点站
def query_station(train_no, from_station, to_station, date):
    url='https://kyfw.12306.cn/otn/czxx/queryByTrainNo'
    payload = {'train_no': train_no, #列车代码
           'from_station_telecode': from_station, #起点站序号
           'to_station_telecode': to_station, #终点站序号
           'depart_date': date} #日期
    r = requests.get(url, params=payload)
    return r.json()

def trans_station(df, day):
    df_empty = pd.DataFrame(columns=['日期', 'station_train_code', 'station_no', 'station_name',
                                     'arrive_time', 'start_time',
                                     'stopover_time', 'isEnabled'])
    for index, row in df.iterrows():
        # print(index,row['出发站'], row['到达站'], row['起点站'], row['终点站'], row['列车编号'])
        stations_data = query_station(row['列车编号'], row['出发站'], row['到达站'], day)['data']['data']
        for sd in stations_data:
            df_empty.loc[1,['日期', 'station_train_code', 'station_no', 'station_name',
                                     'arrive_time', 'start_time',
                                     'stopover_time', 'isEnabled']] = [day, index, sd['station_no'], sd['station_name'],
                                                                       sd['arrive_time'], sd['start_time'], sd['stopover_time'], sd['isEnabled']]
    return df_empty

day, ss, es, ty = '2018-07-23', 'BJP', 'SHH', 'ADULT'
rawtiket_data = query_ticket(day, ss, es, ty)
ticket_data = trans_ticket(rawtiket_data)
print(ticket_data)
station_data = trans_station(ticket_data, day)
print(station_data)
