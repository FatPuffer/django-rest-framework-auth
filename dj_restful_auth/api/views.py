from django.http import JsonResponse, HttpResponse
from rest_framework .views import APIView
from api.models import UserInfo, UserToken
from api.utils.permision import MyPermission, SVIPPermission

ORDER_DICT = {
    1:{
        'name':'女朋友',
        'age':18,
        'gender':'女',
        'content':'....'
    },
    2:{
        'name':'男朋友',
        'age':22,
        'gender':'男',
        'content':'....'
    },
}


def md5(user):
    import hashlib
    import time

    ctime = str(time.time())

    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    """
    用户登录认证
    """
    # 不需要认证的视图进行如下配置，覆盖全局认证即可
    authentication_classes = []
    # 不需要权限如下配置，覆盖全局配置即可
    permission_classes = []

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'

            # 为登录用户创建token
            token = md5(user)
            ret['token'] = token
            # 存在就更新，不存在则创建
            UserToken.objects.update_or_create(user=obj, defaults={'token': token})
        except Exception as e:
            pass

        return JsonResponse(ret)


# class Authtication(object):
#     def authenticate(self, request):
#         token = request._request.GET.get('token')
#         token_obj = UserToken.objects.filter(token=token).first()
#         if not token_obj:
#             raise exceptions.AuthenticationFailed('用户认证失败')
#         # 在rest framework内部会将整个两个字段赋值给request,以供认证操作使用
#         return (token_obj.user, token_obj)
#
#     def authenticate_header(self, request):
#         pass


class OrderView(APIView):
    """
    订单相关业务（SVIP才有权限查看）
    """
    permission_classes = [SVIPPermission,]

    def get(self, request, *args, **kwargs):
        # Todo: request.user 拿到的就是token_obj.user
        # Todo: request.auth 拿到的就是token_obj
        # token = request._request.GET.get('token')
        # if not token:
        #     return HttpResponse('用户未登录')

        ret = {'code': 1000, 'msg': None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)


class UserInfoView(APIView):
    """
    个人中心（普通用户、VIP用户有权限）
    """
    permission_classes = [MyPermission,]

    def get(self, request, *args, **kwargs):
        print(request.user)
        return HttpResponse('用户信息')

