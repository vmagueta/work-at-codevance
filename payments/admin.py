from django.contrib import admin

from .models import Antecipation, Payment, Vendor

admin.site.register(Vendor)
admin.site.register(Payment)
admin.site.register(Antecipation)
