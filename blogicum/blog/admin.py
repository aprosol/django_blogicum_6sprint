from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Category, Comment, Location, Post

# Установка отображения пустых значений в админке.
admin.site.empty_value_display = 'Не задано'


class PostInline(admin.TabularInline):
    """
    Определение Inline-класса, который используется
    для создания встроенных форм для связанных объектов Post.
    """

    model = Post
    # Количество дополнительных форм для ввода.
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    """Класс администрирования для модели Category."""

    inlines = (
        PostInline,
    )


class LocationAdmin(admin.ModelAdmin):
    """Класс администрирования для модели Location."""

    inlines = (
        PostInline,
    )


class PostAdmin(admin.ModelAdmin):
    """Класс администрирования для модели Post."""

    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'author',
        'location',
        'category',
        'is_published'
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


# Регистрация моделей в админке.
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment)

User = get_user_model()
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, UserAdmin)
