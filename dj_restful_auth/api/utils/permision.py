# -*-coding:GBK -*-
from rest_framework.permissions import BasePermission


class SVIPPermission(BasePermission):
    message = "必须是SVIP才能访问"

    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True
