from django.contrib import admin
from .models import Users, Project, Management

# Register your models here.

admin.site.register(Users)
admin.site.register(Project)
admin.site.register(Management)