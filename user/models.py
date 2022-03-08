from django.db import models
from django.contrib.auth.models import User

Permission = (
    ('VISITOR','普通用户'),
    ('UPDATE','修改权限'),
    # 删除的权限
    ('DELETE', '删除用户'),
    # 新增的权限
    ('ADD', '新增用户'),
    # 管理员的权限，增删改查
    ('ADMIN', '管理员权限')
)


class Role(models.Model):
    ROLE_CHOICES = (
        (0, '医生'),
        (1, '护士'),
        (2, '护士长')
    )
    role_code = models.CharField('role code', max_length=64, unique=True, help_text='用户角色标识')
    # e.g 新增用户
    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=0, verbose_name='角色')
    permission = models.CharField(choices=Permission,default='VISITOR',max_length=50,verbose_name='权限')

    def __str__(self):
        return str(self.role)

    class Meta:
        db_table = 'role'


class UserRole(models.Model):
    """用户角色关系表"""
    user_id = models.IntegerField('user id', blank=False, help_text='用户id', unique=True)
    role_codes = models.CharField('role codes', blank=True, default=None, max_length=256, help_text='用户的角色codes')
    class Meta:
        db_table = 'user_role'

class RolePermission(models.Model):
    """角色权限关系表"""
    role_code = models.CharField('role code', max_length=64, blank=False, help_text='用户角色标识')
    pms_code = models.CharField('permission code', blank=False, max_length=64, help_text='权限code')

    class Meta:
        unique_together = ('role_code', 'pms_code')
        db_table = 'role_permission'

class UserTable(models.Model):
    GENDER_CHOICES = (
        (0, '男'),
        (1, '女')
    )
    user_id = models.AutoField(primary_key=True)
    name = models.CharField('姓名', default='', max_length=50)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    password = models.CharField('密码', default='123', max_length=50)
    phone = models.CharField('手机', default='', max_length=11)
    position = models.CharField('职位', default='', max_length=50)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('最后修改时间', auto_now=True)
    description = models.TextField('个人描述', null=True)
    user_role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'
