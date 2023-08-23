'''decide what models get registered to the admin page to ultimatly get saved to postgresql database'''

from django.contrib import admin
from .models import config

admin.site.register(config)