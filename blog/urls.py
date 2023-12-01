from django.urls import path
from . import views

app_name = 'blog'  # app namespace

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('posts/', views.post_list, name='post_list'),
    # class-based post list view:
    # path('posts/', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),
    path('search/', views.post_search, name='post_search'),
    path('search_form/', views.post_search_form, name='post_search_form'),
]