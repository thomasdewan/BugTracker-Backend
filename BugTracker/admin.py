from django.contrib import admin
from .models import Issue,Comment,State

admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(State)
