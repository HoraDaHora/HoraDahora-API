from API.models import CustomUser
from rest_framework import viewsets
from API.serializers import UserSerializer
from rest_framework import permissions
from rest_framework.decorators import permission_classes

# @permission_classes((permissions.AllowAny))
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer