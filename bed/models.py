from django.db import models
from django.contrib.auth.models import User



# 
class Bed(models.Model):
    STATUS_CHOICES = (
        (0, 'Empty'),
        (1, 'Occupied')
    )
    bed_id = models.AutoField(primary_key=True)
    bed_name = models.CharField('Bed number', max_length=70)
    price = models.IntegerField('Bed price', default='')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name='Bed status')

    def __str__(self):
        return self.bed_name

    class Meta:
        db_table = 'bed'
