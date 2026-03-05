from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RentalViewSet

# Router para registrar los ViewSets
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'rentals', RentalViewSet, basename='rental')

urlpatterns = [
    path('', include(router.urls)),
]
