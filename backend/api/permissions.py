from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrRedOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminCurentUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_superuser
                or obj.author == request.user)
