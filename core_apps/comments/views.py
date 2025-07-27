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
from django.template.defaultfilters import linebreaks

from core_apps.posts.models import Post
from .models import Comment
from .serializers import CommentSerializer
from core_apps.posts.serializers import PostSerializer, PostListSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    """List comments for a post or create a new comment"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).select_related('author').order_by('created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a comment"""
    queryset = Comment.objects.select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'DELETE'] and obj.author != self.request.user:
            self.permission_denied(self.request, message="You can only edit your own comments.")
        return obj



@require_http_methods(["POST"])
@login_required
def create_comment_ajax(request, post_id):
    """Create a new comment via AJAX"""
    try:
        post = get_object_or_404(Post, id=post_id)
        data = json.loads(request.body)
        
        text = data.get('text', '').strip()
        if not text:
            return JsonResponse({
                'success': False,
                'errors': {'text': ['This field is required.']}
            })
        
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            text=text
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Comment added successfully!',
            'comment': {
                'id': comment.id,
                'text': comment.text,
                'author': comment.author.username,
                'author_full_name': comment.author.get_full_name() or comment.author.username,
                'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p'),
            }
        })
        
    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Post not found.'
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
def delete_comment_ajax(request, comment_id):
    """Delete a comment via AJAX"""
    try:
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        comment.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Comment deleted successfully!'
        })
        
    except Comment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Comment not found or you do not have permission to delete it.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        })


@require_http_methods(["PUT"])
@login_required
def edit_comment_ajax(request, comment_id):
    try:
        # Get the comment and check ownership
        comment = get_object_or_404(Comment, id=comment_id)

        # Check if user owns the comment
        if comment.author != request.user:
            return JsonResponse({
                'success': False,
                'message': 'You are not authorized to edit this comment.'
            }, status=403)

        # Parse JSON data
        try:
            if not request.body:
                return JsonResponse({
                    'success': False,
                    'message': 'No data received'
                }, status=400)
                
            data = json.loads(request.body.decode('utf-8'))
            print(f"Parsed data: {data}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)

        # Get and validate the new text
        new_text = data.get('text', '').strip()
        print(f"New text: '{new_text}'")
        
        if not new_text:
            return JsonResponse({
                'success': False,
                'errors': {'text': ['This field is required.']}
            }, status=400)

        # Update the comment
        old_text = comment.text
        comment.text = new_text
        comment.save()
        
        print(f"Comment updated from '{old_text}' to '{new_text}'")

        # Return success response
        return JsonResponse({
            'success': True,
            'message': 'Comment updated successfully!',
            'comment': {
                'id': comment.id,
                'text': comment.text, 
                'text_html': linebreaks(comment.text),  
                'author': comment.author.username,
                'updated_at': str(comment.updated_at),
            }
        })

    except Comment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Comment not found.'
        }, status=404)
    except Exception as e:
        print(f"Unexpected error in edit_comment_ajax: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)