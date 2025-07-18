from uuid import uuid4
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from core.app.user.domain.entities import User as UserEntity

# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        fields = kwargs.copy()
        fields.setdefault("is_staff", False)
        return self._create_user(email, password, **fields)

    def create_superuser(self, email, password=None, **kwargs):
        fields = kwargs.copy()
        fields.setdefault("is_staff", True)
        return self.create_user(email, password, **fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom authentication model"""
    USER_ROLES = [("administrative", _("Administrator"))]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the authentication can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this authentication should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def to_entity(self) -> UserEntity:
        user = UserEntity(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            is_active=self.is_active,
            date_joined=self.date_joined
        )   

        return user

    @staticmethod
    def from_entity(entity: UserEntity) -> "User":
        return User(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            is_active=entity.is_active,
            date_joined=entity.date_joined
        )