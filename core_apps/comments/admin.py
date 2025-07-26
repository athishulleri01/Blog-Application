from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'author', 'post_title', 'created_at', 'view_comment']
    list_filter = ['created_at', 'author', 'post']
    search_fields = ['text', 'author__username', 'post__title']
    readonly_fields = ['created_at']
    raw_id_fields = ['author', 'post']

    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = 'Post'

    def view_comment(self, obj):
        url = reverse('posts:post_detail', args=[obj.post.pk])
        return format_html('<a href="{}#comment-{}" target="_blank">View</a>', url, obj.pk)
    view_comment.short_description = 'View Comment'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post')
