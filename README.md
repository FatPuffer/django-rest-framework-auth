# django-rest-framework-auth

# 1.认证

  ## 问题 1：有些API需要用户登录成功之后，才能访问：有些无需登录就能访问。
  
  ## 基本使用认证组件
  
    解决：
    
      a：创建两张表
    
      b：用户登录（返回token并保存到数据库）
  
  ## 认证方式
  
    1. 局部视图使用&全局使用
    
    2. 匿名时：request.user = None
  
  ## 使用
  
    1. 创建类：必须继承：from rest_framework.authentication import BaseAuthentication，实现 authenticate 方法 和 authenticate_header（直接pass即可）
    
    2. 返回值：
    
      a：None，该认证类不做处理，交给其他认证类处理
      
      b：raise exceptions.AuthenticationFailed('用户认证失败')  # from rest_framework import exceptions
      
      c：return (token_obj.user, token_obj)  # 元素1赋值给 request.user; 元素2赋值给 request.auth
    
    3. 局部使用
      
      在视图类里面写上
          
      authentication_classes = [Authentication,]
    
    4. 全局使用
    
      REST_FRAMEWORK = {
        
        # 全局认证配置
        
        "DEFAULT_AUTHENTICATION_CLASSES": ['api.utils.auth.FirstAuthtication', 'api.utils.auth.Authtication'],
        
        # 当用户认证失败时，返回的信息，默认返回匿名用户（）
        
        # "UNAUTHENTICATED_USER": lambda:"匿名用户"
        
        "UNAUTHENTICATED_USER": None,  # 匿名，request.user = None
        
        "UNAUTHENTICATED_TOKEN": None,  # 匿名，request.auth = None
      }
      
      
  ## 源码流程
    
    1. dispatch
    
      a. 封装request
        
        获取定义的认证类（全局/局部），通过列表生成式创建对象
    
      b. initial
      
        perform_authentication
          request.user(内部循环.....)
          
# 2. 权限 
  
  ## 1. 基本使用
  
      a：创建权限管理类（可以有多个）

            class SVIPPermission(object):
                def has_permission(self, request, view):
                    if request.user.user_type != 3:
                        return False
                    return True
                    
            class MyPermission(object):
                def has_permission(self, request, view):
                    if request.user.user_type != 3:
                        return False
                    return True
      
      b：在视图类中使用
         
            permission_classes = [MyPermission,]

  ## 1. 全局使用
      
      REST_FRAMEWORK = {
        
        # 全局权限配置
        
        "DEFAULT_PERMISSION_CLASSES": ['api.utils.permision.SVIPPermission',],
        
      }
      
      
# 3. 节流（频率限制）

  ## 1. 局部使用
  
      a：创建节流管理类（可以有多个）

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
                 
       b：在视图类中使用

            throttle_classes = [VisitThrottle,]

  ## 1. 全局使用
      
      REST_FRAMEWORK = {
        
        # 全局节流（访问频率限制）配置
        
        "DEFAULT_THROTTLE_RATES": {
        # s秒  m分  h时  d天
        "Fatpuffer": '3/m',  # 游客每分钟访可问3次，根据ip限制
        "AutienticateUser": '10/m'  # 登录用户每分钟可访问10次，根据用户名限制
      }
        
      
