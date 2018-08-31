import datetime
import requests
from AWSMonitor.models import Station, MissingDelay
import simplejson

# 获取最后心跳包时间和最后通讯成功时间和在线状态
def get_online():
    url = 'http://172.18.152.207:8080/tabularsvc.gwt?compositeName=StationGrid&userId=3&USCF_ID=-1'
    html_response = requests.get(url, stream=True)

    contents = simplejson.loads(html_response.text,  strict=False)
    row_count = 0
    onlines = []
    onlines_status = get_online_status()
    for item in contents['data']:
        if 'p2' in item:
            station_num = item['p2']
            if Station.objects.filter(stationNum=station_num):
                status = onlines_status.get(item['p2'])
                if status:
                    status = onlines_status[item['p2']]
                else:
                    status = ""
                last_heart = ''
                last_data_recv = ''
                if 'p14' in item:
                    last_heart = item['p14']
                    last_data_recv = item['p15']
                onlines.append({'station_code': station_num,
                                'last_heart': last_heart,
                                'last_data_recv': last_data_recv,
                                'status': status
                                })
    str_now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')
    return_json = {'data': onlines, 'count': len(onlines), 'lasttime': str_now}
    f = open('status.json', 'w')
    f.write(simplejson.dumps(return_json))
    f.close()
    return onlines

# 获取各站点的在线状态 ok：正常 ST：延迟 Off关闭 ‘’被动
def get_online_status():
    url2 = "http://172.18.152.207:8080/tabularsvc.gwt?compositeName=StationStatusMatrixGrid&compositeId=StationStatusMatrixGrid_1528340500863&compositeType=grid&userId=3&USCF_ID=-1&GROUP_DISPLAY=true&QUERY_OPTION=SHOW_ALL"
    html_response2 = requests.get(url2, stream=True)
    if html_response2.status_code == 200:
        res_repam_all = html_response2.json()
        online_status = []
        online_status_return = {}
        for row in res_repam_all['data']:
            for key in row:
                online_status.append(row[key])
        for single in online_status:
            splits = single.split(';')
            key = splits[1]
            value = splits[2]
            online_status_return[key] = value
        return online_status_return
    else:
        print(html_response2.status_code)

# 获取某一时间点逾限 缺报站点
def get_delay_missing_list(sql_datetime):
    url_missing ='http://172.18.152.120:8080/tabularsvc.gwt?compositeName=DataArrivalStationListGrid&compositeId=DataArrivalStationListGrid&compositeType=grid&QUERY_OPTION=BY_DATA_ARRIVAL_CHK_ITEM&GROUP_ID=1_60_6&COMMAND_NAME=DMGD&DATA_DATE={0}&ROOT_GROUP_ID=1_60&ITEM_CATEGORY='.format(sql_datetime.strftime('%Y-%m-%d %H:00:00'))

    html_response = requests.get(url_missing)
    if html_response.status_code == 200:
        res_repam_all = html_response.json()
        recv_not_ontime =[]
        for row in res_repam_all['data']:
            for key in row:
                if not row[key].find('IR') > 0:
                    recv_not_ontime.append(row[key])
                    print(row[key])
        return recv_not_ontime
    else:
        print(html_response.status_code)

# 将延迟 缺报站点入数据库
def delay_missing_to_db(sql_datetime):
    delay_missing = get_delay_missing_list(sql_datetime)
    if delay_missing:
        for item in delay_missing:
            station_code = item.split(';')[0]
            mis_exist = MissingDelay.objects.filter(station__stationNum=station_code)\
                .filter(mis_delay_time=sql_datetime)
            if mis_exist:
                continue
            station_query = Station.objects.filter(stationNum=station_code)
            if station_query:
                missing_delay = MissingDelay(station=station_query.first(),
                                             mis_delay_time=sql_datetime)
                if item.find('MNR') > 0:
                    missing_delay.mis_delay = 'D'
                missing_delay.save()


