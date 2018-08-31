import requests
import re
import datetime

from bs4 import BeautifulSoup as Soup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MySite.settings")
import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()
from AWSMonitor.models import Station, Fault

#获取故障站点列表


def get_fault_list(user: object, password: object) -> object:

    # Create your models here.
    url = "http://10.69.10.61/login.php"
    url2 = "http://10.69.10.61/qugz.php"

    values = {'user': user, 'password': password}
    ss = requests.Session()
    ss.post(url, data=values)
    r = ss.get(url2)
    content = r.text.encode("iso-8859-1").decode('gbk').encode('utf8')
    soup = Soup(content, 'html.parser')
    trs = soup.find_all('a')
    fault_stations = []
    for a in trs:
        station_code = re.findall(r'sno=(.+?)&dy', a['href'])[0]
        date = re.findall(r'dy=(.+?)&dh', a['href'])[0]
        hour_minute = re.findall(r'dh=(.+?)&opt', a['href'])[0]
        begin_time_str = date + ' ' + hour_minute

        fault_stations.append({'station_code': station_code,
                               'begin_time': begin_time_str})
    return fault_stations


def faults_todb():
    new_faults = get_fault_list('lyqxj', '57073')
    # 如果已经好了，就将IsRecovered 设为True
    for single_old_fault in Fault.objects.filter(IsRecovered=False):
        is_old_recovered = True
        for single_new_fault in new_faults:
            if single_new_fault['station_code'] == single_old_fault.station.stationNum:
                is_old_recovered = False
        if is_old_recovered:
            single_old_fault.IsRecovered = True
            single_old_fault.save()
    # 新加或继续坏的站点
    for single_fault in new_faults:
        fault_station = Station.objects.filter(stationNum=single_fault['station_code'])
        datetime_now = datetime.datetime.now()
        begin_time = datetime.datetime.strptime(single_fault['begin_time'], '%Y-%m-%d %H:%M:%S')
        duration = round((datetime_now - begin_time).total_seconds() / 3600, 1)
        last_time_fault = Fault.objects.filter(IsRecovered=False).filter(station=fault_station.first())
        if last_time_fault:
            current_old_fault = last_time_fault.first()
            current_old_fault.duration = duration
            current_old_fault.save()
            continue
        if fault_station:
            new_fault = Fault(station=fault_station[0], start_time=begin_time, duration=duration)
            new_fault.save()
            continue

    print('从10.69.10.61获取错误站点列表成功!')
