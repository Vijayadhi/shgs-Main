from django.contrib import admin
from django.contrib.auth.models import Group, User

from backend.models import Services, Blog

# Register your models here.
admin.site.register(Services)
admin.site.register(Blog)

admin.site.unregister(Group)
# admin.site.unregister(User)