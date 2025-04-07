from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='owner')


    def save(self, *args, **kwargs):
        if self.is_superuser and self.role != 'admin':
            self.role = 'admin'
            self.is_staff = True

     
        super().save(*args, **kwargs)

    def is_owner(self):
        return self.role in ['owner','manager', 'admin'] # cette role est accesible a owner, manager, admin 

    def is_manager(self):
        return self.role in ['manager', 'admin'] #cette role est accesible a manager, admin

    def is_admin(self):
        return self.role == 'admin' #cette role est accesible uniquement a admin 