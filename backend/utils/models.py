from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from safedelete.models import SafeDeleteModel
from safedelete.managers import SafeDeleteManager


class UserManager(BaseUserManager, SafeDeleteManager):
    def create_user(self, email, password=None, name=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Name field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, SafeDeleteModel):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_id_create = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name="%(class)s_created_by",
        null=True,
        default=None
    )
    user_id_update = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name="%(class)s_updated_by",
        null=True,
        default=None
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)


class BaseFullModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id_create = models.ForeignKey(User, on_delete=models.PROTECT, related_name="%(class)s_created_by")
    user_id_update = models.ForeignKey(User, on_delete=models.PROTECT, related_name="%(class)s_updated_by")

    class Meta:
        abstract = True  # This means that Django will not create a database table for the abstract model itself.


class BaseCreatedByModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_id_create = models.ForeignKey(User, on_delete=models.PROTECT, related_name="%(class)s_created_by")

    class Meta:
        abstract = True


class BaseCreatedAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
