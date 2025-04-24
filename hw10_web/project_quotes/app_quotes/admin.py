from django.contrib import admin
from .models import Tag, Author, Quote

# Реєструємо моделі
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Quote)

# Register your models here.
