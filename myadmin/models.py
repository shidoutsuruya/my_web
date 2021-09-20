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
    def to_dict(self):
        return {
            'id':self.id,'username':self.username,
                'password_hash':self.password_hash,
                'password_salt':self.password_salt,
                'status':self.status,
                'create_at':self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
                'update_at':self.update_at.strftime("%Y-%m-%d %H:%M:%S")
                }
    class Meta:
        db_table='user'
        
class Shop(models.Model):
    name=models.CharField(max_length=255)
    cover_pic=models.CharField(max_length=255)
    banner_pic=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    status=models.IntegerField(1)
    create_at=models.DateTimeField()
    update_at=models.DateTimeField()
    def to_dict(self):
        shopname=self.name.split('-')
        return {
            'id':self.id,
            'name':shopname[0],
            'shop':shopname[1],
            'cover_pic':self.cover_pic,
            'banner_pic':self.banner_pic,
            'address':self.address,
            'phone':self.phone,
            'status':self.status,
            'create_at':self.create_at,
            'update_at':self.update_at,
        }
    class Meta:
        db_table='shop'
    
class Category(models.Model):
    shop_id=models.IntegerField()
    name=models.CharField(max_length=50)
    status=models.IntegerField()
    create_at=models.DateTimeField()
    update_at=models.DateTimeField()
    def to_dict(self):
        dictionary={
            'shop_id':self.shop_id,
            'name':self.name,
            'status':self.status,
            'create_at':self.create_at,
            'update_at':self.update_at
        }
        return dictionary
    class Meta:
        db_table='category'
    
class product(models.Model):
    shop_id=models.IntegerField()
    category_id=models.IntegerField()
    cover_pic=models.CharField(max_length=50)
    name=models.TextField()
    price=models.DecimalField(max_digits=8,decimal_places=2)
    status=models.IntegerField()
    create_time=models.DateTimeField()
    update_time=models.DateTimeField()
    def to_dict(self):
        dictionary={
            'shop_id':self.shop_id,
            'category_id':self.category_id,
            'cover_pic':self.cover_pic,
            'name':self.name,
            'price':self.price,
            'status':self.status,
            'create_time':self.create_time,
            'update_time':self.update_time
        }
        return dictionary
    class Meta:
        db_table='product'