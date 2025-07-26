from django.shortcuts import render




# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Count
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
import json

from .models import Post
from core_apps.comments.models import Comment
from core_apps.comments.serializers import CommentSerializer
from .serializers import PostSerializer, PostListSerializer

def home(request):
    """Home page with post listing"""
    posts = Post.objects.select_related('author').prefetch_related('likes', 'comments').annotate(
        total_likes=Count('likes'),
        total_comments=Count('comments')
    ).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'search_query': search_query,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'user/home.html', context)

def post_detail(request, pk):
    """Post detail page"""
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related('likes', 'comments__author'),
        pk=pk
    )
    comments = post.comments.select_related('author').order_by('created_at')
    
    context = {
        'post': post,
        'comments': comments,
        'total_likes': post.total_likes(),
        'total_comments': post.total_comments(),
        'is_liked': post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False,
    }
    return render(request, 'blog/post_details.html', context)

# API Views
class PostListCreateView(generics.ListCreateAPIView):
    """List all posts or create a new post"""
    queryset = Post.objects.select_related('author').prefetch_related('likes', 'comments').annotate(
        total_likes=Count('likes'),
        total_comments=Count('comments')
    ).order_by('-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return queryset

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a post"""
    queryset = Post.objects.select_related('author').prefetch_related('likes', 'comments__author')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'DELETE'] and obj.author != self.request.user:
            self.permission_denied(self.request, message="You can only edit your own posts.")
        return obj


# AJAX Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    """Toggle like/unlike for a post"""
    try:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            is_liked = False
            message = "Post unliked"
        else:
            post.likes.add(user)
            is_liked = True
            message = "Post liked"
        
        return Response({
            'success': True,
            'is_liked': is_liked,
            'total_likes': post.total_likes(),
            'message': message
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@require_http_methods(["POST"])
@login_required
def create_post_ajax(request):
    """Create a new post via AJAX"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        if not title:
            return JsonResponse({
                'success': False,
                'errors': {'title': ['This field is required.']}
            })
        
        if not content:
            return JsonResponse({
                'success': False,
                'errors': {'content': ['This field is required.']}
            })
        
        # Create post
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Post created successfully!',
            'post': {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': post.author.username,
                'created_at': post.created_at.strftime('%B %d, %Y at %I:%M %p'),
                'total_likes': 0,
                'total_comments': 0,
            },
            'redirect_url': f'/post/{post.id}/'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        })

@require_http_methods(["PUT"])
@login_required
def update_post_ajax(request, post_id):
    """Update a post via AJAX"""
    try:
        post = get_object_or_404(Post, id=post_id, author=request.user)
        data = json.loads(request.body)
        
        # Validate required fields
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        if not title:
            return JsonResponse({
                'success': False,
                'errors': {'title': ['This field is required.']}
            })
        
        if not content:
            return JsonResponse({
                'success': False,
                'errors': {'content': ['This field is required.']}
            })
        
        # Update post
        post.title = title
        post.content = content
        post.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Post updated successfully!',
            'post': {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'updated_at': post.updated_at.strftime('%B %d, %Y at %I:%M %p'),
            }
        })
        
    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Post not found or you do not have permission to edit it.'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        })

@require_http_methods(["DELETE"])
@login_required
def delete_post_ajax(request, post_id):
    """Delete a post via AJAX"""
    try:
        post = get_object_or_404(Post, id=post_id, author=request.user)
        post.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Post deleted successfully!',
            'redirect_url': '/'
        })
        
    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Post not found or you do not have permission to delete it.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        })

# Search API
@api_view(['GET'])
def search_posts(request):
    """Search posts API endpoint"""
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({'results': []})
    
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ).select_related('author').annotate(
        total_likes=Count('likes'),
        total_comments=Count('comments')
    ).order_by('-created_at')[:10]
    
    serializer = PostListSerializer(posts, many=True, context={'request': request})
    return Response({'results': serializer.data})