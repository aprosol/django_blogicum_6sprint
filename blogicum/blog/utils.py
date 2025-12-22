from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone


def with_comment_count(queryset):
    """Annotate posts with comment_count in one place."""
    return queryset.annotate(comment_count=Count('comments'))


def filter_published_posts(queryset):
    """Filter posts by published status and availability for any queryset."""
    return queryset.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    )


def published_posts_with_comment_count(queryset, only_published=True):
    """Optionally filter by published status and add comment_count."""
    if only_published:
        queryset = filter_published_posts(queryset)
    return with_comment_count(queryset)


def paginate_queryset(request, queryset, per_page):
    """Return a single page for the given queryset."""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return paginator, page, page.object_list, page.has_other_pages()
