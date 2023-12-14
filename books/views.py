from typing import Any
from django.db.models.query import QuerySet
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from datetime import date, timedelta
from books.forms import BookForm
from books.models import Libro, Prestamo
# Create your views here.

# class ListBookView(View):
#     def get(self, request):
#         return render(request, 'books/list_book.html', context={'books': Book.objects.all().order_by('-created_at')})
# class DetailBookViewAnt(View):
#     def get(self, request):
#         return render(request, 'books/list_book.html', context={'books': Book.objects.all().order_by('-created_at')})

class ListBookView(LoginRequiredMixin, ListView):
    model = Libro
    queryset = Libro.objects.filter(disponibilidad='disponible')

class ListBookPrestadoView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'books/libros_prestados_usuario.html'
    
    # def get_queryset(self):
    #     return Prestamo.objects.filter(usuario=self.request.user, estado='prestado')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['prestamos_prestados'] = Prestamo.objects.filter(usuario=self.request.user, estado='prestado')
        context['prestamos_devueltos'] = Prestamo.objects.filter(usuario=self.request.user, estado='devuelto')

        return context
    


class DetailBookView(LoginRequiredMixin, DetailView):
    model = Libro
    #template_name = 'books/book_detail.html'

class UpdateBookView(LoginRequiredMixin, UpdateView):
    model= Libro
    fields = ['titulo', 'autores', 'editorial', 'rating', 'fecha_publicacion','genero', 'ISBN', 'resumen','portada']
    template_name="books/libro_update.html"
    success_url = reverse_lazy("list-book")
    
class DeleteBookView(LoginRequiredMixin, DeleteView):
    model= Libro
    #fields = ['title', 'author', 'rating']
    success_url = reverse_lazy("list-book")

class CreateBookView(LoginRequiredMixin, View):
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


@login_required
def realizar_prestamo(request, pk):
    libro = get_object_or_404(Libro, pk=pk)

    if request.method == 'POST':
        usuario = request.user  # Se asume que el usuario actual está autenticado
        fecha_prestamo = date.today()
        fecha_devolucion = fecha_prestamo + timedelta(days=15)  # Se establece una devolución por defecto en 15 días

        # Crear un nuevo préstamo
        Prestamo.objects.create(
            libro=libro,
            fecha_prestamo=fecha_prestamo,
            fecha_devolucion=fecha_devolucion,
            usuario=usuario,
            estado='prestado'
        )

        # Cambiar la disponibilidad del libro a prestado
        libro.disponibilidad = 'prestado'
        libro.save()

        # Redirigir a la página de detalles del libro prestado o a otra página deseada
        return redirect('detail-book', pk=pk)
    
    return render(request, 'books/realizar_prestamo.html', {'libro': libro})

@login_required
def devolver_libro(request, pk):
    libro_prestado = get_object_or_404(Libro, pk=pk, disponibilidad='prestado')
    prestamo = Prestamo.objects.filter(libro=libro_prestado, usuario=request.user, estado='prestado').first()

    if request.method == 'POST':
        # Actualizar estado del préstamo a devuelto
        prestamo.estado = 'devuelto'
        prestamo.fecha_devolucion = date.today()
        prestamo.save()
        

        # Actualizar disponibilidad del libro a disponible
        libro_prestado.disponibilidad = 'disponible'
        libro_prestado.save()

        return redirect('detail-book', pk=pk)

    return render(request, 'books/devolver_libro.html', {'libro': libro_prestado})