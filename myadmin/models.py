from django.db import models
from datetime import datetime
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=100)
    password_salt=models.CharField(max_length=50)
    status=models.IntegerField(default=1)
    create_at=models.DateTimeField(default=datetime.now())
    update_at=models.DateTimeField(default=datetime.now())
    class Meta:
        db_table='user'