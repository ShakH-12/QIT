from django.contrib.auth.models import User
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipe_author", verbose_name="Recipe Author")
    title = models.CharField(validators=[MinLengthValidator(5)], max_length=255, verbose_name="Recipe title", db_index=True)
    description = models.TextField(validators=[MaxLengthValidator(2000)], verbose_name="Recipe description", db_index=True)
    ingredients = models.TextField(validators=[MaxLengthValidator(2000)], verbose_name="Recipe ingredients")
    instructions = models.TextField(validators=[MaxLengthValidator(2000)], verbose_name="Recipe instructions")
    cooking_time = models.PositiveIntegerField(verbose_name="Recipe cooking time")
    views = models.PositiveIntegerField(default=0, verbose_name="Recipe views")
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipies"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["title", "description"])]

    def __str__(self):
        return self.title

    @property
    def is_popular(self):
        return self.views > 100

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def add_view(self):
        self.views += 1
        self.save(update_fields=["views"])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_images")
    image = models.ImageField(upload_to="recipe_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recipe.title

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class RecipeComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipecomment_author", verbose_name="Recipe Comment author", db_index=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipecomment_recipe", verbose_name="Recipe")
    text = models.TextField(db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recipe Comment"
        verbose_name_plural = "Recipe Comments"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["author", "text"])]

    def __str__(self):
        return f"Recipe Comment from {self.author.username}"

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class RecipeLike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipelike_author", verbose_name="Recipe Like author", db_index=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipelike_recipe", verbose_name="Recipe")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)