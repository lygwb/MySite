# Generated by Django 2.0.3 on 2018-05-23 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AWSMonitor', '0002_auto_20180523_0314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrument',
            name='make_factory',
        ),
        migrations.AddField(
            model_name='instrument',
            name='instrument_jdt_date',
            field=models.DateTimeField(null=True, verbose_name='到检日期'),
        ),
    ]
