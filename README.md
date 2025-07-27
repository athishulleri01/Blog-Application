# Django Blog Application Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Setup Instructions](#setup-instructions)
5. [API Documentation](#api-documentation)
6. [Frontend Features](#frontend-features)
7. [Models Documentation](#models-documentation)
8. [Views Documentation](#views-documentation)
9. [URL Configuration](#url-configuration)
10. [Testing](#testing)
11. [Deployment](#deployment)

## Project Overview

A modern blog platform built with Django and Django REST Framework featuring user authentication, post creation, commenting system, and social interaction features like post likes. The application provides both traditional web views and RESTful API endpoints for seamless frontend interactions.

### Technology Stack
- **Backend**: Django 4.x, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, JavaScript, AJAX, Bootstrap5
- **Authentication**: Django's built-in authentication system
- **API**: RESTful API with DRF

## Features

### Core Features
- ✅ User registration, login, and logout
- ✅ Create, read, update, delete blog posts
- ✅ Comment system with CRUD operations
- ✅ Like/unlike posts functionality
- ✅ User profiles with post and comment history
- ✅ Search functionality for posts
- ✅ Pagination for posts and comments
- ✅ Responsive design

### Authentication & Authorization
- Only authenticated users can create posts and comments
- Users can only edit/delete their own posts and comments
- Session-based authentication for web views
- Token authentication ready for API access

### AJAX Features
- Dynamic post creation without page refresh
- Real-time like/unlike functionality
- Comment system with live updates
- Profile editing with instant feedback
- Search with live results

## Project Structure

```
Blog-Application/
├── config/
│   ├── __init__.py
│   ├── urls.py
│   ├── wsgi.py
|   └── settings/
|      ├── __init__.py
|      ├── base.py
|      ├── local.py
|      └── production.py
├── core_apps/
│   ├── __init__.py
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   ├── posts/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   └── admin.py
│   └── comments/
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── serializers.py
│       └── admin.py
├── templates/
│   ├── base.html
│   ├── user/
│   │   ├── home.html
│   │   ├── auth/
│   │   │   ├── signin.html
│   │   │   └── signup.html
│   │   └── profile/
│   │       └── profile.html
│   ├── includes/
│   │   ├── navbar.html
│   │   ├── footer.html
│   └── blog/
│       ├── post_details.html
│       └── components/
│           ├── comment_item.html
│           └── post_card.html
│           ├── comments_list.html
│           └── pagination.html
├── static/
|    ├── css/
|    ├── js/
|    └── images/
├── requirements/
|    ├── base.txt
|    ├── local.txt
|    └── production.txt
├── .envs/
|    ├── .env.example
|    ├── .env.local
├── manage.py
├── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/athishulleri01/Blog-Application.git
cd Blog-Application
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# On development purpose:
pip install -r requirements\base.txt 
```

### 4. Environment Configuration
Create a `.env.local` file in the .envs folder:

```env
SECRET_KEY=your-secret-key-here
ADMIN_URL=
```

### 5. Database Setup
```bash
# Create and run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### 8. Test the Application
```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test core_apps.posts
python manage.py test core_apps.accounts
python manage.py test core_apps.comments
```

## Screenshots

### 🏠 Homepage (Before Login)
![Homepage](screenshots/homepage.png)

### 🔐 Login Page
![Login](screenshots/login.png)

### 📝 Register Page
![Register](screenshots/register.png)

### 🏡 Home (After Login)
![Home Logged In](screenshots/home_loggedin.png)

### ✍️ Create a Post
![Post a Post](screenshots/post_create.png)

### 👀 View Posts
![View Posts](screenshots/post_view.png)

### ✏️ Edit a Post
![Edit Post](screenshots/post_edit.png)

### 🗑️ Delete a Post
![Delete Post](screenshots/post_delete.png)

### ❤️ Like a Post
![Like Post](screenshots/post_like.png)

### 💬 Comment on a Post
![Comment Post](screenshots/post_comment.png)

### 🖊️ Edit a Comment
![Edit Comment](screenshots/comment_edit.png)

### ❌ Delete a Comment
![Delete Comment](screenshots/comment_delete.png)

### 👤 Profile Page
![Profile Page](screenshots/profile_page.png)

### ⚙️ Edit Profile
![Edit Profile](screenshots/profile_edit.png)

### 🧾 View User's Posts
![User Posts](screenshots/user_posts.png)

### 💬 View User's Comments
![User Comments](screenshots/user_comments.png)

### 🔓 Logout
![Logout](screenshots/logout.png)

## API Documentation

### Authentication Endpoints

#### Register User
```http
POST /accounts/ajax/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password1": "securepassword123",
    "password2": "securepassword123"
}
```

#### Login User
```http
POST /accounts/ajax/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "securepassword123"
}
```

### Posts API Endpoints

#### List All Posts
```http
GET /api/posts/
```

#### Create Post
```http
POST /ajax/posts/create/
Content-Type: application/json
Authorization: Required (logged in user)

{
    "title": "My Blog Post",
    "content": "This is the content of my blog post."
}
```

#### Get Post Detail
```http
GET /post/{id}/
```

#### Update Post
```http
PUT /ajax/posts/{id}/update/
Content-Type: application/json
Authorization: Required (post author only)

{
    "title": "Updated Title",
    "content": "Updated content"
}
```

#### Delete Post
```http
DELETE /ajax/posts/{id}/delete/
Authorization: Required (post author only)
```

#### Like/Unlike Post
```http
POST /ajax/posts/{id}/like/
Authorization: Required (logged in user)
```

### Comments API Endpoints

#### List Comments for Post
```http
GET /api/posts/{post_id}/comments/
```

#### Create Comment
```http
POST /ajax/posts/{post_id}/comments/
Content-Type: application/json
Authorization: Required (logged in user)

{
    "text": "This is my comment"
}
```

#### Update Comment
```http
PUT /comments/ajax/edit/{comment_id}/
Content-Type: application/json
Authorization: Required (comment author only)

{
    "text": "Updated comment text"
}
```

#### Delete Comment
```http
DELETE /ajax/comments/{comment_id}/delete/
Authorization: Required (comment author only)
```

### Search API
```http
GET /api/search/?q=search_term
```

## Frontend Features

### AJAX Implementation
All major operations are implemented with AJAX for smooth user experience:

- **Post Management**: Create, edit, delete posts without page refresh
- **Comment System**: Add, edit, delete comments dynamically
- **Like System**: Toggle likes with real-time count updates
- **Search**: Live search results as you type
- **Profile Updates**: Edit profile information instantly

### Form Validation
- Client-side validation for immediate feedback
- Server-side validation for security
- Error handling with user-friendly messages

### Responsive Design
- Mobile-first approach
- Bootstrap-compatible styling
- Clean, modern interface

## Models Documentation

### User Profile Model
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Post Model
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
```

### Comment Model
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## Views Documentation

### Authentication Views
- `ajax_register`: Handle user registration via AJAX
- `ajax_login`: Handle user login via AJAX
- `profile_view`: Display user profile with posts and comments
- `ajax_edit_profile`: Update user profile information

### Post Views
- `home`: Main page with paginated post list
- `post_detail`: Individual post view with comments
- `create_post_ajax`: Create new post via AJAX
- `update_post_ajax`: Update existing post
- `delete_post_ajax`: Delete post
- `toggle_like`: Like/unlike post functionality

### Comment Views
- `create_comment_ajax`: Add comment to post
- `edit_comment_ajax`: Edit existing comment
- `delete_comment_ajax`: Delete comment
- `load_comments_page`: Paginated comment loading

## URL Configuration

### Main URLs (`blog_project/urls.py`)
```python
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("core_apps.posts.urls")),
    path('accounts/', include('core_apps.accounts.urls')),
    path('api/', include('core_apps.posts.urls')),
    path('', include('core_apps.comments.urls')),
    path('api/', include('core_apps.comments.urls')),
]
```

### App-specific URL patterns are organized in their respective `urls.py` files

## Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific tests
python manage.py test core_apps.posts.tests
python manage.py test core_apps.accounts.tests
python manage.py test core_apps.comments.tests

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Coverage
The application includes comprehensive tests for:
- Model functionality
- View responses
- API endpoints
- Authentication flows
- AJAX operations

## Deployment

### Production Setup

1. **Environment Variables**
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

2. **Database Configuration**
Update `settings.py` for PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Static Files**
```bash
python manage.py collectstatic
```

4. **Web Server Configuration**
- Use Gunicorn or uWSGI for WSGI server
- Configure Nginx for static file serving
- Set up SSL certificates

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "blog_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Security Considerations

- CSRF protection enabled for all forms
- User input validation and sanitization
- SQL injection protection via Django ORM
- XSS protection with template escaping
- Secure authentication flows
- Permission-based access control

## Performance Features

- Database query optimization with `select_related` and `prefetch_related`
- Pagination to handle large datasets
- Static file optimization
- Efficient AJAX requests to minimize server load

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Progressive enhancement for older browsers
- Mobile-responsive design

## Troubleshooting

### Common Issues

1. **Migration Errors**
```bash
python manage.py makemigrations --empty core_apps.posts
python manage.py migrate --fake-initial
```

2. **Static Files Not Loading**
```bash
python manage.py collectstatic --clear
```

3. **Permission Denied Errors**
Check file permissions and Django user permissions

4. **Database Connection Issues**
Verify database configuration in settings.py

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the test files for usage examples

---

**Note**: This documentation covers the complete setup and usage of the Django blog application. Make sure to follow the setup instructions carefully and test all features before deployment.
