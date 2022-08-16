from django.contrib import admin

from app.models import Subscriber

class SubscriberAdmin(admin.ModelAdmin):
    ordering = ['email']
    search_fields = ['email']


# Register your models here.
admin.site.register(Subscriber, SubscriberAdmin)