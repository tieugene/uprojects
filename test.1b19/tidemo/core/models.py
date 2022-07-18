import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_save
# from django.utils.translation import gettext_lazy as _

PTypeChoices = (
    (1, "Primary",),
    (2, "Secondary"),
    (3, "External"),
    (4, "Indirect"),
)


def validate_01(value):
    if value % 100 != 1:
        raise ValidationError("%(value)s must be ...01", params={'value': value},)


def validate_02(value):
    if value % 100 != 2:
        raise ValidationError("%(value)s must be ...02", params={'value': value},)


def validate_03(value):
    if value % 100 != 3:
        raise ValidationError("%(value)s must be ...03", params={'value': value},)


class Org(models.Model):
    myid = models.BigIntegerField(unique=True, null=True, blank=True, validators=(validate_02,), verbose_name="ID")
    name = models.CharField(max_length=40, unique=True, verbose_name="Name")
    fullname = models.CharField(max_length=255, null=True, blank=True, verbose_name="Full name")
    vat = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="VAT")  # 11 digits only for ru.org
    kpp = models.PositiveIntegerField(null=True, blank=True, verbose_name="KPP")  # 9 digits only (can be multiple)
    # auto:
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ('name',)
        indexes = (
            models.Index(fields=('myid',)),
            models.Index(fields=('name',)),
        )


class Depart(models.Model):
    myid = models.PositiveBigIntegerField(unique=True, null=True, blank=True, validators=(validate_03,),
                                          verbose_name="ID")
    name = models.CharField(max_length=32, verbose_name="Name")
    parent = models.ForeignKey('Depart', null=True, blank=True, on_delete=models.CASCADE)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    persons = models.ManyToManyField('Person', through='Membership', through_fields=('depart', 'person'))

    def __str__(self):
        return f"{self.org.name}.{self.name}"

    def person_qty(self):
        return self.persons.count()

    class Meta:
        verbose_name = "Deparment"
        verbose_name_plural = "Deparments"
        ordering = ('name', )
        unique_together = (('name', 'parent_id', 'org_id'),)
        indexes = (
            models.Index(fields=('myid',)),
            models.Index(fields=('name',)),
            models.Index(fields=('parent',)),
            models.Index(fields=('org',)),
        )


class Person(User):
    """
    User fields:
    username: not null, uniq
    password: not null
    first_name: not null
    last_name: not null
    email: not null
    is_active:bool
    date_joined:datetime(auto_now_add=True)
    """
    myid = models.PositiveBigIntegerField(unique=True, null=True, blank=True, validators=(validate_01,),
                                          verbose_name="ID")
    mid_name = models.CharField(max_length=32, null=True, blank=True, verbose_name="Middle name")
    phone = models.CharField(max_length=16, unique=True, null=True, blank=True, verbose_name="Main Phone")
    # ptype = models.ForeignKey(PType, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Type")
    ptype = models.PositiveSmallIntegerField(choices=PTypeChoices, null=True, blank=True,
                                             verbose_name="Type")
    sex = models.BooleanField(null=True, blank=True, verbose_name="Sex")
    tz = models.CharField(max_length=32, null=True, blank=True, verbose_name="Time zone")
    sn_ok = models.URLField(null=True, blank=True, verbose_name="OK profile URL")
    sn_ig = models.URLField(null=True, blank=True, verbose_name="Instagram profile URL")
    sn_tg = models.CharField(max_length=32, null=True, blank=True, verbose_name="Telegram account")
    sn_wa = models.CharField(max_length=32, null=True, blank=True, verbose_name="WhatsApp account")
    sn_vb = models.CharField(max_length=32, null=True, blank=True, verbose_name="Viber account")
    # auto:
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated")
    # semi-auto:
    statemod_at = models.DateTimeField(null=True, verbose_name="State updated")
    # m2m
    # departs = models.ManyToManyField(Depart, through='Membership', through_fields=('person', 'depart'))

    def __str__(self):
        return ' '.join((self.last_name, self.first_name))

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"
        ordering = ('last_name', 'first_name', 'mid_name',)
        indexes = (
            models.Index(fields=('myid',)),
            models.Index(fields=('mid_name',)),
        )


class Phone(models.Model):
    person = models.ForeignKey(Person, related_name='phone_set', on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, verbose_name="Phone")

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "Phone"
        verbose_name_plural = "Phones"
        ordering = ('phone',)


class EMail(models.Model):
    person = models.ForeignKey(Person, related_name='email_set', on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        ordering = ('email',)


class SnVK(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    url = models.URLField(verbose_name="Profile URL")

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "VK profile"
        verbose_name_plural = "VK profiles"
        ordering = ('url',)


class SnFB(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    url = models.URLField(verbose_name="Profile URL")

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "FB profile"
        verbose_name_plural = "FB profiles"
        ordering = ('url',)


class Membership(models.Model):
    depart = models.ForeignKey(Depart, on_delete=models.CASCADE, db_index=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, db_index=True)
    # auto:
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created")

    class Meta:
        unique_together = ('depart', 'person')


@receiver(pre_save, sender=Person)
def _person_pre_save(sender, instance, **_):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if not obj.ptype == instance.ptype:
            instance.statemod_at = datetime.datetime.now()
