from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户名")
    email = models.EmailField(max_length=32,verbose_name="邮箱",null=True,blank=True)
    ug = models.ForeignKey("Group",null=True,blank=True,verbose_name="职位")
    u2r = models.ManyToManyField("Role",verbose_name="角色")

    def text_username(self):
        return self.username

    def value_username(self):
        return self.username

    def text_email(self):
        return self.email

    def value_email(self):
        return self.email

    def __str__(self):
        return self.username

class Role(models.Model):
    name = models.CharField(max_length=32,verbose_name="角色")

    def __str__(self):
        return self.name

class Group(models.Model):
    title = models.CharField(max_length=32,verbose_name="用户组")

    def __str__(self):
        return self.title