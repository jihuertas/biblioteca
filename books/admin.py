from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin, register

from books.models import Libro, Autor, Editorial


@register(Libro)
class BookAdmin(ModelAdmin):
    pass

admin.site.register(Autor)
admin.site.register(Editorial)
