from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Case)
admin.site.register(SiteUser)
admin.site.register(State)
admin.site.register(City)
admin.site.register(CourtOf)
admin.site.register(CaseType)
admin.site.register(CaseStage)
