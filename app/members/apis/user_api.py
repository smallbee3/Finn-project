from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.image.resize import clear_imagekit_cache_img_profile
from utils.pagination.custom_pagination import CustomPagination
from utils.permission.custom_permission import IsOwnerOrReadOnly
from ..serializers import (
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer)

__all__ = (
    'UserListCreateAPIView',
    'UserRetrieveUpdateDestroyAPIView',
    'UserProfileImageDeleteAPIView',
)

User = get_user_model()

"""
1. 유저만들기 (회원가입)
2. 유저리스트
3. 유저정보
4. 유저 삭제
5. 유저 수정
"""


class UserListCreateAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request):

        user_list = User.objects.filter(Q(is_superuser=False), Q(is_staff=False))

        # 1) Pagination 적용 이전
        # return Response(UserSerializer(user_list, many=True).data, status=status.HTTP_200_OK)

        # 2) CustomPagination 사용
        # users = [UserSerializer(user).data for user in user_list]
        users = UserSerializer(user_list, many=True).data
        # print(users)
        pagination = CustomPagination(users, request)

        return Response(pagination.object_list, status=status.HTTP_200_OK)


class UserRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,

        IsOwnerOrReadOnly,
        # APIView 상에서 동작을 안함
        # -> return obj.owner == request.user 라는 잘못된 코드가 있는데도
        #    Generic View 로 고치기 전까지 호출자체가 안되서 모르고 있었음..
    )

    def get(self, request, pk):
        data = {
            'user': UserSerializer(get_object_or_404(User, pk=pk)).data
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        # if request.user == user:
        # serializer = UserUpdateSerializer(request.user, data=request.data)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save(images=request.FILES.get('img_profile'))
            # 위 코드 대신 def validate에서 images를 꺼낸 후 validation까지 한 후 넣어준다.

            serializer.save()
            # return Response(serializer.data, status=status.HTTP_200_OK)
            # 디버깅 할 때 수정된 정보만 보기위해 설정 -> "serializer.data"

            user = get_object_or_404(User, pk=pk)
            # 이곳에서 'user'를 호출하지 않으면 수정된 데이터가 Response에 나타나지 않음.
            # (* 위에서 user에 할당된 데이터는 serializers/auth.py에서 'user.save()'로
            # 값이 변하지 않기 때문에)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        # return Response('일치하는 회원정보가 없습니다.', status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        # user = get_object_or_404(User, pk=pk)
        try:
            user = User.objects.get(pk=pk)
        # except Exception as ex:
        #     print(ex)
        #     print(type(ex))
        #     print(type(ex).__name__)
        #     print(ex.__class__.__name__)

        # except DoesNotExist as exception:

        except:
            return Response('일치하는 회원정보가 없습니다.', status=status.HTTP_204_NO_CONTENT)

        if request.user == user:
            serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                user = get_object_or_404(User, pk=pk)
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response('일치하는 회원정보가 없습니다.', status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):

        # serializer = AuthTokenSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     user = serializer.validated_data.get('user')
        #     user.delete()
        # user = get_object_or_404(User, pk=pk)
        user = User.objects.get(pk=pk)
        if request.user == user:
            request.user.delete()
            return Response('해당 유저가 삭제되었습니다.', status=status.HTTP_204_NO_CONTENT)
        return Response('일치하는 회원정보가 없습니다.', status=status.HTTP_404_NOT_FOUND)


class UserProfileImageDeleteAPIView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user == user:
            if user.images.img_profile:
                # clear_imagekit_cache_img_profile(user.pk)
                user.images.img_profile.delete()
                user.images.img_profile_28.delete()
                user.images.img_profile_225.delete()
                return Response('해당 유저의 프로필사진이 삭제되었습니다.', status=status.HTTP_200_OK)
            return Response('해당 유저의 프로필사진이 존재하지 않습니다.', status=status.HTTP_404_NOT_FOUND)
        return Response('일치하는 회원정보가 없습니다.', status=status.HTTP_404_NOT_FOUND)
