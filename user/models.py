from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with either an email or a phone number.
        """
        if not username:
            raise ValueError("The Email or Phone number field is required")

        if "@" in username:
            extra_fields["email"] = self.normalize_email(username)
            extra_fields["phone_number"] = None
        else:
            extra_fields["phone_number"] = username
            extra_fields["email"] = None

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not email:
            raise ValueError("Superuser must have an email or phone number")

        return self.create_user(username=email, password=password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # We will modify this in the backend for phone login
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email if self.email else self.phone_number
    
class PriestProfile(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='priest_profiles')
    # Priest-specific fields:
    profile = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    experience = models.IntegerField(blank=False, null=False)
    address = models.CharField(max_length=60, blank=False, null=False)
    # Add other priest-specific fields as needed

    def __str__(self):
        return f"PriestProfile for {self.user.email or self.user.phone_number}"
