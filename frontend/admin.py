from django.contrib import admin
from .models import Packages,agent,BlogPost

# Register your models here.
admin.site.register(Packages)
admin.site.register(agent)
admin.site.register(BlogPost)