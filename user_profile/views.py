from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from custom_user.models import CustomUser
from custom_user.serializers import CustomUserSerializer


class UserProfileView(generics.RetrieveAPIView,
                      generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'patch']
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get(self, request: Request, *args, **kwargs):
        """
        본인의 프로필입니다.
        `profile_image`는 이미지를 바로 다운 받을 수 있는 url이 제공됩니다.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def patch(self, request: Request, *args, **kwargs):
        """
        프로필을 수정합니다.
        이미지는 바로 업로드 하면 됩니다.
        """
        s: CustomUserSerializer = self.get_serializer()
        s.update(request.user, request.data)

        return Response(self.get_serializer(request.user).data)
