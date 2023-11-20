from django import forms

from books.models import Libro


class BookForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('titulo', 'autores', 'editorial', 'rating', 'fecha_publicacion','genero', 'ISBN', 'resumen','portada')

