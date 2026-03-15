from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from .models import Recipe, RecipeComment, RecipeLike
from .serializers import RecipeSerializer, RecipeCommentSerializer, RecipeLikeSerializer


class ListView(generics.ListAPIView):
    queryset = Recipe.objects.filter(is_active=True, is_deleted=False)
    serializer_class = RecipeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]


class DetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.filter(is_active=True, is_deleted=False)
    serializer_class = RecipeSerializer

    def retrieve(self, request, pk):
        instance = self.get_object()
        instance.add_view()
        return Response(RecipeSerializer(instance).data)


class RecipeCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = RecipeCommentSerializer

    def get_queryset(self):
        return RecipeComment.objetcs.filter(is_active=True, recipe_id=self.kwargs["recipe_id"])

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(author=request.user)
        return Response(RecipeCommentSerializer(instance).data)


class RecipeLikeView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecipeLikeSerializer

    def create(self, request, *args, **kwargs):
        recipe_id = request.data.get("recipe")
        if not recipe_id:
            return Response({"recipe": "recipe are required"}, status=400)

        recipe = Recipe.objects.filter(id=recipe_id).first()
        if not recipe:
            return Response({"recipe": "not found"}, status=404)

        like = RecipeLike.objects.filter(author=request.user, recipe=recipe).first()
        if like:
            like.delete()
            return Response({"ok": True, "msg": "like was deleted"})

        instance = RecipeLike.objects.create(author=request.user, recipe=recipe)
        return Response(RecipeLikeSerializer(instance).data)