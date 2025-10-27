from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Hapus TokenObtainPairView bawaan dari sini
from rest_framework_simplejwt.views import TokenRefreshView 
# Impor View login kustom Anda
from apps.users.views import MyTokenObtainPairView 

from apps.films.views import FilmViewSet
from apps.comments.views import CommentViewSet
from apps.thumbs.views import ThumbViewSet

# Buat router
router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='film')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'thumbs', ThumbViewSet, basename='thumb')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URL API untuk Autentikasi User
    path('api/users/', include('apps.users.urls')),

    # URL API untuk Login (JWT)
    # VVV GUNAKAN VIEW KUSTOM ANDA DI SINI VVV
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Daftarkan semua URL dari router ke /api/
    path('api/', include(router.urls)),
]