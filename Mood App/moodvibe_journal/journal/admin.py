# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Songs, Quotes, Journal

admin.site.register(Songs)
admin.site.register(Quotes)
admin.site.register(Journal)
