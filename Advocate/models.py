from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models


# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SiteUser(models.Model):
    company_name = models.CharField(max_length=250)
    company_logo = models.ImageField(upload_to='company_logo/', blank=True, null=True)
    full_name = models.CharField(max_length=500)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    state = models.ForeignKey(State)
    city = models.ForeignKey(City)
    email = models.CharField(max_length=254)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class CourtOf(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class CaseType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class CaseStage(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


# u = SiteUser.objects.get(user__email='denanath.vijay1991@gmail.com')


class Case(models.Model):
    advocate = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    title = models.CharField(max_length=150)
    case_no = models.CharField(max_length=100, unique=True)
    court_of = models.ForeignKey(CourtOf, on_delete=models.CASCADE)
    case_type = models.ForeignKey(CaseType, on_delete=models.CASCADE)
    case_stage = models.ForeignKey(CaseStage, on_delete=models.CASCADE)
    filling_date = models.DateField()
    party_name = models.CharField(max_length=100)
    appearing_lawyer = models.CharField(max_length=500)
    opposite_lawyer = models.CharField(max_length=500, blank=True)
    fees = models.FloatField(default=0.00, blank=True)
    remarks = models.TextField(blank=True)
    prev_date = models.DateField()
    next_date = models.DateField(blank=True, null=True)
    fav = models.BooleanField(default=False, blank=True, editable=False)
    archived = models.BooleanField(default=False, blank=True, editable=False)
    confirmation = models.CharField(max_length=10, choices=((0, 'Canceled'), (1, 'Pending'), (2, 'Confirmed')),
                                    default='Pending', editable=False)

    def __str__(self):
        return self.title


NEW_USERNAME_LENGTH = 254

