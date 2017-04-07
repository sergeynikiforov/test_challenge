from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user manager
    """
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """
    objects = UserManager()

    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    is_admin = models.BooleanField(_('is administrator'), default=False)
    is_verified = models.BooleanField(_('is verified'), default=False)
    team = models.ForeignKey(
        'users.Team',
        verbose_name='team',
        related_name='members',
        related_query_name='member',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns self.first_name + self.last_name with space in between
        :return: str - full name
        """
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name).strip()

    def get_short_name(self):
        """
        Returns self.email
        :return: 
        """
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Team(models.Model):
    """
    Team model
    """
    name = models.CharField('Team name', max_length=256)

    def __str__(self):
        return self.name
