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

price_map =  {'A1':'硬座', 'A2':'软座', 'A3':'硬卧', 'A4':'软卧', 'A6':'高级软卧', 'A9':'商务座/特等座', 'F':'动卧',
              'M':'一等座', 'O':'二等座', 'WZ':'无座'}
# 第一个查询，返回一个列表，每个元素都是包含一个ticket信息的复杂字符串
def query_ticket(train_date, from_station, to_station, ticket_type, logticket):
    url='https://kyfw.12306.cn/otn/leftTicket/query'
    payload = {'leftTicketDTO.train_date': train_date, #日期
           'leftTicketDTO.from_station': from_station, #起点站
           'leftTicketDTO.to_station': to_station, #目的站
           'purpose_codes': ticket_type} #车票类型
    try:
        r = requests.get(url, params=payload, headers=headers)
        data = r.json()['data']['result']
        return data 
    except Exception as e:
        time.sleep(1)
        print('延迟1秒', e)
        logticket.warn(f'延迟1秒, {e}')
        print(train_date, from_station, to_station, ticket_type)
        logticket.warn(f"{train_date}, {from_station}, {to_station}, {ticket_type}")
        return query_ticket(train_date, from_station, to_station, ticket_type, logticket)

# 对第一个查询进行格式转换，从复杂字符串中提取相关信息出来，存放在DF中
# '起点站', '列车编号', '终点站', '出发站', '到达站', '出发时间', '到达时间', '历时', '起点站发车日期', '是否可以预订', '备注', 'seat_types', '软卧',
# '无座', '商务座/特等座', '一等座', '二等座'
def trans_ticket(ticket_list):
    df_empty = pd.DataFrame(columns=['列车代码', '起点站', '列车编号', '终点站', '出发站', '到达站', '出发时间', '到达时间',
                                     '历时', '起点站发车日期', '是否可以预订', '备注', 'seat_types', '软卧',
                                     '无座', '商务座/特等座', '一等座', '二等座'])
    for ticket in ticket_list:
        ticket_split = ticket.split('|')
        # print(ticket_split[3], ticket_split[30])
        # pprint(ticket_split)
        df_empty.loc[df_empty.index.size,['备注', '列车编号', '起点站', '终点站', '出发站',
                                      '到达站', '出发时间', '到达时间',
                                      '历时', '是否可以预订', '起点站发车日期', '软卧', '无座',
                                      '二等座', '一等座', '商务座/特等座', 'seat_types', '列车代码']] = [ticket_split[1], ticket_split[2], 
                                                      ticket_split[4],
                                                      ticket_split[5], ticket_split[6], ticket_split[7],
                                                      ticket_split[8], ticket_split[9], ticket_split[10], 
                                                      ticket_split[11], ticket_split[13], ticket_split[23],
                                                      ticket_split[26], ticket_split[30], ticket_split[31],
                                                      ticket_split[32], ticket_split[35], ticket_split[3]]
    if (df_empty.empty is True):
        print(ticket_list)
    # return df_empty
    df_empty.to_csv('ticket.csv', mode='a', encoding='utf8', header=False, index=False)

# 第二个查询，输入的是出发站和到达站，而不是起点站和终点站
def query_station(train_no, from_station, to_station, date):
    url='https://kyfw.12306.cn/otn/czxx/queryByTrainNo'
    payload = {'train_no': train_no, #列车代码
           'from_station_telecode': from_station, #起点站序号
           'to_station_telecode': to_station, #终点站序号
           'depart_date': date} #日期
    r = requests.get(url, params=payload)
    return r.json()

# 第二个查询的二级封装，输入一个第一级查询的DF和日期，对DF每一行进行第二级查询，返回合并查询后的DF
# '日期', 'station_train_code', 'train_no', 'station_no', 'station_name', 'arrive_time', 'start_time',
# 'stopover_time', 'isEnabled', 'start_station_name', 'end_station_name', 'train_class_name'
def query_station2(df, day):
    df_L = []

    for index, rows in df.iterrows():
        df_empty = pd.DataFrame(columns=['日期', 'station_train_code', 'train_no', 'station_no', 'station_name',
                                            'arrive_time', 'start_time',
                                            'stopover_time', 'isEnabled', 'start_station_name', 'end_station_name', 'train_class_name'])
        tn, fs, ts = rows['列车编号'], rows['出发站'], rows['到达站']
        data = query_station(tn,fs,ts,day)['data']['data']
        for row in data:
            df_empty.loc[row['station_no'],['日期', 'station_train_code', 'train_no', 'station_no', 'station_name',
                            'arrive_time', 'start_time',
                            'stopover_time', 'isEnabled', 
                            'start_station_name', 'end_station_name', 
                            'train_class_name']] = [day, data[0]['station_train_code'], tn, row['station_no'], row['station_name'],
                                                            row['arrive_time'], row['start_time'], row['stopover_time'], row['isEnabled'],
                                                            data[0]['start_station_name'], data[0]['end_station_name'], data[0]['train_class_name']]
        df_L.append(df_empty)
        df_all = pd.concat(df_L, ignore_index=True)
    return df_all

#输入日期、起点站代码、目的站代码、车票类型，返回相关数据
def query_price(train_no, from_station_no, to_station_no, seat_types, train_date):
    url='https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice'
    payload = {'train_no': train_no, #列车代码
           'from_station_no': from_station_no, #起点站序号
           'to_station_no': to_station_no, #目的站序号
           'seat_types': seat_types, #座位类型
           'train_date': train_date} #日期
    r = requests.get(url, params=payload, headers=headers)
    return r.json()

# def query_price2():
