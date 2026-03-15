from django.contrib import admin
from .models import Recipe, RecipeImage, RecipeComment, RecipeLike


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active"]
    list_filters = ["title", "is_active", "created_at"]


@admin.register(RecipeImage)
class RecipeImageAdmin(admin.ModelAdmin):
    list_display = ["recipe"]
    list_filters = ["recipe", "image"]


@admin.register(RecipeComment)
class RecipeCommentAdmin(admin.ModelAdmin):
    list_display = ["author"]


@admin.register(RecipeLike)
class RecipeLikeAdmin(admin.ModelAdmin):
    list_display = ["author", "recipe"]