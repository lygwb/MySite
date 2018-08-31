import requests
from AWSMonitor.models import Station

# 获取某一站时间段内某要素实测数据值
#station_code:O2674
#item_name:temp
#dtbegin:2018060611000000
def get_aws_value(station_code, item_name, dtbegin, dtend ):
    url = 'http://172.18.152.207:8080/tabularsvc.gwt?compositeName=DetailObservationDataGrid1&compositeType=grid&QUERY_OPTION=BY_STATION_COMMAND_LAYER_DATERANGE&STATION_NUMBER={0}&COMMAND_NAME=DMGD&COMMAND_TIMESCALECATEGORY=MINUTELY&columns={1}&ELEMENT_VALUE_CONDITION_PARAMS=evc_date_02,{2}@{3}'.format(station_code, item_name, dtbegin, dtend)

    html_response = requests.get(url)
    json_data = html_response.json()
    aws_value = []
    for item in json_data['data']:
        aws_value.append([item['oDate'], item['e0']])
    return aws_value


# 获取某一要素最新的观测值 temp 等
def get_lastest_value(elements_name):
    url = 'http://172.18.152.120:8080/tabularsvc.gwt?compositeName=SimpleDataMatrixGrid&compositeId=SimpleDataMatrixGrid_6797708241511627028&compositeType=grid&userId=10&QUERY_OPTION=BY_LATEST_ELEMENTS&ELEMENT_NAMES={0}&DATA_CONTAINER=DMGD&SHOW_NULL_VALUE=true&USCF_ID=-1&COLUMN_COUNT=10&dir=DESC&sort={0}'.format(elements_name)
    html_response = requests.get(url)
    json_data = html_response.json()
    station_codes = Station.objects.values('stationNum')
    aws_values = []
    ly_values = []
    for item in json_data['data']:
        for sub_item in item.values():
            aws_values.append(sub_item)

    for station_code in station_codes:
        for aws_value in aws_values:
            if station_code['stationNum'] in aws_value:
                splits = aws_value.split('#')
                if (splits[4] != '-' and splits[7] == 'INTIME') or splits[7] == 'STALE':
                    ly_values.append([splits[1], splits[2], splits[3], splits[4], splits[5], splits[7]])
                    print(splits[1], splits[2], splits[3], splits[4], splits[5], splits[7])

    print(len(ly_values))


