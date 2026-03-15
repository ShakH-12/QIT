from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, min_length=8)
	password2 = serializers.CharField(write_only=True, min_length=8)
	email = serializers.EmailField()

	class Meta:
		model = User
		fields = ["username", "password", "password2", "email"]

	def validate(self, attrs):
		if User.objects.filter(email=attrs["email"]).exists():
			raise serializers.ValidationError({"email": "email already taked"})
		if attrs["password"] != attrs["password2"]:
			raise serializers.ValidationError({"password": "password didn't match"})
		return attrs

	def create(self, validated_data):
		validated_data.pop("password2")
		return User.objects.create_user(**validated_data)


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]
        read_only_fields = ["id", "date_joined"]