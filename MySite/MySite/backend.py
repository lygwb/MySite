import os
import datetime
from back_end.get_fault import faults_todb
from back_end.get_station import get_base_info
from back_end.get_status import delay_missing_to_db, get_delay_missing_list
from back_end.get_aws_value import get_aws_value, get_lastest_value
from AWSMonitor.models import MissingDelay
from  back_end.get_status import get_online, get_online_status
from back_end.my_timer import my_timer_interface
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MySite.settings")
import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()
if __name__ == "__main__":
    #获取站点 仪器 配件信息到数据库
    #get_base_info()

    # 获取错误站点列表 从10.69.10.61
    #faults_todb()

    #获取心调包时间和最后通讯时间
    #get_online()

    # 获取各站点的在线状态 ok：正常 ST：延迟 Off关闭 ‘’被动
    #get_online_status()

    get_delay_missing_list(datetime.datetime.now())






