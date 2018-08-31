
#获取站点信息 仪器信息 设备信息
import requests
import datetime
from bs4 import BeautifulSoup as Soup
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MySite.settings")
import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()
from AWSMonitor.models import Station, Instrument, Equipment
# 获取站点列表


def get_station_list(cityCode):
    url = "http://172.18.152.85:10525/hnqxjson/pStation/pStationGetStations.hd?option=0"
    try:
        html_response = requests.get(url)
        if html_response.status_code == 200:
            res_repam_all = html_response.json()
            stations = [station for station in res_repam_all['list']
            if (station['cityCode'] !=None and station['cityCode'].startswith(cityCode)
                and station['category'] == '100')
            ]
            print('{0}--获取站点信息成功'.format(datetime.datetime.now()))
            return stations

    except:
        print('{0}--获取站点信息失败'.format(datetime.datetime.now()))


# 获取站点仪器信息
def get_equips(login_name, password):
    try:
        url = 'http://192.168.70.58:8080/qxwz/login.do'
        url2 ='http://192.168.70.58:8080/qxwz/admin/StationInfo.do'
        post_data2 = {'method': 'list', 'mod_id': '108010', 'pager.pageSize': 400	}
        postdata = {'login_name': login_name, 'method': 'login', 'password': password}
        ss = requests.Session()
        ss.post(url, data=postdata)
        r = ss.post(url2, post_data2)
        content_table = Soup(r.text, 'html.parser').find(attrs={'class': 'datagrid'})
        equips = []
        for tr in content_table.findAll('tr'):
            tds = tr.findAll('td')
            if len(tds) == 11:

                equip_code = tds[1].getText()
                if equip_code == '\xa0':
                    break
                else:
                    equip_code = equip_code.strip()
                equip_name = tds[2].getText()
                make_factory = tds[5].getText()
                station_code = tds[4].getText()
                element_num = tds[7].getText()

                equip = {'equip_code': equip_code, 'equip_name': equip_name, 'make_factory': make_factory,
                                  'station_code': station_code, 'element_num': element_num}
                equips.append(equip)
        print('{0}--获取仪器信息成功'.format(datetime.datetime.now()))
        return equips
    except:
        print('{0}--获取仪器信息失败'.format(datetime.datetime.now()))


# 获取站点仪器设备信息
def get_instruments(equip_code, login_name, password):
    try:
        url = 'http://192.168.70.58:8080/qxwz/login.do'
        postdata = {'login_name': login_name, 'method': 'login', 'password': password}
        ss = requests.Session()
        ss.post(url, data=postdata)
        url3 = 'http://192.168.70.58:8080/qxwz/admin/StationInfo.do?method=viewEquip&station_two_code={0}'.format(
            equip_code)
        html_instruments = ss.post(url3)

        instrument_soup = Soup(html_instruments.text, 'html.parser')
        instrument_names = instrument_soup.findAll(attrs={'class': 'equip_name'})
        instrument_jdTs = instrument_soup.findAll(attrs={'class': 'jdt'})
        instrument_two_code = instrument_soup.findAll(attrs={'name': 'two_dimension_code'})

        instruments = []
        for i in range(len(instrument_names)):
            instrument_jdt = (instrument_jdTs[i].parent.getText()[1:29])
            instrument_jdt_date = datetime.datetime.strptime(instrument_jdt, '%a %b %d 00:00:00 CST %Y')
            instruments.append({'instrument_name': instrument_names[i].getText(),
                                'instrument_jdT': instrument_jdt_date,
                                'instrument_two_code': instrument_two_code[i].attrs['value']})
        return instruments

    except:
        print('{0}--获取仪器信息失败'.format(datetime.datetime.now()))

def get_base_info():
    stations =get_station_list('HNLY')
    index = 0
    for s in stations:
        single_station = Station(stationNum=s['stationNum'],
                                 category=int(s['category']),
                                 cityCode=s['cityCode'],
                                 description=s['description'],
                                 stationclass=s['stationclass'],
                                 isMask=s['isMask'],
                                 gprsID=s['gprsID'],
                                 province=s['province'],
                                 city=s['city'],
                                 stationName=s['stationName'],
                                 longitude=float(s['longitude']),
                                 latitude=float(s['latitude']),
                                 high=float(s['high']),
                                 builtdate=datetime.datetime.strptime(s['builtdate'], '%Y-%m-%d %H:%M:%S.%f'),
                                 lastUpdate=datetime.datetime.strptime(s['lastUpdate'], '%Y-%m-%d %H:%M:%S.%f')
                                 )
        single_station.save()
    Equipment.objects.all().delete()
    equips = get_equips('jihongli', '123456')
    index = 0
    for equip in equips:
        station = Station.objects.filter(stationNum=equip['station_code'])
        if station:
            single_equip = Equipment(equip_code=equip['equip_code'],
                                     equip_name=equip['equip_name'],
                                     element_num=equip['element_num'],
                                     make_factory=equip['make_factory'],
                                     station=Station.objects.filter(stationNum=equip['station_code']).first())
            single_equip.save()

    for equip in Equipment.objects.all():
        instruments = get_instruments(equip.equip_code, 'jihongli', '123456')
        for instrument in instruments:
            single_instrument = Instrument(instrument_code=instrument['instrument_two_code'],
                                           instrument_name=instrument['instrument_name'],
                                           equipment=equip,
                                           instrument_jdt_date=instrument['instrument_jdT']
                                           )
            single_instrument.save()


