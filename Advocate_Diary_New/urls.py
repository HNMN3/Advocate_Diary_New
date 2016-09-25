"""Advocate_Diary_New URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from Advocate import views
from Advocate_Diary_New import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^date-cases/(?P<date>.+)/', views.home, name='date-cases'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^add-new-case/', views.add_new_case, name='add_new_case'),
    url(r'update-case/(.+)/', views.update_case, name='update-case'),
    url(r'fav-case/(.+)/', views.change_fav, name='fav-case'),
    url(r'archive-case/(.+)/', views.archive, name='archive-case'),
    url(r'restore-case/(.+)/', views.restore, name='restore-case'),
    url(r'archived-cases/', views.archived_cases, name='archived-cases'),
    url(r'starred-cases/', views.starred_cases, name='starred-cases'),
    url(r'all-cases/', views.all_cases, name='all-cases'),
    url(r'search-cases/', views.search_cases, name='search-cases'),
    url(r'calender/', views.calender, name='calender-current'),
    url(r'contact-us/', TemplateView.as_view(template_name='Advocate/contact-us.html'), name='contact-us'),

]

