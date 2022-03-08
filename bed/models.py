from django.db import models
from django.contrib.auth.models import User


# 导入Django自带用户模块

# 文章
class Bed(models.Model):
    STATUS_CHOICES = (
        (0, '空'),
        (1, '有人')
    )
    bed_id = models.AutoField(primary_key=True)
    bed_name = models.CharField('床位名称', max_length=70)
    price = models.IntegerField('床位价格', default='')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name='床位状态')

    def __str__(self):
        return self.bed_name

    class Meta:
        db_table = 'bed'
