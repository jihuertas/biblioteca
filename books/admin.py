from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin, register

from books.models import Libro, Autor, Editorial, Prestamo, Usuario


@register(Libro)
class BookAdmin(ModelAdmin):
    pass

admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Prestamo)
admin.site.register(Usuario)
