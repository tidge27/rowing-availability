from django.db import models
from availability_site.models import CharNullField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import uuid

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    crsid = CharNullField(max_length=64, null=True, blank=True, unique=True, default=None)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    coach = models.BooleanField(default=False)
    is_bow = models.BooleanField(default=True)
    is_stroke = models.BooleanField(default=True)
    is_cox = models.BooleanField(default=False)
    # events = models.relationship("Event", backref="user", cascade="all, delete-orphan")
    # personal_outings = models.relationship("OutingMember", backref="user")
    # group_members = models.relationship("GroupMember", backref="user")

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '<User {}>'.format(self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

