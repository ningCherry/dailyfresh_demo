# Generated by Django 2.2 on 2020-02-15 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
        ('df_order', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OederDetailInfo',
            new_name='OrderDetailInfo',
        ),
    ]
