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
    path('comments/ajax/edit/<int:comment_id>/', views.edit_comment_ajax, name='edit_comment_ajax'),
    path('ajax/posts/<int:post_id>/comments/page/', views.load_comments_page, name='load_comments_page'),
    
]