# Generated by Django 2.1.15 on 2022-08-29 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qosapp', '0009_auto_20220826_2300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meter',
            name='burst_size',
        ),
        migrations.RemoveField(
            model_name='meter',
            name='limited_rate',
        ),
        migrations.AddField(
            model_name='meter',
            name='basic',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='meter',
            name='meterBandHeaders',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='meter',
            name='meterStatistics',
            field=models.TextField(null=True),
        ),
    ]
