from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CASCADE

# Create your models here.

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField()
    foto = models.ImageField(upload_to='autores/', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    sitio_web = models.URLField()

    def __str__(self):
        return self.nombre
     
class Libro(Model):
    titulo = models.CharField(max_length=200)
    autores = models.ManyToManyField(Autor)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=13)
    resumen = models.TextField()
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)

    DISPONIBILIDAD_CHOICES = (
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('en_proceso', 'En proceso de préstamo'),
    )
    disponibilidad = models.CharField(max_length=20, choices=DISPONIBILIDAD_CHOICES, default='disponible')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.titulo


class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    ESTADO_CHOICES = (
        ('prestado', 'Prestado'),
        ('devuelto', 'Devuelto'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='prestado')

    def __str__(self):
        return f"Prestamo de {self.libro.titulo} a {self.usuario}"

class Usuario(AbstractUser):
    # Agrega cualquier campo adicional que desees para el usuario
    dni = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.username
