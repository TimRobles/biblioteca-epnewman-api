from django.contrib import admin
from .models import Book, Rental


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Book.
    """
    list_display = [
        'title',
        'author',
        'isbn',
        'category',
        'year',
        'language',
        'available',
        'created_at',
    ]
    list_filter = ['category', 'language', 'available', 'year']
    search_fields = ['title', 'author', 'isbn', 'isbn10', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'author', 'year', 'publisher')
        }),
        ('Identificación', {
            'fields': ('isbn', 'isbn10')
        }),
        ('Clasificación', {
            'fields': ('category', 'language')
        }),
        ('Descripción', {
            'fields': ('description', 'synopsis')
        }),
        ('Detalles', {
            'fields': ('pages', 'cover_url')
        }),
        ('Estado', {
            'fields': ('available',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Rental.
    """
    list_display = [
        'book',
        'user_name',
        'user_email',
        'rented_at',
        'due_at',
        'status',
        'days_remaining',
    ]
    list_filter = ['status', 'rented_at', 'due_at']
    search_fields = ['book__title', 'user_name', 'user_email']
    readonly_fields = ['rented_at', 'returned_at', 'is_overdue', 'days_remaining']
    ordering = ['-rented_at']
    
    fieldsets = (
        ('Información del Alquiler', {
            'fields': ('book', 'user_name', 'user_email')
        }),
        ('Fechas', {
            'fields': ('rented_at', 'due_at', 'returned_at')
        }),
        ('Estado', {
            'fields': ('status', 'is_overdue', 'days_remaining')
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_returned', 'extend_rental_7_days']
    
    def mark_as_returned(self, request, queryset):
        """Acción para marcar alquileres como devueltos."""
        count = 0
        for rental in queryset:
            if rental.status != 'returned':
                rental.return_book()
                count += 1
        self.message_user(request, f'{count} alquiler(es) marcado(s) como devuelto(s).')
    mark_as_returned.short_description = 'Marcar como devuelto'
    
    def extend_rental_7_days(self, request, queryset):
        """Acción para extender alquileres 7 días."""
        count = 0
        for rental in queryset:
            if rental.status in ['active', 'overdue']:
                rental.extend_rental(days=7)
                count += 1
        self.message_user(request, f'{count} alquiler(es) extendido(s) por 7 días.')
    extend_rental_7_days.short_description = 'Extender 7 días'
