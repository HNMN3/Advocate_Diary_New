# Keep coding and change the world..And do not forget anything..Not Again..
from .models import *
from django import forms
from django.db.models import Model
from functools import partial
from django.contrib.admin import widgets as admin_widget


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for bound_field in self:
            if hasattr(bound_field, "field") and bound_field.field.required:
                bound_field.field.widget.attrs["required"] = "required"


class RegistrationForm(forms.Form):
    company_name = forms.CharField(max_length=250, label='Company Name',
                                   widget=forms.TextInput(attrs={'required': 'required', 'class': 'auth-box-item'}))
    company_logo = forms.ImageField(required=False, label='Company Logo',
                                    widget=forms.FileInput(attrs={'class': 'auth-box-item'}))
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '6', 'cols': '82', 'required': 'required', 'class': 'auth-box-item'}))
    state = forms.ModelChoiceField(State.objects.all(), 'Select State..',
                                   widget=forms.Select(
                                       attrs={'required': 'required', 'class': 'auth-box-item',
                                              'onchange': 'changeCities()'}))
    city = forms.ModelChoiceField(City.objects.all(), 'Select City..',
                                  widget=forms.Select(attrs={'required': 'required', 'class': 'auth-box-item'}))
    full_name = forms.CharField(max_length=500,
                                widget=forms.TextInput(attrs={'required': 'required', 'class': 'auth-box-item'}))
    email = forms.EmailField(max_length=100,
                             widget=forms.EmailInput(attrs={'required': 'required', 'class': 'auth-box-item'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'required', 'class': 'auth-box-item'}))
    phone = forms.CharField(max_length=15,
                            widget=forms.TextInput(
                                attrs={'pattern': '[0-9]{10}', 'required': 'required', 'class': 'auth-box-item'}))
    agree = forms.BooleanField(label='I/we agree to Terms of Use.',
                               widget=forms.CheckboxInput(attrs={'required': 'required'}))


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100,
                             widget=forms.EmailInput(attrs={'required': 'required', 'class': 'auth-box-item'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'required', 'class': 'auth-box-item'}))


class CaseForm(BaseForm):
    class Meta:
        model = Case
        fields = '__all__'
        widgets = {'filling_date': forms.TextInput(attrs={'type': 'date'}),
                   'prev_date': forms.TextInput(attrs={'type': 'date'}),
                   'next_date': forms.TextInput(attrs={'type': 'date'})
                   }


class SearchCaseForm(forms.Form):
    case_no = forms.CharField(max_length=100, required=False)
    party_name = forms.CharField(max_length=100, required=False)
    title = forms.CharField(max_length=100, required=False)
    court_of = forms.ModelChoiceField(CourtOf.objects.all(), '--Select--', required=False)
    case_type = forms.ModelChoiceField(CaseType.objects.all(), '--Select--', required=False)
    case_stage = forms.ModelChoiceField(CaseStage.objects.all(), '--Select--', required=False)
