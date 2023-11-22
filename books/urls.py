from django.urls import path
from books.views import DeleteBookView, ListBookView, CreateBookView, DetailBookView, UpdateBookView, ListBookPrestadoView
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', ListBookView.as_view(), name='list-book'),
    path('prestados', ListBookPrestadoView.as_view(), name='libros-prestados'),
    path('book/new', CreateBookView.as_view(), name='create-book'),
    path('book/<int:pk>', DetailBookView.as_view(), name='detail-book'),
    path('book/<int:pk>/edit', UpdateBookView.as_view(), name='update-book'),
    path('book/<int:pk>/delete', DeleteBookView.as_view(), name='delete-book'),
    path('book/<int:pk>/prestamo',views.realizar_prestamo, name='realizar-prestamo'),
    path('book/<int:pk>/devolver',views.devolver_libro, name='devolver-libro'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
