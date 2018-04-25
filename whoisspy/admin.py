from django.contrib import admin
from .models import Category, Group, Phrase, UserProfile

admin.site.register(Category)
admin.site.register(Group)
admin.site.register(Phrase)
admin.site.register(UserProfile)