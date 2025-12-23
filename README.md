# Отчет по проекту

## Раздел 1

### 1. Модели Category, Location, Post, Comment должны быть представлены в админке – admin.py
Файл: `blogicum/blog/admin.py:1-65`
Фрагмент кода:
```python
from .models import Category, Comment, Location, Post
...
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment)
```
Пояснение: Все четыре модели импортируются и регистрируются в админке, поэтому отображаются в административном интерфейсе.

### 2. В моделях у всех полей для связи между таблицами с типом ForeignKey должны быть заданы параметры on_delete. Для большинства — CASCADE, для локации и категории — SET_NULL
Файл: `blogicum/blog/models.py:57-92`
Фрагмент кода:
```python
author = models.ForeignKey(
    User, on_delete=models.CASCADE,
    verbose_name='Автор публикации'
)
location = models.ForeignKey(
    Location,
    on_delete=models.SET_NULL, null=True, blank=True,
    verbose_name='Местоположение'
)
category = models.ForeignKey(
    Category,
    on_delete=models.SET_NULL, null=True,
    verbose_name='Категория'
)
...
author = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True,
    verbose_name='Автор комментария'
)
post = models.ForeignKey(
    Post, related_name='comments', on_delete=models.CASCADE, null=True)
```
Пояснение: Для всех ForeignKey указан `on_delete`, при этом `location` и `category` используют `SET_NULL`, остальные — `CASCADE`.

### 3. При настройке формы в forms.py для поста нужно предоставить на редактирование поля is_published, pub_date
Файл: `blogicum/blog/forms.py:12-19`
Фрагмент кода:
```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
```
Пояснение: Поля `is_published` и `pub_date` не исключены из формы, а `pub_date` настраивается виджетом.

### 4. Извлекаемые из URL ключи — в urls.py — должны быть содержательными: pk или id не годятся
Файл: `blogicum/blog/urls.py:8-27`
Фрагмент кода:
```python
path('posts/<int:post_id>/', ...)
path('posts/<int:post_id>/edit/', ...)
path('posts/<post_id>/delete/', ...)
path('posts/<post_id>/edit_comment/<comment_id>/', ...)
```
Пояснение: Используются содержательные имена параметров (`post_id`, `comment_id`, `category_slug`, `username`), без `pk`.

### 5. В маршрутах, которые настраиваются в urls.py, для ника пользователя тип параметра в URL не может быть slug
Файл: `blogicum/blog/urls.py:16-17`
Фрагмент кода:
```python
path('profile/<str:username>/',
     views.ProfileView.as_view(), name='profile'),
```
Пояснение: Для `username` используется тип `str`, а не `slug`.

### 6. Явные URL могут применяться только в path() в urls.py
Файл: `blogicum/blog/views.py:46-54`; `blogicum/templates/blog/create.html:4-31`; `blogicum/templates/blog/comment.html:4-31`
Фрагмент кода:
```python
login_url = reverse_lazy('login')
...
return reverse('blog:profile', args=[username])
```
```html
{% if view_name == 'blog:edit_post' %}
...
{% if view_name == 'blog:edit_comment' %}
```
Пояснение: В views и шаблонах используются имена маршрутов (`reverse`, `reverse_lazy`, `view_name`), явные URL не прописаны.

### 7. В контроллерах в views.py через reverse() или redirect()
Файл: `blogicum/blog/views.py:52-54`
Фрагмент кода:
```python
def get_success_url(self):
    username = self.object.author.username
    return reverse('blog:profile', args=[username])
```
Пояснение: URL вычисляется через `reverse()` по имени маршрута.

### 8. В шаблонах через {% url 'имя-маршрута' параметр %}
Файл: `blogicum/templates/includes/header.html:5-35`
Фрагмент кода:
```html
<a class="navbar-brand" href="{% url 'blog:index' %}">
...
<a class="text-decoration-none text-reset" href="{% url 'blog:profile' user.username %}">...</a>
```
Пояснение: Шаблоны формируют ссылки через `{% url %}`.

### 9. Извлечение поста, категории, комментария из базы выполняется только через get_object_or_404()
Файл: `blogicum/blog/views.py:111-118`; `blogicum/blog/views.py:164-166`; `blogicum/blog/views.py:205-206`; `blogicum/blog/views.py:226-227`
Фрагмент кода:
```python
post = get_object_or_404(Post, id=post_id)
...
self.category = get_object_or_404(
    Category, slug=self.kwargs['category_slug'], is_published=True
)
...
post = get_object_or_404(Post, id=post_id)
...
return get_object_or_404(Comment, id=comment_id)
```
Пояснение: Одиночные объекты Post, Category, Comment извлекаются через `get_object_or_404()`.

### 10. Все посты на страницах «Главная», «Посты категории», «Посты автора» должны быть дополнены количеством комментариев
Файл: `blogicum/blog/views.py:31-38`; `blogicum/blog/views.py:135-148`; `blogicum/blog/views.py:163-172`
Фрагмент кода:
```python
queryset = published_posts_with_comment_count(queryset)
...
posts = published_posts_with_comment_count(posts)
```
Пояснение: Во всех наборах постов добавляется `comment_count` через общую функцию.

### 11. Вычисление количества комментариев к постам должно находиться в единственном месте — в новой функции
Файл: `blogicum/blog/utils.py:6-24`
Фрагмент кода:
```python
def with_comment_count(queryset):
    return queryset.annotate(comment_count=Count('comments'))

def published_posts_with_comment_count(queryset, only_published=True):
    if only_published:
        queryset = filter_published_posts(queryset)
    return with_comment_count(queryset)
```
Пояснение: Подсчет комментариев вынесен в функции `with_comment_count` и `published_posts_with_comment_count`.

### 12. После вызова annotate() обязательно нужен вызов сортирующего метода
Файл: `blogicum/blog/views.py:37-38`; `blogicum/blog/models.py:76-81`
Фрагмент кода:
```python
queryset = published_posts_with_comment_count(queryset)
return queryset.order_by(*Post._meta.ordering)
```
```python
class Meta:
    ordering = ('-pub_date',)
```
Пояснение: После `annotate()` сортировка выполняется с опорой на `Post._meta.ordering`.

### 13. Вычисление одной страницы пагинатора нужно разместить в новой функции
Файл: `blogicum/blog/utils.py:27-32`; `blogicum/blog/views.py:21-23`
Фрагмент кода:
```python
def paginate_queryset(request, queryset, per_page):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return paginator, page, page.object_list, page.has_other_pages()
```
```python
class PaginationMixin:
    def paginate_queryset(self, queryset, page_size):
        return paginate_queryset(self.request, queryset, page_size)
```
Пояснение: Вычисление страницы вынесено в `paginate_queryset` и используется через mixin.

### 14. Набор постов на странице автора должен зависеть от посетителя
Файл: `blogicum/blog/views.py:135-146`
Фрагмент кода:
```python
if self.request.user != profile:
    posts = published_posts_with_comment_count(posts)
else:
    posts = published_posts_with_comment_count(posts, only_published=False)
```
Пояснение: Автор видит все свои посты, остальные — только опубликованные.

### 15. Фильтрация записей из таблицы постов по опубликованности должна размещаться в новой функции
Файл: `blogicum/blog/utils.py:11-17`
Фрагмент кода:
```python
def filter_published_posts(queryset):
    return queryset.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    )
```
Пояснение: Логика фильтрации вынесена в функцию `filter_published_posts`.

### 16. Контроллер-функции для создания, редактирования, удаления работают не с анонимом. Нужно применить @login_required
Файл: `blogicum/blog/views.py:41-94`
Фрагмент кода:
```python
@method_decorator(login_required, name='dispatch')
class PostCreateView(LoginRequiredMixin, CreateView):
    ...

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    ...

@method_decorator(login_required, name='dispatch')
class PostDeleteView(LoginRequiredMixin, DeleteView):
    ...
```
Пояснение: Для create/edit/delete применяется `@login_required` на уровне `dispatch`.

### 17. Для применения redirect() не нужно вычислять URL через reverse()
Файл: `blogicum/blog/views.py:76-79`
Фрагмент кода:
```python
return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
```
Пояснение: `redirect()` получает имя маршрута напрямую.

### 18. В контроллере post_detail() нужно анализировать автора поста
Файл: `blogicum/blog/views.py:109-118`
Фрагмент кода:
```python
post = get_object_or_404(Post, id=post_id)
if post.author == self.request.user:
    return post
published_posts = filter_published_posts(Post.objects.all())
return get_object_or_404(published_posts, id=post_id)
```
Пояснение: Автор видит свой пост, остальные — только опубликованные.

## Раздел 2

### 19. В гит-репозитории не должны храниться папки static, static-dev, html
Файл: `.gitignore:148-152`
Фрагмент кода:
```
static/
static-dev/
html/
```
Пояснение: Папки исключены через `.gitignore`.

### 20. Класс формы для поста в forms.py лучше настраивать не через fields, а через exclude; created_at не должно попадать в форму
Файл: `blogicum/blog/forms.py:12-19`; `blogicum/core/models.py:4-13`
Фрагмент кода:
```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
```
```python
created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='Добавлено',
)
```
Пояснение: Форма использует `exclude`, а `created_at` является `auto_now_add` и не редактируется.

### 21. Функции «фильтрация по опубликованным» и «дополнение числа комментариев» может быть объединена в одну
Файл: `blogicum/blog/utils.py:20-24`
Фрагмент кода:
```python
def published_posts_with_comment_count(queryset, only_published=True):
    if only_published:
        queryset = filter_published_posts(queryset)
    return with_comment_count(queryset)
```
Пояснение: Объединенная функция выполняет фильтрацию и аннотацию.

### 22. Функция, фильтрующая по опубликованности, может принимать параметром набор постов для фильтрации
Файл: `blogicum/blog/utils.py:11-17`
Фрагмент кода:
```python
def filter_published_posts(queryset):
    return queryset.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    )
```
Пояснение: Функция принимает queryset параметром и применяется к разным наборам постов.

### 23. Чтобы в контроллере post_detail() отказать в показе неопубликованного поста не автору, лучше всего делать два вызова get_object_or_404()
Файл: `blogicum/blog/views.py:109-118`
Фрагмент кода:
```python
post = get_object_or_404(Post, id=post_id)
...
published_posts = filter_published_posts(Post.objects.all())
return get_object_or_404(published_posts, id=post_id)
```
Пояснение: Первый вызов берет пост из полной таблицы, второй — из опубликованных.

### 24. Первый вызов get_object_or_404() — для извлечения поста по ключу из полной таблицы
Файл: `blogicum/blog/views.py:109-112`
Фрагмент кода:
```python
post = get_object_or_404(Post, id=post_id)
```
Пояснение: Первый вызов берет пост по ключу из полной таблицы.

### 25. Второй вызов get_object_or_404() — из набора опубликованных постов
Файл: `blogicum/blog/views.py:116-118`
Фрагмент кода:
```python
published_posts = filter_published_posts(Post.objects.all())
return get_object_or_404(published_posts, id=post_id)
```
Пояснение: Второй вызов работает по набору опубликованных постов.

### 26. Извлечения постов для уже извлеченной категории/автора лучше выполнять через поле связи
Файл: `blogicum/blog/views.py:135-140`; `blogicum/blog/views.py:168-170`
Фрагмент кода:
```python
posts = profile.posts.select_related(
    'author'
).prefetch_related('comments', 'category', 'location')
```
```python
queryset = self.category.posts.select_related(
    'author', 'category', 'location'
)
```
Пояснение: Для автора и категории используются связанные менеджеры (`profile.posts`, `category.posts`).

### 27. При указании сортировки после annotate() лучше не угадывать значение, а брать из Post._meta.ordering
Файл: `blogicum/blog/views.py:37-38`; `blogicum/blog/models.py:76-81`
Фрагмент кода:
```python
return queryset.order_by(*Post._meta.ordering)
```
```python
class Meta:
    ordering = ('-pub_date',)
```
Пояснение: Сортировка берется из `Post._meta.ordering`.

### 28. В контроллерах создания/редактирования поста нужна разная обработка для GET и POST
Файл: `blogicum/blog/views.py:56-59`; `blogicum/blog/views.py:87-90`
Фрагмент кода:
```python
def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['data'] = self.request.POST or None
    return kwargs
```
Пояснение: Форма получает `request.POST or None`, что корректно обрабатывает GET и POST.

### 29. У модели «Пользователь» есть поля, которые нельзя показывать в админке — нужен UserAdmin
Файл: `blogicum/blog/admin.py:1-72`
Фрагмент кода:
```python
from django.contrib.auth.admin import UserAdmin
...
User = get_user_model()
...
admin.site.register(User, UserAdmin)
```
Пояснение: Пользователь регистрируется в админке через `UserAdmin`, который скрывает чувствительные поля.
