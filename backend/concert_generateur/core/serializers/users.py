from rest_framework import serializers
from core.models.users import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'artist')  # Par défaut, rôle artiste
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cette adresse email est déjà utilisée.")
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
