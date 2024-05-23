from django.contrib import admin
from .models import Favorite, UserTelegram


admin.site.register([Favorite, UserTelegram])