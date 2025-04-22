from django.contrib.auth.models import Group
from rest_framework import serializers
from core.serializers.users import UserSerializer

class GroupSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'users']

    def get_users(self, obj):
        return [{'id': user.id, 'username': user.username, 'email': user.email} for user in obj.user_set.all()]
