# Generated by Django 5.1 on 2024-08-24 22:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_articles', models.PositiveIntegerField(default=0)),
                ('active_articles', models.PositiveIntegerField(default=0)),
                ('flags', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('about', models.TextField()),
                ('cover_image', models.URLField()),
                ('meta_title', models.CharField(max_length=255)),
                ('meta_description', models.TextField()),
                ('keywords', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=20)),
                ('media', models.URLField()),
                ('source', models.URLField()),
                ('media_order', models.PositiveIntegerField()),
                ('is_embed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('profile_image', models.URLField()),
                ('cover_image', models.URLField()),
                ('bio', models.TextField()),
                ('role', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('short_description', models.TextField()),
                ('cover_image', models.URLField()),
                ('content', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('tags', models.JSONField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('relevance', models.FloatField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='MediaOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.media')),
            ],
        ),
        migrations.CreateModel(
            name='MediaArticleInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.user')),
            ],
        ),
    ]