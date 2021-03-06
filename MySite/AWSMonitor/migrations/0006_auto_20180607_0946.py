# Generated by Django 2.0.3 on 2018-06-07 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AWSMonitor', '0005_missingdelay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='station',
            name='county',
        ),
        migrations.RemoveField(
            model_name='station',
            name='latitudebak',
        ),
        migrations.RemoveField(
            model_name='station',
            name='longitudebak',
        ),
        migrations.RemoveField(
            model_name='station',
            name='photoFile',
        ),
        migrations.RemoveField(
            model_name='station',
            name='photoFile1',
        ),
        migrations.RemoveField(
            model_name='station',
            name='photoFile2',
        ),
        migrations.RemoveField(
            model_name='station',
            name='photoFile3',
        ),
        migrations.RemoveField(
            model_name='station',
            name='photoFile4',
        ),
        migrations.AlterField(
            model_name='station',
            name='cityCode',
            field=models.CharField(default='HNLY', max_length=5, verbose_name='所属地区'),
        ),
    ]
