# Generated by Django 2.2.12 on 2021-02-10 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('bed_id', models.AutoField(primary_key=True, serialize=False)),
                ('bed_name', models.CharField(max_length=70, verbose_name='Bed name')),
                ('price', models.IntegerField(default='', verbose_name='Bed price')),
                ('status', models.SmallIntegerField(choices=[(0, 'Empty'), (1, 'Occupied')], default=0, verbose_name='Bed status')),
            ],
            options={
                'db_table': 'bed',
            },
        ),
    ]
