import requests
import datetime

#user；10379GLY
#password:1234
#logonType:userFlag
#从172.18.152.226获取本区域（市区）质量控制内疑误信息
def get_226(user: object, password: object, logonType) -> object:

    # 登陆地址
    url = "http://172.18.152.226/MDOS2/logon.action"
    #未出理的
    url_un = 'http://172.18.152.226/MDOS2/queryMessageForQCRecordS.action?pageflag=3&stationType=region&elementKey=-1&startTime=2018-08-03+16%3A00%3A00&endTime=2018-09-03+16%3A00%3A0&createLevel=-1'
    url4 = 'http://172.18.152.226/MDOS2/queryMessageForQCRecordS.action?pageflag=2&stationType=region&elementKey=-1&startTime=2018-08-03+16%3A00%3A00&endTime=2018-09-03+16%3A00%3A0&createLevel=-1'
    values = {'username': user, 'userpwd': password, "logonType": logonType, 'date': datetime.datetime.now()}

    ss = requests.Session()
    ss.post(url, data=values)
    r = ss.get(url4)
    print(r.text)