from django.urls import path
from . import views

app_name = "kitchen"

urlpatterns = [
    path("", views.ListView.as_view()),
    path("<int:pk>/", views.DetailView.as_view()),
    path("comment/", views.RecipeCommentListCreateView.as_view()),
    path("like/", views.RecipeLikeView.as_view()),
]