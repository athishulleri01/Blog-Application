// static/js/blog.js

// Blog-specific functionality
window.BlogApp = window.BlogApp || {};

// Post management functions
BlogApp.posts = {
    // Create a new post
    create: async function(postData) {
        try {
            const response = await BlogApp.api.post('/ajax/posts/create/', postData);
            return response;
        } catch (error) {
            console.error('Error creating post:', error);
            throw error;
        }
    },

    // Update an existing post
    update: async function(postId, postData) {
        try {
            const response = await fetch(`/ajax/posts/${postId}/update/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': BlogApp.getCsrfToken(),
                },
                body: JSON.stringify(postData)
            });
            return await response.json();
        } catch (error) {
            console.error('Error updating post:', error);
            throw error;
        }
    },

    // Delete a post
    delete: async function(postId) {
        try {
            const response = await BlogApp.api.delete(`/ajax/posts/${postId}/delete/`);
            return response;
        } catch (error) {
            console.error('Error deleting post:', error);
            throw error;
        }
    },

    // Toggle like on a post
    toggleLike: async function(postId) {
        try {
            const response = await BlogApp.api.post(`/ajax/posts/${postId}/like/`);
            return response;
        } catch (error) {
            console.error('Error toggling like:', error);
            throw error;
        }
    },

    // Search posts
    search: async function(query) {
        try {
            const response = await BlogApp.api.get(`/api/search/?q=${encodeURIComponent(query)}`);
            return response;
        } catch (error) {
            console.error('Error searching posts:', error);
            throw error;
        }
    }
};

// Comment management functions
BlogApp.comments = {
    // Add a comment to a post
    create: async function(postId, commentData) {
        try {
            const response = await BlogApp.api.post(`/ajax/posts/${postId}/comments/`, commentData);
            return response;
        } catch (error) {
            console.error('Error creating comment:', error);
            throw error;
        }
    },

    // Delete a comment
    delete: async function(commentId) {
        try {
            const response = await BlogApp.api.delete(`/ajax/comments/${commentId}/delete/`);
            return response;
        } catch (error) {
            console.error('Error deleting comment:', error);
            throw error;
        }
    }
};

// Global post functions (for backward compatibility)
window.toggleLike = async function(postId) {
    if (!document.querySelector('meta[name="user-authenticated"]')) {
        // User not authenticated, show login modal
        const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
        loginModal.show();
        return;
    }

    try {
        const response = await BlogApp.posts.toggleLike(postId);
        
        if (response.success) {
            // Update all like buttons for this post
            document.querySelectorAll(`[data-post-id="${postId}"] .like-btn, .like-btn[onclick*="${postId}"]`).forEach(btn => {
                const likeCount = btn.querySelector('.like-count');
                
                if (response.is_liked) {
                    btn.classList.add('liked');
                } else {
                    btn.classList.remove('liked');
                }
                
                if (likeCount) {
                    likeCount.textContent = response.total_likes;
                }
            });
        } else {
            BlogApp.showNotification(response.message || 'Failed to update like', 'danger');
        }
    } catch (error) {
        BlogApp.showNotification('Failed to update like', 'danger');
    }
};

window.editPost = function(postId) {
    // For home page - redirect to post detail for editing
    if (window.location.pathname === '/') {
        window.location.href = `/post/${postId}/`;
        return;
    }
    
    // For post detail page - show edit modal
    const editModal = document.getElementById('editPostModal');
    if (editModal) {
        const modal = new bootstrap.Modal(editModal);
        modal.show();
    }
};

window.deletePost = async function(postId) {
    if (!confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await BlogApp.posts.delete(postId);
        
        if (response.success) {
            BlogApp.showNotification(response.message, 'success');
            
            // If on home page, remove the post card
            if (window.location.pathname === '/') {
                const postCard = document.querySelector(`[data-post-id="${postId}"]`);
                if (postCard) {
                    postCard.style.transition = 'all 0.3s ease';
                    postCard.style.opacity = '0';
                    postCard.style.transform = 'translateY(-20px)';
                    setTimeout(() => postCard.remove(), 300);
                }
            } else {
                // If on post detail page, redirect to home
                setTimeout(() => {
                    window.location.href = response.redirect_url || '/';
                }, 1500);
            }
        } else {
            BlogApp.showNotification(response.message || 'Failed to delete post', 'danger');
        }
    } catch (error) {
        BlogApp.showNotification('Failed to delete post', 'danger');
    }
};

window.sharePost = function(postId) {
    const postCard = document.querySelector(`[data-post-id="${postId}"]`);
    const postTitle = postCard ? postCard.querySelector('.card-title a').textContent : document.title;
    const postUrl = postCard ? postCard.querySelector('.card-title a').href : window.location.href;
    
    if (navigator.share) {
        navigator.share({
            title: postTitle,
            url: postUrl
        }).catch(err => console.log('Error sharing:', err));
    } else {
        // Fallback - copy to clipboard
        navigator.clipboard.writeText(postUrl).then(() => {
            BlogApp.showNotification('Link copied to clipboard!', 'success');
        }).catch(() => {
            // Fallback for older browsers
            const textarea = document.createElement('textarea');
            textarea.value = postUrl;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            BlogApp.showNotification('Link copied to clipboard!', 'success');
        });
    }
};

// Enhanced search functionality
BlogApp.search = {
    currentQuery: '',
    searchTimeout: null,
    isSearching: false,

    init: function() {
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        
        if (!searchInput) return;

        // Live search with debounce
        searchInput.addEventListener('input', (e) => {
            this.handleInput(e.target.value.trim());
        });

        // Handle search form submission
        const searchForm = searchInput.closest('form');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.performSearch(searchInput.value.trim(), true);
            });
        }

        // Handle Enter key
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.performSearch(searchInput.value.trim(), true);
            }
        });

        // Hide results when clicking outside
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !searchResults?.contains(e.target)) {
                this.hideResults();
            }
        });
    },

    handleInput: function(query) {
        clearTimeout(this.searchTimeout);
        
        if (query.length < 2) {
            this.hideResults();
            return;
        }

        this.searchTimeout = setTimeout(() => {
            this.performSearch(query);
        }, 300);
    },

    performSearch: async function(query, redirect = false) {
        if (!query || this.isSearching) return;

        this.currentQuery = query;
        this.isSearching = true;

        if (redirect) {
            // Redirect to search results page
            window.location.href = `/?search=${encodeURIComponent(query)}`;
            return;
        }

        try {
            const response = await BlogApp.posts.search(query);
            this.displayResults(response.results);
        } catch (error) {
            console.error('Search failed:', error);
            this.displayResults([]);
        } finally {
            this.isSearching = false;
        }
    },

    displayResults: function(results) {
        const searchResults = document.getElementById('searchResults');
        if (!searchResults) return;

        if (results.length === 0) {
            searchResults.innerHTML = `
                <div class="search-result-item text-center py-3">
                    <i class="fas fa-search text-muted mb-2"></i>
                    <div class="text-muted">No results found</div>
                    <small class="text-muted">Try different keywords</small>
                </div>
            `;
        } else {
            searchResults.innerHTML = results.map(post => `
                <div class="search-result-item" onclick="window.location.href='/post/${post.id}/'">
                    <div class="d-flex align-items-start">
                        <div class="flex-grow-1">
                            <div class="fw-medium text-dark mb-1">${this.highlightQuery(post.title)}</div>
                            <div class="text-muted small mb-1">${this.highlightQuery(post.content_preview)}</div>
                            <div class="d-flex align-items-center text-muted small">
                                <span>by ${post.author_full_name}</span>
                                <span class="mx-1">·</span>
                                <span>${post.created_at_formatted}</span>
                                <span class="mx-1">·</span>
                                <i class="fas fa-heart me-1"></i>${post.total_likes}
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        searchResults.classList.remove('d-none');
    },

    highlightQuery: function(text) {
        if (!this.currentQuery) return text;
        
        const regex = new RegExp(`(${this.currentQuery})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
}