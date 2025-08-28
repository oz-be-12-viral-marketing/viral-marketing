from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "name", "nickname", "phone_number"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
            nickname=validated_data["nickname"],
            phone_number=validated_data["phone_number"],
            is_active=False,  # 이메일 인증 후 활성화
        )
        return user


class EmailVerificationSerializer(serializers.Serializer):
    uid64 = serializers.CharField()
    token = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs.get("email"), password=attrs.get("password"))
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs["user"] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "nickname", "phone_number"]
        read_only_fields = ["email"]
