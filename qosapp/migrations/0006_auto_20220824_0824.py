# Generated by Django 2.1.15 on 2022-08-24 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qosapp', '0005_auto_20220824_0734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='basic',
            field=models.TextField(),
        ),
    ]