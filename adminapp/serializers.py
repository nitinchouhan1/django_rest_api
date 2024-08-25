from rest_framework import serializers
from .models import Category, User, Article, ArticleStats, Media, MediaOrderItem, MediaArticleInfo
import bcrypt

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'about': {'required': False, 'allow_blank': True},
            'cover_image': {'required': False, 'allow_blank': True},
            'meta_title': {'required': False, 'allow_blank': True},
            'meta_description': {'required': False, 'allow_blank': True},
            'keywords': {'required': False, 'allow_blank': True},
        }

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ArticleStatsSerializer(serializers.Serializer):
    total_articles = serializers.IntegerField()
    total_articles_in_category = serializers.IntegerField(required=False)
    total_articles_by_user = serializers.IntegerField(required=False)
    error = serializers.CharField(required=False)

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class MediaOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaOrderItem
        fields = '__all__'

class MediaArticleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaArticleInfo
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_image': {'required': False},
            'cover_image': {'required': False},
            'bio': {'required': False},
        }

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'role', 'slug']

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("Email is already in use")

        hashed_password = bcrypt.hashpw(validated_data['password'].encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')
        
        return User.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)