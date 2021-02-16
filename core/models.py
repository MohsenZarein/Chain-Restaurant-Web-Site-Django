from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.IntegerField(primary_key=True, unique=True)
    gender = models.CharField(max_length=10)
    province = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    street = models.CharField(max_length=225)
    alley = models.CharField(max_length=225)

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
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

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


class Branch(models.Model):
    branch_code = models.IntegerField(primary_key=True, unique=True)
    phone = models.CharField(max_length=50)
    personnel_count = models.IntegerField(default=0)
    province = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    street = models.CharField(max_length=225)
    alley = models.CharField(max_length=225)

    def __str__(self):
        return self.province + '-' + self.city
    
