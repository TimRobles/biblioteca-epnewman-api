from django.db import models
from django.utils import timezone
from datetime import timedelta


class Book(models.Model):
    """
    Modelo para representar un libro en la biblioteca.
    """
    CATEGORY_CHOICES = [
        ('ficcion', 'Ficción'),
        ('no_ficcion', 'No Ficción'),
        ('ciencia', 'Ciencia'),
        ('tecnologia', 'Tecnología'),
        ('historia', 'Historia'),
        ('arte', 'Arte'),
        ('filosofia', 'Filosofía'),
        ('poesia', 'Poesía'),
        ('infantil', 'Infantil'),
        ('juvenil', 'Juvenil'),
        ('autoayuda', 'Autoayuda'),
        ('biografia', 'Biografía'),
        ('otros', 'Otros'),
    ]
    
    LANGUAGE_CHOICES = [
        ('es', 'Español'),
        ('en', 'Inglés'),
        ('fr', 'Francés'),
        ('de', 'Alemán'),
        ('it', 'Italiano'),
        ('pt', 'Portugués'),
        ('otros', 'Otros'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Título')
    author = models.CharField(max_length=200, verbose_name='Autor')
    isbn = models.CharField(max_length=13, unique=True, verbose_name='ISBN-13')
    isbn10 = models.CharField(max_length=10, blank=True, null=True, verbose_name='ISBN-10')
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='otros',
        verbose_name='Categoría'
    )
    description = models.TextField(verbose_name='Descripción')
    synopsis = models.TextField(blank=True, null=True, verbose_name='Sinopsis')
    cover_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='URL de Portada'
    )
    year = models.IntegerField(verbose_name='Año de Publicación')
    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default='es',
        verbose_name='Idioma'
    )
    publisher = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Editorial'
    )
    pages = models.IntegerField(blank=True, null=True, verbose_name='Páginas')
    available = models.BooleanField(default=True, verbose_name='Disponible')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
            models.Index(fields=['available']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    @property
    def is_available(self):
        """Verifica si el libro está disponible para alquilar."""
        return self.available


class Rental(models.Model):
    """
    Modelo para representar un alquiler de libro.
    """
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('returned', 'Devuelto'),
        ('overdue', 'Vencido'),
    ]
    
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='rentals',
        verbose_name='Libro'
    )
    user_name = models.CharField(max_length=200, verbose_name='Nombre del Usuario')
    user_email = models.EmailField(verbose_name='Email del Usuario')
    rented_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Alquiler')
    due_at = models.DateTimeField(verbose_name='Fecha de Vencimiento')
    returned_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Fecha de Devolución'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Estado'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='Notas')
    
    class Meta:
        verbose_name = 'Alquiler'
        verbose_name_plural = 'Alquileres'
        ordering = ['-rented_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user_email']),
            models.Index(fields=['due_at']),
        ]
    
    def __str__(self):
        return f"{self.book.title} - {self.user_name} ({self.status})"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para:
        1. Establecer la fecha de vencimiento (14 días por defecto)
        2. Actualizar el estado si está vencido
        3. Actualizar la disponibilidad del libro
        """
        # Si es un nuevo alquiler, establecer fecha de vencimiento
        if not self.pk and not self.due_at:
            self.due_at = timezone.now() + timedelta(days=14)
        
        # Actualizar estado si está vencido
        if self.status == 'active' and timezone.now() > self.due_at:
            self.status = 'overdue'
        
        # Guardar el alquiler
        super().save(*args, **kwargs)
        
        # Actualizar disponibilidad del libro
        self.update_book_availability()
    
    def update_book_availability(self):
        """Actualiza la disponibilidad del libro basándose en alquileres activos."""
        active_rentals = Rental.objects.filter(
            book=self.book,
            status__in=['active', 'overdue']
        ).exists()
        
        self.book.available = not active_rentals
        self.book.save()
    
    def extend_rental(self, days=7):
        """Extiende el período de alquiler por un número de días."""
        self.due_at = self.due_at + timedelta(days=days)
        self.save()
        return self
    
    def return_book(self):
        """Marca el libro como devuelto."""
        self.returned_at = timezone.now()
        self.status = 'returned'
        self.save()
        return self
    
    @property
    def is_overdue(self):
        """Verifica si el alquiler está vencido."""
        return self.status == 'active' and timezone.now() > self.due_at
    
    @property
    def days_remaining(self):
        """Calcula los días restantes del alquiler."""
        if self.status != 'active':
            return 0
        delta = self.due_at - timezone.now()
        return max(0, delta.days)
