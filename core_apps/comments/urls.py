# blog/urls.py
from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [

    path('api/posts/<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment_list_api'),
    path('api/comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail_api'),

    # AJAX endpoints
    path('ajax/posts/<int:post_id>/comments/', views.create_comment_ajax, name='create_comment_ajax'),
    path('ajax/comments/<int:comment_id>/delete/', views.delete_comment_ajax, name='delete_comment_ajax'),
]