from django.contrib import admin

from app.models import Notice, Subscriber

class SubscriberAdmin(admin.ModelAdmin):
  ordering = ['email']
  search_fields = ['email']


class NoticeAdmin(admin.ModelAdmin):
  ordering = ['-date']
  list_display = ['date']

# Register your models here.
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Notice, NoticeAdmin)