from django.db import models
from django.contrib.auth.models import User
from bed.models import Bed


class Patient(models.Model):
    GENDER_CHOICES = (
        (0, 'Male'),
        (1, 'Female')
    )
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField('Name', default='', max_length=50)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='Gender')
    age = models.CharField('Age', default='', max_length=50)
    department = models.CharField('Department', default='', max_length=50)
    created = models.DateTimeField('Admission time', auto_now_add=True)
    modified = models.DateTimeField('Discharge time', auto_now=True)
    description = models.TextField('Medical history description', null=True)
    patient_bed_id = models.OneToOneField(Bed, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'patient'


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField('Department name', default='', max_length=50)
    doctor_name = models.CharField('Doctor', default='', max_length=50)
    addr = models.IntegerField('Floor', default='')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'
