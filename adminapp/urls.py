from django.urls import path
from . import views

urlpatterns = [

    path('admin/articles', views.list_articles, name='list_articles'),
    path('admin/article/<int:id>', views.get_article_by_id, name='get_article_by_id'),
    path('admin/article/flags', views.get_article_flags, name='get_article_flags'),
    path('admin/article/create', views.create_article, name='create_article'),
    path('admin/article/update', views.update_article, name='update_article'),
    path('admin/article/update/status', views.update_article_status, name='update_article_status'),
    path('admin/article/update/flag', views.update_article_flag, name='update_article_flag'),
    path('admin/article/delete', views.delete_article, name='delete_article'),


    path('admin/categories', views.list_categories, name='list-categories'),
    path('admin/categories', views.list_categories_by_name, name='list-categories-by-name'),
    path('admin/category/<int:id>', views.get_category_by_id, name='get-category-by-id'),
    path('admin/category/create', views.create_category, name='create-category'),
    path('admin/category/update', views.update_category, name='update-category'),
    path('admin/category/delete', views.delete_category, name='delete-category'),

    path('admin/users/', views.list_users, name='list_users'),
    path('admin/users/search', views.search_users, name='search_users'),
    path('admin/user/<int:user_id>', views.get_user_by_id, name='get_user_by_id'),
    path('admin/user/create', views.create_user, name='create_user'),
    path('admin/user/update', views.update_user, name='update_user'),
    path('admin/user/set-password', views.set_user_password, name='set_user_password'),
    path('admin/user/set-status', views.set_user_status, name='set_user_status'),

    path('admin/stats', views.get_stats, name='get_stats'),
    # path('auth/create_user', views.create_user, name='create-user')
    path('signin', views.signIn, name='signin'),
]