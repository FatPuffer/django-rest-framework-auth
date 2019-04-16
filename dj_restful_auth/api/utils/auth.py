from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from api.models import UserInfo, UserToken


class FirstAuthtication(BaseAuthentication):
    """可以有多个认证模型类"""
    def authenticate(self, request):
        pass

    def authenticate_header(self, request):
        pass


class Authtication(BaseAuthentication):
    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在rest framework内部会将整个两个字段赋值给request,以供认证操作使用
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        return 'Basic realm="api"'
