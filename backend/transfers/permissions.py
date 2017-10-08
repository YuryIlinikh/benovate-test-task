from rest_framework.permissions import BasePermission


class CreateOnly(BasePermission):

    def has_permission(self, request, view):
        return view.action is 'create'

    def has_object_permission(self, request, view, obj):
        return False
