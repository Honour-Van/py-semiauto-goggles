from datetime import date, datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Counters(models.Model):
    id = models.AutoField
    count = models.IntegerField(max_length=11, default=0)
    createdAt = models.DateTimeField(default=datetime.now(), )
    updatedAt = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Counters'  # 数据库表名


class Position(models.Model):
    id = models.AutoField
    latitude = models.DecimalField(max_length=7, decimal_places=5, max_digits=12, default=0)
    longitude = models.DecimalField(max_length=8, decimal_places=5, max_digits=13, default=0) # 考虑到北京的经度在116左右，所以多一位
    # date = models.DateField(default=timezone.now)
    timestamp = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Position'