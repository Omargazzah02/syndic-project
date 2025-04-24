from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from residences_app.models import Residence


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='owner')
    phone = models.CharField(max_length=30 , blank=True)

    residence = models.ForeignKey(
        Residence,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managers'
    )



    def clean(self):
        super().clean()
        if self.role != 'manager' and self.residence is not None:
            raise ValidationError("Seuls les utilisateurs avec le rôle 'manager' peuvent être liés à une résidence.")


    def save(self, *args, **kwargs):
        # Si l'utilisateur a un mot de passe non haché, on le hache ici
        self.full_clean()  # Appelle clean() automatiquement
        if self.password and not self.password.startswith('pbkdf2_'):
           self.password = make_password(self.password)

    

        if self.is_superuser and self.role != 'admin':
            self.role = 'admin'
            self.is_staff = True

        # Appel à la méthode save de la classe parente
        super().save(*args, **kwargs)

    def is_owner(self):
        return self.role in ['owner', 'manager', 'admin']

    def is_manager(self):
        return self.role in ['manager', 'admin']

    def is_admin(self):
        return self.role == 'admin'
