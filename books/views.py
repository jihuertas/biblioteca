from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
# Create your views here.

from books.forms import BookForm
from books.models import Libro


# class ListBookView(View):
#     def get(self, request):
#         return render(request, 'books/list_book.html', context={'books': Book.objects.all().order_by('-created_at')})
# class DetailBookViewAnt(View):
#     def get(self, request):
#         return render(request, 'books/list_book.html', context={'books': Book.objects.all().order_by('-created_at')})

class ListBookView(ListView):
    model = Libro

class DetailBookView(DetailView):
    model = Libro
    #template_name = 'books/book_detail.html'

class UpdateBookView(UpdateView):
    model= Libro
    fields = ['titulo', 'autores', 'editorial', 'rating', 'fecha_publicacion','genero', 'ISBN', 'resumen','portada']
    template_name="books/libro_update.html"
    success_url = reverse_lazy("list-book")
    
class DeleteBookView(DeleteView):
    model= Libro
    #fields = ['title', 'author', 'rating']
    success_url = reverse_lazy("list-book")

class CreateBookView(View):
    def get(self, request):
        return render(request, 'books/libro_create.html',
                      context={'forms': formset_factory(BookForm, extra=3)})

    def post(self, request):
        formset = formset_factory(BookForm)
        formset = formset(data=request.POST)

        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    form.save()
            return redirect(to='list-book')

        else:
            return render(request, 'books/libro_create.html',
                          context={'forms': formset})
