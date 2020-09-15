from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, username, email_address, password, **extra_fields):

        now  = timezone.localtime(timezone.now())

        if not email_address and not username:
            raise ValueError("A username or email is required to create an account")

        email_address = self.normalize_email(email_address)
        username = self.model.normalize_username(username)

        user = self.model(username=username, email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email_address, password=None, **extra_fields):

        return self._create_user(username, email_address, password, **extra_fields)

    def create_superuser(self, username, email_address, password, **extra_fields):
        email_address = self.normalize_email(email_address)
        username = self.model.normalize_username(username)
        
        return self._create_user(username, email_address, password, **extra_fields)

class AccountType(models.Model):
    account_type = models.CharField(
        unique=True,
        max_length=20,
    )

    def __str__(self):
        return "%s" % (self.account_type)


class CustomUser(AbstractBaseUser): 
    username = models.CharField(
        unique=True,
        max_length=20,
    )
    email_address = models.EmailField(
        verbose_name='email address',
        max_length=50,
        unique=True,
    )
    account_type = models.ForeignKey(
        AccountType,
        on_delete=models.CASCADE,
        related_name="user_account_type",
        null = True,
    )
    is_active = models.BooleanField(
        default=True
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email_address",]
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email_address])

    def __str__(self):
        if not self.username:
             return "%s" % (self.email_address)
        else:
            return "%s" % (self.username)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
       return True
    
    
    def getPosition(self):
        committees = self.committees.filter(isDeleted=False)

        if committees.first():
            return committees.first().position.id

        elif self.account_type.id == 1:
            return 'ADMIN'
        return ''

    @property
    def is_staff(self):
        return True

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class UserProfile(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    name = models.CharField(
        max_length=255,
    )
    age = models.IntegerField(
        blank = True,
        null = True,
        default = 0,
    )
    birthdate = models.DateField(
        blank = True,
        null = True,
    )
    birthplace = models.CharField(
        blank = True,
        null = True,
        max_length=255,
    )
    gender = models.ForeignKey(
        'settings.GenderType',
        on_delete=models.CASCADE,
        related_name="gender_user",
        blank = True,
        null = True,
    )
    profile_picture = models.FileField(
        null = True,
        blank=True,
        upload_to=user_directory_path
    )
    digital_signature = models.ImageField(
        blank=True,
        null = True,
        upload_to=user_directory_path
    )

    def __str__(self):
        return "%s - %s" % (self.user, self.name)

class UserApps(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="appAccess"
    )
    installedApps = models.ManyToManyField(
        'settings.AppName',
        blank=True
    )

    def __str__(self):
        return "%s - %s" % (self.user, self.installedApps)


class UserLogs(models.Model):
    action_time = models.DateTimeField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="userLogs"
    )
    action_type = models.CharField(
        max_length=255,
        blank=True,
        null = True,
    )
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        related_name="account_content_type",
        blank=True,
        null = True,
    )
    object_id = models.PositiveIntegerField(
        blank=True,
        null = True,
    )
    content_object = GenericForeignKey(
        'content_type', 
        'object_id',
    )
    object_type = models.CharField(
        max_length=255,
        blank=True,
        null = True,
    )
    apiLink = models.CharField(
        max_length=255,
        blank=True,
        null = True,
    )
    valueToDisplay = models.CharField(
        max_length=255,
        blank=True,
        null = True,
    )

    def __str__(self):
        return "%s - %s %s %s" % (self.user,self.action_type, self.content_type, self.object_id)

class LogDetails(models.Model):
    logDetails = models.ForeignKey(
        UserLogs,
        on_delete=models.CASCADE,
        related_name="logDetails"
    )
    action = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return "%s - %s" % (self.logDetails,self.action)