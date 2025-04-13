from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group
from core.serializers.groups import GroupSerializer

class GroupAdminViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
