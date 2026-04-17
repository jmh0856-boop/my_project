from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    # 본인 리소스만 접근 가능하도록 권한 설정
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
