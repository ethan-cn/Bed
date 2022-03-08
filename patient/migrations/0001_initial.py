# Generated by Django 2.2.12 on 2021-02-10 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50, verbose_name='姓名')),
                ('gender', models.SmallIntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性别')),
                ('age', models.CharField(default='', max_length=50, verbose_name='年龄')),
                ('department', models.CharField(default='', max_length=50, verbose_name='科室')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='入院时间')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='出院时间')),
                ('description', models.TextField(null=True, verbose_name='病历描述')),
                ('patient_bed_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bed.Bed')),
            ],
            options={
                'db_table': 'patient',
            },
        ),
    ]
