from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'total_likes', 'total_comments', 'view_post']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'total_likes', 'total_comments']
    raw_id_fields = ['author']
    filter_horizontal = ['likes']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('Engagement', {
            'fields': ('likes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def view_post(self, obj):
        url = reverse('posts:post_detail', args=[obj.pk])
        return format_html('<a href="{}" target="_blank">View</a>', url)
    view_post.short_description = 'View Post'

    def total_likes(self, obj):
        return obj.likes.count()
    total_likes.short_description = 'Likes'

    def total_comments(self, obj):
        return obj.comments.count()
    total_comments.short_description = 'Comments'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author').prefetch_related('likes', 'comments')

# Customize admin site
admin.site.site_header = "BlogApp Administration"
admin.site.site_title = "BlogApp Admin"
admin.site.index_title = "Welcome to BlogApp Administration"