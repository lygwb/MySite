from django.shortcuts import render
from .models import Station, MissingDelay, Fault
import json
import os
import datetime
from django.http import HttpResponse, JsonResponse

from random import *


def index(request):
    faults = Fault.objects.filter(IsRecovered=False)
    f = open(os.getcwd()+'/MySite/status.json', 'r')
    online = json.load(f)['data']
    f.close()
    faults_view = []

    for fault in faults:
        for single_online in online:
            if single_online['station_code'] == fault.station.stationNum:
                faults_view.append({
                    'station_code': fault.station.stationNum,
                    'station_name': fault.station.stationName,
                    'begin_time': fault.start_time,
                    'duration': fault.duration,
                    'last_heart': single_online['last_heart'],
                    'last_data_recv': single_online['last_data_recv'],
                    'status': single_online['status']
                 })
    time_now = datetime.datetime.now()
    if time_now.minute>20:
        time_now = time_now + datetime.timedelta(hours=-1)
    last_aws_values = []
    values = []
    for station in Station.objects.all():
        statin_name = station.stationName
        station_num = station.stationNum
        time_aws = time_now + datetime.timedelta(minutes=-randint(0, 300))
        aws_value = round(uniform(15, 35), 1)
        last_aws_values.append([
            statin_name, station_num, aws_value, time_aws
        ])
        values.append(aws_value)
    viewmodel = {}
    value_max = max(values)
    value_min = min(values)
    value_average = round(sum(values)/len(values), 1)
    tongji ={'max':value_max,
             'min':value_min,
             'average':value_average,
             'count':len(values)}
    viewmodel['tongji'] = tongji
    viewmodel['fault'] = faults_view
    viewmodel['aws_values'] = last_aws_values
    return render(request, "AWSMonitor/index.html", context=viewmodel)
def single_station(request,station_num):
    station = Station.objects.filter(stationNum=station_num)
    if station:
        equip = station[0].equipment_set.first()
        instruments = equip.instrument_set.all()

        content = {'station':station[0],
                   'equip':equip,
                   'instruments':instruments
                   }
        historys = []
        time_now = datetime.datetime.now()
        for i in range(0,7):
            historys.append({
                'time':time_now + datetime.timedelta(days=-7+i),
                'duration': round(uniform(5, 23), 1)

            })

        content['historys'] = historys

        intimes = []
        missings = 0
        delay = 0

        for i in range(0,7):
            h24s = []
            for hour in range(0, 24):
                status = randint(0,30)
                if status==0:
                    missings +=1
                elif status == 1:
                    delay += 1
                h24s.append(status)
            intimes.append({
                'time':time_now + datetime.timedelta(days=-7+i),
                'h24s':h24s,

            })

        content['intimes'] = intimes
        content['missing'] = missings
        content['delay'] = delay
    return render(request, 'AWSMonitor/singlestation.html', content)


def single_station_intimes(request, station_num,  start, end):
    intimes = []
    missings = 0
    delay = 0
    content = {}
    d = start
    delta = datetime.timedelta(days=1)
    while d <= end:
        h24s = []
        for hour in range(0, 24):
            status = randint(0, 30)
            if status == 0:
                missings += 1
            elif status == 1:
                delay += 1
            h24s.append(status)
        intimes.append({
            'time': d,
            'h24s': h24s,})
        d += delta

    content['intimes'] = intimes
    content['missing'] = missings
    content['delay'] = delay
    return HttpResponse(json.dumps(content), content_type="application/json")


def daterange(request):
    return render(request,"AWSMonitor/daterange.html")
def battery(request):
    return render(request,"AWSMonitor/battery.html")
def tongji(request):
    tongjiinfo = {}
    tongjis= []
    tongjis.append(TongJi("市区",12000,150,55))
    tongjis.append(TongJi("孟津",96000,230,0))
    tongjis.append(TongJi("偃师",13200,350,155))
    tongjis.append(TongJi("伊川",14400,250,155))
    tongjis.append(TongJi("汝阳",10800,350,45))
    tongjis.append(TongJi("嵩县",12000,250,0))
    tongjis.append(TongJi("栾川",13200,280,155))
    tongjis.append(TongJi("宜阳",7200,250,155))
    tongjis.append(TongJi("洛宁",9600,320,255))
    tongjis.append(TongJi("嵩县",8400,250,5))
    tongjis = sorted(tongjis, key=lambda tj: -tj.intime_perc)
    count, missing, delay = 0, 0, 0
    for tj in tongjis:
        count += tj.count

    tongjiinfo["tongjis"] = tongjis
    return render(request,"AWSMonitor/tongji.html", context=tongjiinfo)

class TongJi(object):
    def __init__(self, name, count ,missing, delay):
        self.name = name
        self.count = count
        self.missing = missing
        self.delay = delay
        self.intime = self.count - self.missing -self.delay
        self.missing_perc = round(self.missing*100/self.count, 2)
        self.delay_perc = round(self.delay*100/self.count, 2)
        self.intime_perc = round(self.intime*100/self.count, 2)



def jtest(request):
    tongjis = []
    tongjis.append(TongJi("市区", 12000, 150, 55))
    tongjis.append(TongJi("孟津", 96000, 230, 0))
    tongjis.append(TongJi("偃师", 13200, 350, 155))
    tongjis.append(TongJi("伊川", 14400, 250, 155))
    tongjis.append(TongJi("汝阳", 10800, 350, 45))
    tongjis.append(TongJi("嵩县", 12000, 250, 0))
    tongjis.append(TongJi("栾川", 13200, 280, 155))
    tongjis.append(TongJi("宜阳", 7200, 250, 155))
    tongjis.append(TongJi("洛宁", 9600, 320, 255))
    tongjis.append(TongJi("嵩县", 8400, 250, 5))
    tongjis = sorted(tongjis, key=lambda tj: -tj.intime_perc)
    # print(json.dumps(tongjis))
    return render(request, 'AWSMonitor/jquerytest.html', {
        'List': ['a','b','c'],
        'tongji':{'name':tongjis[0].name}
    })