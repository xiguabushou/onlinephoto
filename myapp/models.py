from django.db import models
from datetime import datetime

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80)
    photoname = models.CharField(max_length=40)
    addtime = models.DateTimeField(default=datetime.now)

class CustomUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # 通常不会直接存储明文密码
    # 你可以添加其他字段，如 email, first_name, last_name 等

    def __str__(self):
        return self.username

