
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save, pre_save


class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=255)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


def add_to_default_group(sender, instance, **kwargs):
    user = instance
    if kwargs["created"]:
        group = Group.objects.get(name='Staff')
        user.groups.add(group)


post_save.connect(add_to_default_group, sender=User)

# class UserRole(models.Model):
#     roles = models.CharField(blank=True, null=True,max_length=255)
#     def __unicode__(self):
#         return self.roles


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=255, blank=True)
    postaladdress = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=50, blank=True)
    subcounty = models.CharField(max_length=50, blank=True)
    constituency = models.CharField(max_length=50, blank=True)
    ward = models.CharField(max_length=50, blank=True)
    employee_gender = models.CharField(max_length=50, blank=True)
    employee_id_number = models.IntegerField(blank=True, null = True)
    photo = models.ImageField(upload_to='uploads', blank=True)

    def __str__(self):
        return self.name


def create_dummy_profile(sender, instance, ** kwargs):
    user_id = instance.id
    if kwargs["created"]:
        profile = UserProfile.objects.create(user=instance)
        profile.save()


post_save.connect(create_dummy_profile, sender=User)
