from django.shortcuts import render
from django.http import JsonResponse
from rest_framework .views import APIView
from api.models import UserInfo, UserToken


def md5(user):
    import hashlib
    import time

    ctime = str(time.time())

    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = UserInfo.objects.filter(username=user, password=pwd).first()
            print(obj)
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'

            # 为登录用户创建token
            token = md5(user)
            # 存在就更新，不存在则创建
            print(token)
            UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            print(123)
        except Exception as e:
            pass

        return JsonResponse(ret)
