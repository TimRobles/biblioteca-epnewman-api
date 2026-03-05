from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Rental
from .serializers import (
    BookSerializer,
    BookListSerializer,
    RentalSerializer,
    RentalCreateSerializer,
    ExtendRentalSerializer,
    BookStatisticsSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar libros.
    
    Endpoints:
    - GET /api/books/ - Listar libros con búsqueda y filtros
    - POST /api/books/ - Crear nuevo libro
    - GET /api/books/{id}/ - Obtener detalle de libro
    - PUT/PATCH /api/books/{id}/ - Actualizar libro
    - DELETE /api/books/{id}/ - Eliminar libro
    - GET /api/books/statistics/ - Obtener estadísticas
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'description', 'isbn', 'isbn10']
    ordering_fields = ['title', 'author', 'year', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        Usa BookListSerializer para listado y BookSerializer para detalle.
        """
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer
    
    def get_queryset(self):
        """
        Filtra libros por query params:
        - category: filtrar por categoría
        - available: filtrar por disponibilidad (true/false)
        - author: filtrar por autor exacto
        - year: filtrar por año
        - language: filtrar por idioma
        """
        queryset = Book.objects.all()
        
        # Filtrar por categoría
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filtrar por disponibilidad
        available = self.request.query_params.get('available', None)
        if available is not None:
            is_available = available.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(available=is_available)
        
        # Filtrar por autor
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__icontains=author)
        
        # Filtrar por año
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(year=year)
        
        # Filtrar por idioma
        language = self.request.query_params.get('language', None)
        if language:
            queryset = queryset.filter(language=language)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Endpoint para obtener estadísticas de la biblioteca.
        GET /api/books/statistics/
        """
        total_books = Book.objects.count()
        available_books = Book.objects.filter(available=True).count()
        rented_books = total_books - available_books
        
        total_rentals = Rental.objects.count()
        active_rentals = Rental.objects.filter(status='active').count()
        overdue_rentals = Rental.objects.filter(status='overdue').count()
        
        data = {
            'total_books': total_books,
            'available_books': available_books,
            'rented_books': rented_books,
            'total_rentals': total_rentals,
            'active_rentals': active_rentals,
            'overdue_rentals': overdue_rentals,
        }
        
        serializer = BookStatisticsSerializer(data)
        return Response(serializer.data)


class RentalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar alquileres.
    
    Endpoints:
    - GET /api/rentals/ - Listar alquileres
    - POST /api/rentals/ - Crear alquiler (alquilar libro)
    - GET /api/rentals/{id}/ - Obtener detalle de alquiler
    - PATCH /api/rentals/{id}/extend/ - Extender plazo de alquiler
    - PATCH /api/rentals/{id}/return/ - Devolver libro
    """
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rented_at', 'due_at', 'status']
    ordering = ['-rented_at']
    
    def get_serializer_class(self):
        """
        Usa RentalCreateSerializer para creación y RentalSerializer para el resto.
        """
        if self.action == 'create':
            return RentalCreateSerializer
        return RentalSerializer
    
    def get_queryset(self):
        """
        Filtra alquileres por query params:
        - status: filtrar por estado (active, returned, overdue)
        - user_email: filtrar por email del usuario
        - book: filtrar por ID del libro
        """
        queryset = Rental.objects.select_related('book').all()
        
        # Filtrar por estado
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filtrar por email del usuario
        user_email = self.request.query_params.get('user_email', None)
        if user_email:
            queryset = queryset.filter(user_email__iexact=user_email)
        
        # Filtrar por libro
        book_id = self.request.query_params.get('book', None)
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        
        return queryset
    
    @action(detail=True, methods=['patch'])
    def extend(self, request, pk=None):
        """
        Extiende el plazo de un alquiler activo.
        PATCH /api/rentals/{id}/extend/
        
        Body: { "days": 7 }
        """
        rental = self.get_object()
        
        # Validar que el alquiler esté activo
        if rental.status not in ['active', 'overdue']:
            return Response(
                {'error': 'Solo se pueden extender alquileres activos o vencidos.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar y obtener días a extender
        serializer = ExtendRentalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        days = serializer.validated_data.get('days', 7)
        
        # Extender alquiler
        rental.extend_rental(days=days)
        
        # Si estaba vencido, actualizar a activo
        if rental.status == 'overdue':
            rental.status = 'active'
            rental.save()
        
        # Serializar y retornar
        response_serializer = RentalSerializer(rental)
        return Response(response_serializer.data)
    
    @action(detail=True, methods=['patch'])
    def return_book(self, request, pk=None):
        """
        Marca un alquiler como devuelto.
        PATCH /api/rentals/{id}/return/
        """
        rental = self.get_object()
        
        # Validar que el alquiler no esté ya devuelto
        if rental.status == 'returned':
            return Response(
                {'error': 'Este alquiler ya fue devuelto.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Devolver libro
        rental.return_book()
        
        # Serializar y retornar
        serializer = RentalSerializer(rental)
        return Response(serializer.data)
