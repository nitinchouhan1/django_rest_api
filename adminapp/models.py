from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    about = models.TextField(blank=True)
    cover_image = models.URLField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

class User(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_image = models.URLField(blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    tags = models.JSONField(blank=True, null=True)  # For storing tags
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    relevance = models.FloatField(null=True, blank=True)

class ArticleStats(models.Model):
    total_articles = models.PositiveIntegerField(default=0)
    active_articles = models.PositiveIntegerField(default=0)
    flags = models.JSONField(default=dict)

class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)
    media = models.URLField()
    source = models.URLField()
    media_order = models.PositiveIntegerField()
    is_embed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MediaOrderItem(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

class MediaArticleInfo(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
