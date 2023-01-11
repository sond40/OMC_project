from django.urls import path, re_path
from . import views

app_name ="omc"
urlpatterns = [
    path('', views.RecipeList.as_view(), name='recipe_list_view'),
    path('<int:pk>/', views.RecipeDetail.as_view(), name='recipe_detail_view'),
    path('refrigerator/', views.RefrigeratorList.as_view(), name='refrigerator_view'),
    path('search/<str:q>/', views.RecipeSearch.as_view(), name='recipe_search'),
    re_path(r'category/[0-9]{8}/', views.RecipeCategory.as_view(), name='recipe_category'),
]
 