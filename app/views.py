from app import models
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin
from app.exceptions import exception
from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


"""
1.序列化
"""
class dataserializer(DynamicFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ["id","username","password","Role",]

    def create(self, validated_data):
        """新增用户(管理员-10001 / 客服-20001 / 会员-30001)"""
        role = validated_data["Role"]
        user_obj = models.UserProfile.objects.create_user(**validated_data)

        if role == "10001": # 管理员
            group, created = Group.objects.get_or_create(name="admin")
        elif role == "20001": # 客服
            group, created = Group.objects.get_or_create(name="server")
        elif role == "30001": # 会员
            group, created = Group.objects.get_or_create(name="player")
        else:
            raise exception.myException400("Role error")

        group.user_set.add(user_obj)  # 把用户添加到xxx权限组

        return user_obj
"""
2.视图
"""
class getdata(mixins.CreateModelMixin,
              mixins.DestroyModelMixin,
              mixins.UpdateModelMixin,
              mixins.ListModelMixin,
              mixins.RetrieveModelMixin,
              GenericViewSet):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserProfile.objects.all()
    serializer_class = dataserializer

