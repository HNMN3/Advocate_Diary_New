import datetime
import random
import re
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count
from django.db.models.sql import Query
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import time
from .forms import *


# Create your views here.
@login_required
def home(request, date=None):
    if date is None:
        date = datetime.datetime.today()
        month = date.month
        day = date.day
        year = date.year
        # date = str(date.day) + '/' + str(date.month) + '/' + str(date.year)
    else:
        year, month, day = date.strip().split('-')
        date = datetime.datetime.strptime(str(day) + ' ' + str(month) + ' ' + str(year), '%d %m %Y')
    one = datetime.timedelta(days=1)
    adv = SiteUser.objects.get(user=request.user)
    data = Case.objects.filter(advocate=adv, next_date__day=day, next_date__month=month, next_date__year=year,
                               archived=False).order_by('title')
    return render(request, 'Advocate/case-list.html',
                  {'heading': 'Home', 'date': date, 'prev_date': (date - one).date(), 'next_date': (date + one).date(),
                   'today': date.date(), 'cases': data})


def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            del (form.cleaned_data['agree'])
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            city = City.objects.get(name=city)
            try:
                User.objects.get(username=form.cleaned_data['email'])
                return HttpResponse('User already exist')
            except User.DoesNotExist:
                pass
            form.cleaned_data['email'] = re.match('(.+)@.*\..*', form.cleaned_data['email']).groups()[0]
            try:
                if len(form.cleaned_data['email']) > 30:
                    raise Exception
            except Exception:
                return render(request, 'Advocate/signup.html',
                              {'form': form, 'states': State.objects.all(), 'email_length': 1})

            auth_user = User.objects.create(username=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            auth_user.set_password(form.cleaned_data['password'])
            auth_user.save()
            del (form.cleaned_data['state'])
            del (form.cleaned_data['city'])
            del (form.cleaned_data['email'])
            del (form.cleaned_data['password'])

            user = SiteUser(**form.cleaned_data)
            user.city = city
            user.state = state
            user.user = auth_user
            user.save()

            return redirect('/login/')
    else:
        form = RegistrationForm()

    return render(request, 'Advocate/signup.html', {'form': form,
                                                    'states': State.objects.all()})


def login(request):
    wrong = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        user = authenticate(username=re.match('(.+)@.*\..*', request.POST['email']).groups()[0],
                            password=request.POST['password'])
        print(request.POST)
        if user is not None:
            auth_login(request, user)
            return redirect(home)
        else:
            wrong = True
    else:
        form = LoginForm()

    return render(request, 'Advocate/login.html',
                  {'header_title': 'A Diary For Advocates', 'form': form, 'wrong': wrong})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('/login/')


@login_required
def add_new_case(request):
    if request.method == "POST":
        form = CaseForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['next_date'] is None:
                form.cleaned_data['next_date'] = form.cleaned_data['filling_date']
            form.save()
            c = Case.objects.get(case_no=form.cleaned_data['case_no'])
            c.advocate = SiteUser.objects.get(user=request.user)
            c.save()
            return redirect(home, date=form.cleaned_data['next_date'])
    else:
        form = CaseForm()

    return render(request, 'Advocate/add-new-case.html',
                  {'page_heading': 'Add New Case', 'form': form, 'button_value': 'Add Case'})


@login_required
def update_case(request, case_no):
    case = get_object_or_404(Case, case_no=case_no)

    if request.method == 'POST':
        form = CaseForm(request.POST or None, instance=case)
        print(form)
        if form.is_valid():
            form.save()
            return redirect(home, date=form.cleaned_data['next_date'])
    else:
        form = CaseForm(instance=case)

    return render(request, 'Advocate/add-new-case.html',
                  {'page_heading': 'Update Case', 'form': form, 'button_value': 'Update Case', 'update_case': 1,
                   'case_no': case_no})


@login_required
def change_fav(request, case_no):
    case = get_object_or_404(Case, case_no=case_no)
    case.fav = not case.fav
    case.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def archive(request, case_no):
    case = get_object_or_404(Case, case_no=case_no)
    case.archived = True
    case.fav = False
    case.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def restore(request, case_no):
    case = get_object_or_404(Case, case_no=case_no)
    case.archived = False
    case.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def starred_cases(request):
    adv = SiteUser.objects.get(user=request.user)
    data = Case.objects.filter(fav=True, advocate=adv).order_by('next_date')
    return render(request, 'Advocate/case-list.html', {'cases': data, 'heading': 'Starred Cases'})


@login_required
def archived_cases(request):
    adv = SiteUser.objects.get(user=request.user)
    data = Case.objects.filter(archived=True, advocate=adv).order_by('-next_date')
    return render(request, 'Advocate/case-list.html', {'cases': data, 'heading': 'Archived Cases', 'restore': 1})


@login_required
def all_cases(request):
    adv = SiteUser.objects.get(user=request.user)
    data = Case.objects.filter(archived=False, advocate=adv).order_by('next_date')
    return render(request, 'Advocate/case-list.html', {'cases': data, 'heading': 'All Cases'})


@login_required
def search_cases(request):
    data = None
    if request.method == "POST":
        form = SearchCaseForm(request.POST)
        if form.is_valid():
            attr = dict(filter(lambda x: form.cleaned_data[x[0]], form.cleaned_data.items()))
            adv = SiteUser.objects.get(user=request.user)
            data = Case.objects.filter(advocate=adv, **attr)
            return render(request, 'Advocate/case-list.html',
                          {'cases': data, 'heading': 'Search Result', 'search': 1})
    else:
        form = SearchCaseForm()

    return render(request, 'Advocate/search-case.html', {'form': form})


@login_required
def calender(request, month=None):
    adv = SiteUser.objects.get(user=request.user)
    data = Case.objects.filter(archived=False, advocate=adv)

    return render(request, 'Advocate/calender.html', {'data': data, 'rows': range(6), 'columns': range(7),
                                                      'days': ["Sunday", "Monday", "Tuesday", "Wednesday",
                                                               "Thursday",
                                                               "Friday", "Saturday"]})
