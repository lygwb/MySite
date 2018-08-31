from django.db import models


class Fault(models.Model):
    station = models.ForeignKey("Station", verbose_name='站名', on_delete=models.CASCADE)
    start_time = models.DateTimeField('故障起始')
    duration = models.FloatField('持续时间')
    IsRecovered = models.BooleanField('已恢复', default=False)

    class Meta:
        verbose_name_plural = '故障列表'


class MissingDelay(models.Model):
    Missing_Delay = (
        ('M', 'Missing'),
        ('D', 'Delay'),
     )
    station = models.ForeignKey("Station", verbose_name='站名', on_delete=models.CASCADE)
    mis_delay_time = models.DateTimeField('时间')
    mis_delay = models.CharField('缺报/逾限', default='M', choices=Missing_Delay, max_length=1)


class Station(models.Model):
    category = models.IntegerField('类型', default=100)
    stationNum = models.CharField('区站号', max_length=5, default='57073')
    cityCode = models.CharField('所属地区', max_length=5, default='HNLY')
    description = models.CharField('说明', max_length=5, default='57073')
    stationclass = models.CharField(max_length=1)
    isMask = models.CharField(max_length=1)
    gprsID = models.CharField(max_length=11)
    province = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    stationName = models.CharField(max_length=10)
    longitude = models.FloatField('经度')
    latitude = models.FloatField('纬度')
    high = models.FloatField('海拔高度')
    builtdate = models.DateTimeField('创建时间')
    lastUpdate = models.DateTimeField('修改时间')
    address = models.CharField('地址', max_length=100)
    mobileNum = models.CharField('手机号', max_length=11)

    class Meta:
        verbose_name_plural = '站点信息列表'


class Equipment(models.Model):
    equip_code = models.CharField('仪器编码', max_length=34)
    equip_name = models.CharField('仪器名称', max_length=20)
    make_factory = models.CharField('制造厂家', max_length=30)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    instrumentNum = models.IntegerField('设备个数', default=0)
    element_num = models.IntegerField('要素个数', default=0)

    def __str__(self):
        return self.equip_name

    class Meta:
        verbose_name_plural = '仪器列表'


class Instrument(models.Model):
    instrument_code = models.CharField('设备编码', max_length=34)
    instrument_name = models.CharField('设备名称', max_length=30)
    equipment = models.ForeignKey('Equipment', verbose_name='所属仪器', on_delete=models.CASCADE)
    instrument_jdt_date = models.DateTimeField('到检日期', null=True)

    class Meta:
        verbose_name_plural = '设备列表'

    def __str__(self):
        return self.instrument_name

