from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Izin kustom:
    - Izinkan akses baca (GET, HEAD, OPTIONS) untuk semua user.
    - Izinkan akses tulis (POST, PUT, DELETE) HANYA untuk user admin.
    """
    def has_permission(self, request, view):
        # Izinkan metode aman (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # Cek apakah user sudah login DAN adalah admin
        return request.user.is_authenticated and request.user.is_admin