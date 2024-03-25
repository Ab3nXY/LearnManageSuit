from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from guardian.shortcuts import get_perms_for_model



class UserManager(BaseUserManager):
    """ User manager """

    def _create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        if not email:  # check for an empty email
            raise AttributeError("User must set an email address")
        else:  # normalizes the provided email
            email = self.normalize_email(email)

        # create user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes/encrypts password
        user.save(using=self._db)  # safe for multiple databases
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", "Student")
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password=None, **extra_fields):
        """Creates and returns a new staffuser using an email address"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a new superuser using an email address"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)
    
    def create_student(self, email, password=None, **extra_fields):
        """Creates and returns a new student user using an email address"""
        extra_fields.setdefault("role", "Student")
        return self._create_user(email, password, **extra_fields)

    def create_tutor(self, email, password=None, **extra_fields):
        """Creates and returns a new tutor user using an email address"""
        extra_fields.setdefault("role", "Tutor")
        return self._create_user(email, password, **extra_fields)

    def create_guidance(self, email, password=None, **extra_fields):
        """Creates and returns a new guidance user using an email address"""
        extra_fields.setdefault("role", "Guidance")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model """

    email = models.EmailField(
        _("Email Address"),
        max_length=150,
        unique=True,
    )
    is_staff = models.BooleanField(_("Staff status"), default=False)
    is_active = models.BooleanField(_("Active"), default=True)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True)
    first_name = models.CharField(_("First Name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=150, blank=True)

    # Add a field for user role
    ROLE_CHOICES = (
        ("student", "Student"),
        ("tutor", "Tutor"),
        ("guidance", "Guidance"),
        ("admin", "Admin"),
    )
    role = models.CharField(_("Role"), max_length=20, choices=ROLE_CHOICES, default="student")

    # Override has_perm method to check custom permissions based on user role
    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return self.user_permissions.filter(codename=perm).exists()

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True
        return any(self.has_perm(perm) for perm in get_perms_for_model(ContentType.objects.get(app_label=app_label)))

    # Override get_group_permissions method to include custom permissions based on user role
    def get_group_permissions(self, obj=None):
        perms = super().get_group_permissions(obj=obj)
        if self.role == "admin":
            perms |= Permission.objects.filter(content_type__app_label='accounts')
        return perms

    # Override get_all_permissions method to include custom permissions based on user role
    def get_all_permissions(self, obj=None):
        return {
            perm for perm in self.get_group_permissions(obj=obj)
        }

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default = "profile_pics/default.jpg", upload_to='profile_pics')
    border_color = models.CharField(max_length=20, default='#000000')


    def __str__(self):
        return f'{self.user.first_name} Profile' #show how we want it to be displayed