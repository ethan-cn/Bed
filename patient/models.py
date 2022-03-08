from django.db import models
from django.contrib.auth.models import User
from bed.models import Bed


class Patient(models.Model):
    GENDER_CHOICES = (
        (0, '男'),
        (1, '女')
    )
    patient_id = models.AutoField(primary_key = True)
    name = models.CharField('姓名', default='', max_length=50)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    age = models.CharField('年龄',default='',max_length=50)
    department = models.CharField('科室', default='', max_length=50)
    created = models.DateTimeField('入院时间', auto_now_add=True)
    modified = models.DateTimeField('出院时间', auto_now=True)
    description = models.TextField('病历描述', null=True)
    patient_bed_id = models.OneToOneField(Bed, null=True,blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'patient'


class Department(models.Model):
    department_id = models.AutoField(primary_key = True)
    name = models.CharField('科室名称', default='', max_length=50)
    doctor_name = models.CharField('主治医生',default='', max_length=50)
    addr = models.IntegerField('楼层', default='')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'