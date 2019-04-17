# -*-coding:GBK -*-
from rest_framework.permissions import BasePermission


class SVIPPermission(BasePermission):
    message = "������SVIP���ܷ���"

    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True
