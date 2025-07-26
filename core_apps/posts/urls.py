from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home,name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # API endpoints
    path('api/posts/', views.PostListCreateView.as_view(), name='post_list_api'),
    path('api/posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail_api'),    
    path('api/search/', views.search_posts, name='search_posts'),

    
    # AJAX endpoints
    path('ajax/posts/create/', views.create_post_ajax, name='create_post_ajax'),
    path('ajax/posts/<int:post_id>/update/', views.update_post_ajax, name='update_post_ajax'),
    path('ajax/posts/<int:post_id>/delete/', views.delete_post_ajax, name='delete_post_ajax'),
    path('ajax/posts/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
   
]