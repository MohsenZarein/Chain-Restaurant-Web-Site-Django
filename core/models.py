from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os
from uuid import uuid4
from datetime import datetime


def branch_image_upload_path_handler(instance, filename):
    """ Generate file path for new branch image """
    extension = filename.split('.')[-1]
    filename = f'{uuid4()}.{extension}'
    return os.path.join('branches/', filename)


def food_image_upload_path_handler(instance, filename):
    """ Generate file path for new branch image """
    extension = filename.split('.')[-1]
    filename = f'{uuid4()}.{extension}'
    return os.path.join('foods/', filename)
    


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Create and saves a new user """
        if not email:
            raise ValueError('Users must have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    

    def create_superuser(self, email, password):
        """ create and save a new superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username """
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'



class Branch(models.Model):
    branch_code = models.IntegerField(primary_key=True, unique=True)
    phone = models.CharField(max_length=50)
    personnel_count = models.IntegerField(default=0)
    province = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    street = models.CharField(max_length=225)
    alley = models.CharField(max_length=225)
    image = models.ImageField(null=True, blank=False, upload_to=branch_image_upload_path_handler)

    def __str__(self):
        return self.province + '-' + self.city


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.IntegerField(primary_key=True, unique=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    province = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225 ,null=True, blank=True)
    street = models.CharField(max_length=225, null=True, blank=True)
    alley = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.user.email





class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personnel_code = models.IntegerField(primary_key=True, unique=True)
    gender = models.CharField(max_length=10)
    province = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    street = models.CharField(max_length=225)
    alley = models.CharField(max_length=225)
    birth_date = models.DateField()
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    last_service = models.DateTimeField(default=datetime.now , blank=True)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.email
       

class CustomerPhoneNo(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    
    def __str__(self):
        return self.phone
    


class PersonnelPhoneNo(models.Model):
    personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.phone






class Food(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    BREAKFASTS = 'breakfasts'
    PIZZAS = 'pizzas'
    BURGERS = 'burgers'
    SEAFOODS = 'seafoods'
    STARTERS = 'starters'
    SALADS = 'salads'
    KEBABS = 'kebabs'
    GIPPOS = 'gippos'
    TRADITIONALS = 'traditionals'
    FOOD_CATEGORIES = [
        (BREAKFASTS, 'breakfasts'),
        (PIZZAS, 'pizzas'),
        (BURGERS, 'burgers'),
        (SEAFOODS, 'seafoods'),
        (STARTERS, 'starters'),
        (SALADS, 'salads'),
        (KEBABS, 'kebabs'),
        (GIPPOS, 'gippos'),
        (TRADITIONALS, 'traditionals'),
    ]
    category = models.CharField(max_length=30, choices=FOOD_CATEGORIES, default=BREAKFASTS)
    image = models.ImageField(null=True, blank=False, upload_to=food_image_upload_path_handler)


    def __str__(self):
        return self.name



class Table(models.Model):
    is_empty = models.BooleanField(default=True)
    is_reserved = models.BooleanField(default=False)
    capacity = models.IntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)



class OnlineOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    deliverer = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    pay_code = models.CharField(max_length=255, blank=True, null=False, default='0')
    count = models.IntegerField()
    destination_address = models.TextField(max_length=500, null=True, blank=True)
    NOT_DELIVERED = 'not_delivered'
    IS_DELIVERING = 'is_delivering'
    DELIVERED = 'delivered'
    STATUS = [
        (NOT_DELIVERED, 'not_delivered'),
        (IS_DELIVERING, 'is_delivering'),
        (DELIVERED, 'delivered')
    ]
    delivery_status = models.CharField(max_length=15, choices=STATUS, default=NOT_DELIVERED)


    def __str__(self):
        return self.pay_code



    
    
