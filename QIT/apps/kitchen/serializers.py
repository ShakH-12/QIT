from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Recipe, RecipeImage, RecipeComment, RecipeLike


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeImage
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    recipe_images = RecipeImageSerializer(many=True)
    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ["id", "recipe_images"]


class RecipeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeComment
        fields = ["id", "author", "recipe", "text", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "is_active", "created_at", "updated_at"]

    def create(self, validated_data):
        return RecipeComment.objects.create(**validated_data)


class RecipeLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeLike
        fields = "__all__"
        read_only_fields = ["id", "author", "recipe", "created_at"]