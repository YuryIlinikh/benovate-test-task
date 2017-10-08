from decimal import Decimal
from random import randint

from django.contrib.auth.models import User
from django.core.validators import int_list_validator
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch.dispatcher import receiver


class Inn(models.Model):
    inn = models.CharField(max_length=12, unique=True,
                           validators=[int_list_validator(sep='', message=None, code='invalid', allow_negative=False)])

    def __str__(self):
        return str(self.inn)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bill = models.DecimalField(max_digits=19, decimal_places=2, default=Decimal('0.00'))
    inn = models.ForeignKey(Inn, null=True, blank=True)

    def __str__(self):
        return "User: {}, Bill: {}, INN: {}".format(self.user.username, self.bill, self.inn)

#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Transfer:
    def __init__(self, from_user_id: int, to_inn: str, amount: Decimal):
        self.from_user_id = from_user_id
        self.to_inn = to_inn
        self.amount = amount

    def load_from_profile(self):
        return Profile.objects.select_related('user').get(user_id__exact=self.from_user_id)

    def load_inn_profiles(self):
        return Profile.objects.filter(inn__inn__exact=self.to_inn).select_related('user')

    def save(self, from_profile, inn_profiles):
        for inn_profile in inn_profiles:
            inn_profile.save()
        from_profile.save()
