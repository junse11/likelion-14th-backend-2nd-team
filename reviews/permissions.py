from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """본인이 작성한 객체만 수정/삭제 가능"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
