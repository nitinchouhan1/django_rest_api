from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Article, User, Category, ArticleStats
from .serializers import ArticleSerializer, CategorySerializer, RegisterSerializer, LoginSerializer, UserSerializer, ArticleStatsSerializer
from rest_framework.pagination import PageNumberPagination
import jwt
import datetime
from django.conf import settings
import bcrypt

@api_view(['POST'])
def signIn(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                
                if bcrypt.checkpw(serializer.validated_data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token_payload = {
                        'user_id': user.id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1),
                        'iat': datetime.datetime.utcnow()
                    }
                    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
                    user.last_login = datetime.datetime.now()
                    user.save()
                    return Response({"token": token}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_categories_by_name(request):
    search_term = request.GET.get('search', '')
    categories = Category.objects.filter(name__icontains=search_term)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_category_by_id(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category)
    return Response(serializer.data)

@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_category(request):
    category_id = request.data.get('id')
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def delete_category(request):
    category_id = request.data.get('category_id')
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_users(request):
    search_term = request.GET.get('search', '')
    print(search_term)
    users = User.objects.filter(name__icontains=search_term) | User.objects.filter(email__icontains=search_term)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_user(request):
    user_id = request.data.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        if 'password' in request.data:
            serializer.validated_data['password'] = make_password(request.data.get('password'))
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def set_user_password(request):
    user_id = request.data.get('user_id')
    password = request.data.get('password')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user.save()
    return Response({'detail': 'Password updated'})

@api_view(['POST'])
def set_user_status(request):
    user_id = request.data.get('user_id')
    is_active = request.data.get('is_active')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user.is_active = is_active
    user.save()
    return Response({'detail': 'User status updated'})


@api_view(['GET'])
def list_articles(request):
    paginator = PageNumberPagination()
    paginator.page_size = int(request.query_params.get('page_size', 10))
    articles = Article.objects.all()
    
    if 'category_id' in request.query_params:
        articles = articles.filter(category_id=request.query_params['category_id'])
    if 'user_id' in request.query_params:
        articles = articles.filter(user_id=request.query_params['user_id'])
    if 'sort_by' in request.query_params:
        sort_by = request.query_params['sort_by']
        if sort_by in ['views', 'updated_at']:
            articles = articles.order_by(sort_by)
    if 'title' in request.query_params:
        articles = articles.filter(title__icontains=request.query_params['title'])
    if 'is_promoted' in request.query_params:
        articles = articles.filter(is_promoted=request.query_params['is_promoted'].lower() == 'true')
    
    result_page = paginator.paginate_queryset(articles, request)
    serializer = ArticleSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def get_article_by_id(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    serializer = ArticleSerializer(article)
    return Response(serializer.data)

@api_view(['GET'])
def get_article_flags(request):
    stats = ArticleStats.objects.first()
    if not stats:
        return Response({'detail': 'No stats available.'}, status=404)

    return Response(stats.flags)

@api_view(['POST'])
def create_article(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_article(request):
    try:
        article = Article.objects.get(id=request.data.get('id'))
    except Article.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    serializer = ArticleSerializer(article, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_article_status(request):
    try:
        article = Article.objects.get(id=request.data.get('article_id'))
    except Article.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    article.status = request.data.get('status', article.status)
    article.save()
    return Response({'status': article.status})

@api_view(['POST'])
def update_article_flag(request):
    try:
        article = Article.objects.get(id=request.data.get('article_id'))
    except Article.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    flags = request.data.get('flag', {})
    for key, value in flags.items():
        setattr(article, key, value)
    article.save()
    return Response({'flags': flags})

@api_view(['POST'])
def delete_article(request):
    try:
        article = Article.objects.get(id=request.data.get('article_id'))
    except Article.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    article.delete()
    return Response({'detail': 'Article deleted.'})


@api_view(['GET'])
def get_stats(request):
    category_id = request.GET.get('category_id')
    user_id = request.GET.get('user_id')

    data = {}

    if category_id:
        articles_in_category = Article.objects.filter(category_id=category_id).count()
        data['total_articles_in_category'] = articles_in_category

    if user_id:
        articles_by_user = Article.objects.filter(user_id=user_id).count()
        data['total_articles_by_user'] = articles_by_user

    if not category_id and not user_id:
        total_articles = Article.objects.count()
        data['total_articles'] = total_articles

    if not data:
        return JsonResponse({'error': 'At least one of category_id or user_id parameter is required'}, status=400)

    
    return Response({'data': data}, status=200)
