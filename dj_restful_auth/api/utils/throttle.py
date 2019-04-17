from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
# import time
#
# VISIT_RECORD = {}
#
#
# class VisitThrottle(object):
#     """60s内只能访问3次"""
#
#     def __init__(self):
#         self.history = None
#
#     def allow_request(self, request, view):
#         # 1.获取用户IP
#         remote_addr = request.META.get('REMOTE_ADDR')
#         # 获取当前时间
#         ctime = time.time()
#         if remote_addr not in VISIT_RECORD:
#             # 利用时间记录访问次数
#             VISIT_RECORD[remote_addr] = [ctime,]
#             return True
#
#         # 获取历史访问记录列表
#         history = VISIT_RECORD.get(remote_addr)
#         self.history = history
#
#         # 如果当前时间减去60s还大于我们访问记录中的最早的数据，说明该数据是在距离60秒前的数据，则将其删除
#         # 同时将最新的时间数据插入在列表最左侧
#         # 此处目的：控制列表仅保留60s以内的数据
#         while history and history[-1] < ctime - 60:
#             # 删除60s以外的数据
#             history.pop()
#
#         # 如果列表长度小于3，则将新的访问数据加入列表
#         if len(history) < 3:
#             history.insert(0, ctime)
#             return True  # 表示可以继续访问
#         else:
#             return False  # 表示访问频率过高，被限制
#
#     def wait(self):
#         # 可以实现用户界面提示，提示用户还需要等待多久才能继续访问
#         ctime = time.time()
#         # 获取剩余限制时间
#         last_time = 60 - (ctime - self.history[-1])
#         return last_time


class VisitThrottle(SimpleRateThrottle):
    """游客60s内只能访问3次"""
    scope = 'Fatpuffer'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    """登录用户60s内只能访问10次"""
    scope = 'AutienticateUser'

    def get_cache_key(self, request, view):
        return request.user.username
