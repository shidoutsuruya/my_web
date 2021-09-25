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
            'create_at':self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            'update_at':self.update_at.strftime("%Y-%m-%d %H:%M:%S"),
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
            'id':self.id,
            'shop_id':self.shop_id,
            'name':self.name,
            'status':self.status,
            'create_at':self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            'update_at':self.update_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return dictionary
    class Meta:
        db_table='category'
    
class Product(models.Model):
    shop_id=models.IntegerField()
    category_id=models.IntegerField()
    cover_pic=models.CharField(max_length=50)
    name=models.TextField()
    price=models.DecimalField(max_digits=8,decimal_places=2)
    status=models.IntegerField()
    create_at=models.DateTimeField()
    update_at=models.DateTimeField()
    def to_dict(self):
        dictionary={
            'id':self.id,
            'shop_id':self.shop_id,
            'category_id':self.category_id,
            'cover_pic':self.cover_pic,
            'name':self.name,
            'price':self.price,
            'status':self.status,
            'create_at':self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            'update_at':self.update_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return dictionary
    class Meta:
        db_table='product'
class Orders(models.Model):
    shop_id=models.IntegerField()
    member_id=models.IntegerField()
    user_id=models.IntegerField()
    money=models.FloatField()
    status=models.IntegerField(default=1)
    payment_status=models.IntegerField(default=1)
    create_at=models.DateTimeField()
    update_at=models.DateTimeField()
    class Meta:
        db_table='orders'
class OrderDetail(models.Model):
    order_id=models.IntegerField()
    product_id=models.IntegerField()
    product_name=models.CharField(max_length=50)
    price=models.FloatField()
    quantity=models.IntegerField()
    status=models.IntegerField(default=1)
    class Meta:
        db_table='order_detail'
class Payment(models.Model):
    order_id=models.IntegerField()
    member_id=models.IntegerField()
    money=models.FloatField()
    type=models.IntegerField()
    bank=models.IntegerField(default=1)
    status=models.IntegerField(default=1)
    create_at=models.DateTimeField(default=datetime.now)
    update_at=models.DateTimeField(default=datetime.now)
    class Meta:
        db_table='payment'
    