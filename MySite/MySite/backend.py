import os
import datetime
from back_end.get_fault import faults_todb
from back_end.get_station import get_base_info
from back_end.get_status import delay_missing_to_db
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
    get_online()




