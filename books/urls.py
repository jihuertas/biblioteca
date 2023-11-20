from django.urls import path
from books.views import DeleteBookView, ListBookView, CreateBookView, DetailBookView, UpdateBookView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', ListBookView.as_view(), name='list-book'),
    path('book/new', CreateBookView.as_view(), name='create-book'),
    path('book/<int:pk>', DetailBookView.as_view(), name='detail-book'),
    path('book/<int:pk>/edit', UpdateBookView.as_view(), name='update-book'),
    path('book/<int:pk>/delete', DeleteBookView.as_view(), name='delete-book'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
