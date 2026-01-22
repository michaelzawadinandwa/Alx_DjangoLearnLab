from django.urls import path
from . import views

urlpatterns = [
    # Book list view (function-based)
    path('books/', views.list_books, name='list_books'),
    
    # Library detail view (class-based)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # Role-based access control URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Permission-based URLs for book operations
    path('add-book/', views.add_book, name='add_book'),
    path('edit-book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete-book/<int:pk>/', views.delete_book, name='delete_book'),
]
