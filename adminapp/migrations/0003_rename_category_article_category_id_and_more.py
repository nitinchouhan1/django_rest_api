# Generated by Django 5.1 on 2024-08-24 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_alter_category_about_alter_category_cover_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='category',
            new_name='category_id',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='user',
            new_name='user_id',
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='cover_image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='short_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
