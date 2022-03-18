from django.db import models
from django.contrib.auth.models import User

Permission = (
    ('VISITOR','General Users'),
    ('UPDATE','Modify Permission'),
    # Permission to delete
    ('DELETE', 'Delete Users'),
    # Perimssion to add
    ('ADD', 'Add Users'),
    # Administrator's permission, add, delete, modify and check
    ('ADMIN', 'Administrator Permission')
)


class Role(models.Model):
    ROLE_CHOICES = (
        (0, 'Doctor'),
        (1, 'Nurse'),
        (2, 'Nurse Manager')
    )
    role_code = models.CharField('role code', max_length=64, unique=True, help_text='User role identification')
    # e.g Add user
    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=0, verbose_name='Role')
    permission = models.CharField(choices=Permission,default='VISITOR',max_length=50,verbose_name='Permission')

    def __str__(self):
        return str(self.role)

    class Meta:
        db_table = 'role'


class UserRole(models.Model):
    """User Role Relationship Table"""
    user_id = models.IntegerField('user id', blank=False, help_text='User id', unique=True)
    role_codes = models.CharField('role codes', blank=True, default=None, max_length=256, help_text='User role codes')
    class Meta:
        db_table = 'user_role'

class RolePermission(models.Model):
    """Role Permission Relationship Table"""
    role_code = models.CharField('role code', max_length=64, blank=False, help_text='User role identification')
    pms_code = models.CharField('permission code', blank=False, max_length=64, help_text='Permission code')

    class Meta:
        unique_together = ('role_code', 'pms_code')
        db_table = 'role_permission'

class UserTable(models.Model):
    GENDER_CHOICES = (
        (0, 'Male'),
        (1, 'Famle')
    )
    user_id = models.AutoField(primary_key=True)
    name = models.CharField('Name', default='', max_length=50)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='Gender')
    password = models.CharField('Password', default='123', max_length=50)
    phone = models.CharField('Phone', default='', max_length=11)
    position = models.CharField('Position', default='', max_length=50)
    create_time = models.DateTimeField('Creation time', auto_now_add=True)
    modify_time = models.DateTimeField('Last modified time', auto_now=True)
    description = models.TextField('Description', null=True)
    user_role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'
