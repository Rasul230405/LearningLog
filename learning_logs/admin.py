from django.contrib import admin

from .models import Topic, Entry, Comment

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Comment)