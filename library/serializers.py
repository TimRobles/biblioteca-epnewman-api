from rest_framework import serializers
from .models import Book, Rental


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Book.
    Incluye todos los campos y campos calculados.
    """
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'isbn10',
            'category',
            'description',
            'synopsis',
            'cover_url',
            'year',
            'language',
            'publisher',
            'pages',
            'available',
            'is_available',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de libros.
    Solo incluye campos esenciales para mejorar performance.
    """
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'category',
            'cover_url',
            'year',
            'language',
            'available',
            'is_available',
        ]


class RentalSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Rental.
    Incluye información detallada del libro asociado.
    """
    book_detail = BookListSerializer(source='book', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Rental
        fields = [
            'id',
            'book',
            'book_detail',
            'user_name',
            'user_email',
            'rented_at',
            'due_at',
            'returned_at',
            'status',
            'notes',
            'is_overdue',
            'days_remaining',
        ]
        read_only_fields = ['id', 'rented_at', 'returned_at']
    
    def validate_book(self, value):
        """
        Valida que el libro esté disponible para alquilar.
        """
        if not value.available:
            raise serializers.ValidationError(
                "Este libro no está disponible para alquiler en este momento."
            )
        return value


class RentalCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear un alquiler.
    Solo incluye campos necesarios para la creación.
    """
    class Meta:
        model = Rental
        fields = [
            'book',
            'user_name',
            'user_email',
            'notes',
        ]
    
    def validate_book(self, value):
        """
        Valida que el libro esté disponible para alquilar.
        """
        if not value.available:
            raise serializers.ValidationError(
                "Este libro no está disponible para alquiler en este momento."
            )
        return value
    
    def create(self, validated_data):
        """
        Crea un alquiler y marca el libro como no disponible.
        """
        rental = Rental.objects.create(**validated_data)
        return rental


class ExtendRentalSerializer(serializers.Serializer):
    """
    Serializer para extender un alquiler.
    """
    days = serializers.IntegerField(
        min_value=1,
        max_value=30,
        default=7,
        help_text="Número de días para extender el alquiler (1-30)"
    )


class BookStatisticsSerializer(serializers.Serializer):
    """
    Serializer para estadísticas de libros.
    """
    total_books = serializers.IntegerField()
    available_books = serializers.IntegerField()
    rented_books = serializers.IntegerField()
    total_rentals = serializers.IntegerField()
    active_rentals = serializers.IntegerField()
    overdue_rentals = serializers.IntegerField()
